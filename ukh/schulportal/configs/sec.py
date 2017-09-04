# -*- coding: utf-8 -*-
# Copyright (c) 2007-2013 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite

from uvc.configpanel import get_plugin_configuration
from uvcsite.auth.interfaces import ICOUser
from dolmen.security.policies import ExtraRoleMap
from zope.securitypolicy.interfaces import Allow, Deny
from zope.securitypolicy.securitymap import SecurityMap


class CoUserRole(grok.Role):
    grok.name('uvc.CoUser')
    grok.permissions('uvc.ViewContent')


class SpecialSecurity(ExtraRoleMap, grok.Adapter):
    grok.context(uvcsite.IContent)
    grok.baseclass()

    def _compute_extra_data(self):
        extra_map = SecurityMap()
        user = uvcsite.getPrincipal()
        conf = get_plugin_configuration(name="securitysettings")
        if ICOUser.providedBy(user):
            if conf.get('canView', False) is True:
                if user.id == self.context.principal.id:
                    extra_map.addCell('uvc.CoUser', user.id, Allow)
                    uvcsite.log("SETTING CO USER FOR %s %s" %(self.context.__name__, user.id))
                else:
                    uvcsite.log("DENY CO USER FOR %s in %s " % (
                        user.id, self.context.__name__))
                    extra_map.addCell('uvc.Editor', user.id, Deny)
        return extra_map

