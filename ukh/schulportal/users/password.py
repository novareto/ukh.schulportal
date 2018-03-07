# -*- coding: utf-8 -*-

import grok
import uvcsite

from zope.component import getUtility
from ukhtheme.grok.layout import ILayer
from uvcsite.extranetmembership.enms import ENMSCreateUser as BCU
from uvcsite.extranetmembership.enms import ChangePassword as BCP
from uvcsite.extranetmembership.interfaces import IUserManagement
from zope.securitypolicy.interfaces import IPrincipalRoleManager
from zope.app.homefolder.interfaces import IHomeFolder


class ENMSCreateUser(BCU):
    grok.layer(ILayer)
    description = u"Legen Sie hier einen Mitbenutzer an und vergeben Sie die jeweiligen Berechtigungen."

    @uvcsite.action(u"Anlegen")
    def anlegen(self):
        data, errors = self.extractData()
        if errors:
            self.flash('Es sind Fehler aufgetreten', type='error')
            return
        um = getUtility(IUserManagement)
        um.addUser(**data)
        # Setting Home Folder Rights
        for role in data.get('rollen'):
            principal_roles = IPrincipalRoleManager(self.context.__parent__[role])
            principal_roles.assignRoleToPrincipal('uvc.Editor', data.get('mnr'))
        self.flash(u"Vielen Dank! Sie haben einen Mitbenutzer-Account erstellt. Teilen Sie\
                     der Person bitte den Benutzernamen und das neue Passwort\
                     mit. Der Mitbenutzer sollte das Passwort bei der\
                     Erstanmeldung ändern.")
        principal = self.request.principal
        homeFolder = IHomeFolder(principal).homeFolder
        self.redirect(self.url(homeFolder, '++enms++'))


class ChangePassword(BCP):
    grok.layer(ILayer)

    @uvcsite.action(u"Bearbeiten")
    def changePasswort(self):
        data, errors = self.extractData()
        if errors:
            self.flash('Es sind Fehler aufgetreten', type='error')
            return
        um = getUtility(IUserManagement)
        principal = self.request.principal.id
        data['mnr'] = principal
        um.updatePasswort(**data)
        self.flash(u'Ihr Passwort wurde gespeichert!')
        self.redirect(self.application_url())

    @uvcsite.action(u'Abbrechen')
    def handle_cancel(self):
        self.flash(u'Abbruch!')
        self.redirect(self.application_url())
