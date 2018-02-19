#!/usr/bin/python
# -*- coding: utf-8 -*-

import grok
import uvcsite

from ukhtheme.grok.layout import ILayer
from zope.pluggableauth.factories import Principal, AuthenticatedPrincipalFactory
from uvcsite.extranetmembership.interfaces import IUserManagement, IExtranetMember
from zope.pluggableauth.interfaces import IPrincipalInfo, AuthenticatedPrincipalCreated

from sqlalchemy import and_
from z3c.saconfig import Session
from ukh.schulportal.configs.database_setup import users, einrichtungen
from zope.sqlalchemy import mark_changed
from sqlalchemy.sql import select
from zope.component import getUtility
from uvc.cache import cache_me


class User(dict):
    pass


class UserManagement(grok.GlobalUtility):
    """ Utility for Usermanagement """
    grok.implements(IUserManagement)

    UserInterface = IExtranetMember

    def updUser(self, **kwargs):
        """Updates a User"""
        mnr = kwargs.get('mnr')
        az = kwargs.get('az')
        session = Session()
        sql = users.update().where(
            and_(users.c.login == mnr, users.c.az == az)
            ).values(passwort=kwargs.get('passwort'), rollen=','.join(kwargs.get('rollen')))
        session.execute(sql)
        mark_changed(session)

    def updUserStamm(self, **kwargs):
        """Updates a User"""
        mnr, az = self.zerlegUser(uvcsite.getPrincipal().id)
        session = Session()
        sql = users.update().where(
            and_(users.c.login == mnr, users.c.az == az)
            ).values(vname=kwargs.get('vname'), nname=kwargs.get('nname'),
                     vwhl=kwargs.get('vwhl'), tlnr=kwargs.get('tlnr'),
                     anr=kwargs.get('anr'), funktion=kwargs.get('funktion'),
                     titel=kwargs.get('titel'), email=kwargs.get('email'),
                     )
        session.execute(sql)
        mark_changed(session)

    def deleteUser(self, cn):
        mnr, az = self.zerlegUser(cn)
        session = Session()
        sql = users.delete().where(and_(users.c.login == mnr, users.c.az == az))
        session.execute(sql)
        mark_changed(session)

    def addUser(self, **kw):
        mnr, az = kw['mnr'].split('-')
        mnr, az = self.zerlegUser(kw['mnr'])
        user = self.getUser(mnr)
        session = Session()
        import pdb; pdb.set_trace()
        sql = users.insert(dict(
            login=mnr,
            passwort=kw.get('passwort'),
            az=az,
            email=kw.get('email', ''),
            oid=str(user['oid']),
            rollen=','.join(kw.get('rollen', []))
            )
        )
        session.execute(sql)
        mark_changed(session)

    def zerlegUser(self, mnr):
        ll = mnr.split('-')
        if len(ll) == 1:
            return mnr, 'eh'
        return ll

    def getUser(self, mnr):
        """Return a User"""
        mnr, az = self.zerlegUser(mnr)
        if mnr == "servicetelefon":
            return User(
                mnr="servicetelefon",
                az=00,
                oid="ukh",
                email="servicetelefon@ukh.de",
                passwort="ukh",
                rollen=[],
                )

        session = Session()
        query = session.query(users).filter(
            users.c.login == mnr, users.c.az == az)
        if query.count() == 1:
            result = query.one()
            az = result.az
            #import pdb; pdb.set_trace()
            if result.az == 'eh':
                az = '00'
            return User(
                mnr=result.login,
                az=az,
                oid=result.oid,
                nname=result.nname.strip(),
                vname=result.vname.strip(),
                vwhl=result.vwhl.strip(),
                tlnr=result.tlnr.strip(),
                anr=result.anr.strip(),
                funktion=result.funktion.strip(),
                titel=result.titel.strip(),
                email=result.email.strip(),
                passwort=result.passwort.strip(),
                rollen=result.rollen.strip().split(','))
        return None

    def getUsersByMnr(self, mnr):
        return self.getUser(mnr)

    def getUserByEMail(self, mail):
        session = Session()
        query = session.query(users).filter(
            users.c.email == mail)

        if query.count() == 1:
            result = query.one()
            az = result.az
            if result.az == 'eh':
                az = '00'
            return User(
                mnr=result.login,
                az=az,
                oid=result.oid,
                email=result.email,
                passwort=result.passwort,
                rollen=result.rollen)
        return None

    def getUserGroups(self, mnr):
        """Return a group of Users"""
        ret = []
        session = Session()
        query = session.query(users).filter(users.c.login == mnr)
        for x in query.all():
            if x.az == "eh":
                continue
            usr = "%s-%s" % (x.login, x.az)
            ret.append(User(
                cn=usr, mnr=x.login, rollen=x.rollen.strip().split(','), az=x.az))
        return ret

    def updatePasswort(self, **kwargs):
        """Change a passwort from a user"""
        mnr, az = self.zerlegUser(uvcsite.getPrincipal().id)
        session = Session()
        sql = users.update().where(
            and_(users.c.login == mnr, users.c.az == az)
            ).values(passwort=kwargs.get('passwort'),)
        session.execute(sql)
        mark_changed(session)

    def checkRule(self, login):
        uvcsite.log(login)
        return True


def cachekey(func, self):
    key = "%s_%s" % (self.__class__.__name__, self.id)
    return key


class UKHPrincipal(Principal):

    def __init__(self, id, description):
        self.id = id
        self.description = description
        self.groups = []

    @property
    def title(self):
        if self.id == "servicetelefon-0":
            return u"ServiceTelefon"
        return self.getAdresse().get('iknam1', self.id)

    def getUM(self):
        return getUtility(IUserManagement)

    def getOID(self, id=None):
        """
        Gibt die eindeutige OID fuer einen Mitgliedsbetrieb zurueck
        """
        if not id:
            id = self.id
        um = self.getUM()
        usr = um.getUser(id)
        return usr.get('oid', '')

    @cache_me(cachekey)
    def getAdresse(self):
        """
        Holt die Adresse und die Bankverbindung aus der Datenbank
        """
        id = self.id
        if id == "servicetelefon-0":
            return {'iknam1': 'Service Telefon'}
        oid = self.getOID(id)
        session = Session()
        s = select([einrichtungen], and_(einrichtungen.c.enrrcd == str(oid)))
        res = session.execute(s).fetchone()
        d = dict()
        if not res:
            return d
        for k, v in res.items():
            if isinstance(v, str):
                d[k.lower()] = v.strip()
            if isinstance(v, unicode):
                d[k.lower()] = v.strip()
            else:
                d[k.lower()] = v
        return d


class UKHPrincpalFactory(AuthenticatedPrincipalFactory, grok.MultiAdapter):
    grok.adapts(IPrincipalInfo, ILayer)

    def __call__(self, authentication):
        principal = UKHPrincipal(
            authentication.prefix + self.info.id,
            self.info.description)
        grok.notify(AuthenticatedPrincipalCreated(
            authentication, principal, self.info, self.request))
        return principal
