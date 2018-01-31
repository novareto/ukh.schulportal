# -*- coding: utf-8 -*-
# Copyright (c) 2007-2013 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite


from megrok import resourceviewlet
from resources import ukhcss, ukhjs
from zope.interface import Interface
from uvc.layout.slots.managers import Footer
from zope.authentication.interfaces import IUnauthenticatedPrincipal
from uvcsite.content.productregistration import getProductRegistrations


grok.templatedir('templates')


class UKHResourceViewlet(resourceviewlet.ResourceViewlet):
    grok.context(Interface)
    resources = [ukhcss, ukhjs]

    def update(self):
        ukhcss.need()
        ukhjs.need()


class MeineDaten(uvcsite.Page):
    grok.context(uvcsite.IMyHomeFolder)

    @property
    def daten(self):
        dat = {}
        x = self.request.principal.getAdresse()
        dat['enrlfd'] = x[u'enrlfd']
        dat['nz1'] = x[u'iknam1'] + ' ' + x[u'iknam2']
        dat['nz2'] = x[u'iknam3'] + ' ' + x[u'iknam4']
        dat['nz3'] = x[u'ikstr'] + ' ' + str(x[u'ikhnr'])
        dat['nz4'] = str(x[u'ikhplz']) + ' ' + x[u'ikhort']
        dat['tel'] = str(x[u'tkitelv']) + '-' + str(x[u'tkitel'])
        dat['fax'] = str(x[u'tkifaxv']) + '-' + str(x[u'tkifax'])
        dat['mail'] = x[u'tkieml']
        return dat


class LandingPage(uvcsite.Page):
    grok.context(uvcsite.IUVCSite)
    grok.name('index')

    def getItems(self):
        items = dict([x for x in getProductRegistrations()])
        return items

    def getHomeFolder(self):
        return uvcsite.getHomeFolderUrl(self.request)


class StartMenu(uvcsite.MenuItem):
    grok.context(Interface)
    grok.viewletmanager(uvcsite.IGlobalMenu)
    grok.title('Startseite')
    grok.order(1)

    @property
    def title(self):
        return u'<span class="glyphicon glyphicon-home" aria-hidden="true"></span>'

    @property
    def action(self):
        return self.view.application_url()


class LogoutMenu(uvcsite.MenuItem):
    """ Menu fuer das Logout """
    grok.require('zope.View')
    grok.order(99)
    grok.context(Interface)
    grok.title('Abmelden')
    grok.viewletmanager(uvcsite.IGlobalMenu)

    @property
    def action(self):
        return self.view.application_url() + '/logout'


class Logout(grok.View):
    """
    Menueeintrag zum Ausloggen
    mit Cookie loeschen.
    """
    grok.context(Interface)
    grok.title(u'Abmelden')

    KEYS = ("beaker.session.id", "dolmen.authcookie", "auth_pubtkt")

    def update(self):
        if not IUnauthenticatedPrincipal.providedBy(self.request.principal):
            for key in self.KEYS:
                self.request.response.expireCookie(key, path='/', domain="ukh.de")

    def render(self):
        self.request.response.expireCookie('beaker.session.id', path='/')
        self.request.response.expireCookie('dolmen.authcookie', path='/')
        self.request['beaker.session'].delete()
        url = self.application_url()+'/index'
        self.response.redirect(url)


class FooterItem(grok.Viewlet):
    grok.context(Interface)
    grok.viewletmanager(Footer)


from uvcsite.content.views import ProductFolderValues, Index
from ukh.spsuaz.components import SUnfallanzeigen
from uvc.unfallanzeige.verbandsbuch import IVerbandbuchEintrag


class ProductFolderValues(ProductFolderValues):
    grok.adapts(SUnfallanzeigen, None, Index)

    @property
    def values(self):
        values = super(ProductFolderValues, self).values
        uaz_filter = self.request.form.get('filter')
        if uaz_filter == 'uaz':
            return [x for x in values if not IVerbandbuchEintrag.providedBy(x)]
        elif uaz_filter == 'vb':
            return [x for x in values if IVerbandbuchEintrag.providedBy(x)]
        return [x for x in values if not IVerbandbuchEintrag.providedBy(x)]


class UAZVBIndex(Index):
    grok.context(SUnfallanzeigen)

    @property
    def title(self):
        if self.request.form.get('filter', '') == 'vb':
            return u"Verbandbuch"
        return u"Unfallanzeigen"
