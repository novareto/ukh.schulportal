# -*- coding: utf-8 -*-
# Copyright (c) 2007-2013 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite

from uvcsite.auth.interfaces import ICOUser
from zope.component import getUtility
from uvcsite.extranetmembership.interfaces import IUserManagement
from uvcsite.homefolder.views import Index
from uvc.configpanel import get_plugin_configuration
from uvc.tbskin.skin import ITBSkinLayer
from ukhtheme.grok.layout import ILayer


class Index(Index):
    grok.layer(ILayer)

    def getSortOrder(self):
        return get_plugin_configuration(name='homefolder_sorting').get('sortOrder', u'ascending')

    def getSortOn(self):
        return get_plugin_configuration(name='homefolder_sorting').get('sortOn', 'table-modified-5')
