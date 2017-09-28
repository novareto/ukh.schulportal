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
                email=result.email,
                passwort=result.passwort,
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

    def checkRule(self, login):
        uvcsite.log(login)
        return True


from zope.component import getUtility
from ukh.schulportal.configs.cache import cacheme


def cachekey(func, self):
    key = "%s_%s" % (self.__class__.__name__, self.id)
    print "KEY", key
    return key


class UKHPrincipal(Principal):

    def __init__(self, id, description):
        self.id = id
        self.description = description
        self.groups = []

    @property
    def title(self):
        return self.getAdresse().get('iknam1', self.id)

    def getOID(self, id=None):
        """
        Gibt die eindeutige OID fuer einen Mitgliedsbetrieb zurueck
        """
        if not id:
            id = self.id
        um = getUtility(IUserManagement)
        usr = um.getUser(id)
        return usr.get('oid', '')

    @cacheme(cachekey)
    def getAdresse(self):
        """
        Holt die Adresse und die Bankverbindung aus der Datenbank
        """
        id = self.id
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
