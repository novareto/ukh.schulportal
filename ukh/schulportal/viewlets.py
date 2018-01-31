# -*- coding: utf-8 -*-

import grok
from os import path
from ukhtheme.grok.layout import ILayer
from ukhtheme.grok.viewlets import SocialLinks
from zope.interface import Interface
from zope.viewlet.interfaces import IContentProvider
from zope.component import getMultiAdapter, queryMultiAdapter
from megrok.pagetemplate import PageTemplate
from zope.pagetemplate.interfaces import IPageTemplate
from uvc.api.api import get_template
from ukhtheme.grok.viewlets import BGHeader
from ukh.spsuaz.components import SUnfallanzeigen
from uvc.letterbasket.components import LetterBasket

templates_dir = path.join(path.dirname(__file__), 'templates')


class BGHeader(BGHeader):
    grok.layer(ILayer)
    template = get_template(templates_dir, 'bgheader.cpt')

    def welcome(self):
        pr = self.request.principal
        if pr.title == u'Unauthenticated User':
            return ""
        adr = pr.getAdresse()
        name = adr.get('iknam1', '')
        return "<h3>Herzlich Willkommen</h3> <p> %s </p>" % name

    def links(self):
        rc = {}
        pr = self.request.principal
        if pr.title == u'Unauthenticated User':
            return rc
        rc['logout'] = "%s/logout" % self.view.application_url()
        rc['profile'] = "%spersonalpanelview" % uvcsite.getHomeFolderUrl(self.request)
        return rc


class Navigation(grok.ViewletManager):
    grok.name('navigation')
    grok.context(Interface)
    grok.layer(ILayer)


class UniqueNavigation(grok.Viewlet):
    grok.name('central_nav')
    grok.context(Interface)
    grok.layer(ILayer)
    grok.viewletmanager(Navigation)
    grok.require('zope.View')

    id = "globalmenuviewlet"

    def update(self):
        globalmenu = getMultiAdapter(
            (self.view.context, self.request, self.view),
            IContentProvider, 'globalmenu')

        quicklinks = queryMultiAdapter(
            (self.view.context, self.request, self.view),
            IContentProvider, 'quicklinks')

        self.menus = {
            #'globalmenu': globalmenu.getMenuItems(),
            #'personalpreferences': personalpreferences.getMenuItems(),
            #'footer': footer.getMenuItems(),
            'quicklinks': quicklinks.getMenuItems(),
        }
        menus = [x for x in self.menus.values() if x]
        am = []
        for amenu in menus:
            for menu in amenu:
                am.append(menu)
        self.smenus = sorted(am, key=lambda item: item['order'])
        self.renderables = globalmenu.getRenderableItems()

    def render(self):
        template = getMultiAdapter((self, self.request), IPageTemplate)
        return template()


class UniqueNavTemplate(PageTemplate):
    grok.view(UniqueNavigation)
    grok.layer(ILayer)
    template = get_template(templates_dir, 'unique.cpt')


class SocialLinks(SocialLinks):
    grok.layer(ILayer)

    def available(self):
        return False

from uvc.layout.interfaces import IQuickLinks
import uvcsite


class Home(uvcsite.MenuItem):
    grok.viewletmanager(IQuickLinks)
    grok.context(Interface)
    grok.order(10)

    @property
    def title(self):
        return '<span class="glyphicon glyphicon-home" aria-hidden="true"></span>'

    @property
    def action(self):
        return self.view.application_url()


class Verbandbuch(uvcsite.ProductMenuItem):
    grok.viewletmanager(IQuickLinks)
    grok.context(Interface)
    grok.order(20)
    reg_name = "KinderUnfallanzeige"
    title = "Verbandbuch"

    @property
    def action(self):
        action = super(Verbandbuch, self).action
        action = action.replace('/add', '?filter=vb')
        return action


class Unfallanzeige(uvcsite.ProductMenuItem):
    grok.viewletmanager(IQuickLinks)
    grok.context(Interface)
    grok.order(30)
    reg_name = "KinderUnfallanzeige"
    title = "Unfallanzeigen"

    @property
    def action(self):
        action = super(Unfallanzeige, self).action
        action = action.replace('/add', '?filter=uaz')
        return action


class Postfach(uvcsite.ProductMenuItem):
    grok.viewletmanager(IQuickLinks)
    grok.context(Interface)
    grok.order(30)
    reg_name = "nachrichten"
    title = "Postfach"

    @property
    def action(self):
        action = super(Postfach, self).action
        action = action.replace('/@@add', '')
        return action


class MeinDaten(uvcsite.MenuItem):
    grok.context(uvcsite.IMyHomeFolder)
    grok.title(u'Schuldaten')
    grok.viewletmanager(uvcsite.IPersonalMenu)

    @property
    def action(self):
        return self.view.url(self.context, 'meinedaten')


from uvc.layout.slots.managers import Tabs


class Tabs(Tabs):
    grok.layer(ILayer)

    def render(self):
        return ""


class QuickAdd(grok.Viewlet):
    grok.viewletmanager(uvcsite.IAboveContent)
    grok.context(SUnfallanzeigen)

    def render(self):
        if self.request.form.get('filter', '') == 'vb':
            return '<a class="btn" href="%s"> Neuer Eintrag </a>' % self.view.url(self.context, 'addverbandbuch')
        return '<a class="btn" href="%s"> Neuer Eintrag </a>' % self.view.url(self.context, 'add')


class QuickAddLB(grok.Viewlet):
    grok.viewletmanager(uvcsite.IAboveContent)
    grok.context(LetterBasket)

    def render(self):
        return '<a class="btn" href="%s"> Neuer Eintrag </a>' % self.view.url(self.context, '@@add')
