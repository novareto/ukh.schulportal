# -*- coding: utf-8 -*-
# Copyright (c) 2007-2013 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite
from uvcsite.content.productregistration import getProductRegistrations


grok.templatedir('templates')


class LandingPage(uvcsite.Page):
    grok.context(uvcsite.IUVCSite)
    grok.name('index')

    def getItems(self):
        print dict([x for x in getProductRegistrations()])
        return dict([x for x in getProductRegistrations()])

    def getHomeFolder(self):
        return uvcsite.getHomeFolderUrl(self.request)
