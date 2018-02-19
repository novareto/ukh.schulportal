import grok
import uvcsite

from .interfaces import IStammdaten
from zeam.form.base import DictDataManager
from uvcsite.extranetmembership.interfaces import IUserManagement
from zope.component import getUtility


class StammdatenMenu(uvcsite.MenuItem):
    grok.context(uvcsite.IMyHomeFolder)
    grok.title(u'Meine Daten')
    grok.viewletmanager(uvcsite.IPersonalMenu)

    @property
    def action(self):
        return self.view.url(self.context, 'stammdaten')


class Stammdaten(uvcsite.Form):
    grok.context(uvcsite.IMyHomeFolder)
    grok.name(u'stammdaten')
    grok.title(u'Meine Daten')
    grok.require('zope.View')
    dataManager = DictDataManager

    label = u"Meine Daten"
    description = u"Um die Kommunikation mit Ihnen zu vereinfachen,\
                    bitten wir Sie um Ihre Kontaktdaten."
    fields = uvcsite.Fields(IStammdaten)
    ignoreContent = False
    fields['titel'].htmlAttributes['maxlength'] = 50
    fields['vname'].htmlAttributes['maxlength'] = 50
    fields['nname'].htmlAttributes['maxlength'] = 50
    fields['funktion'].htmlAttributes['maxlength'] = 50
    fields['email'].htmlAttributes['maxlength'] = 70
    fields['vwhl'].htmlAttributes['maxlength'] = 20
    fields['tlnr'].htmlAttributes['maxlength'] = 20

    def __init__(self, context, request):
        super(Stammdaten, self).__init__(context, request)
        um = getUtility(IUserManagement)
        user = um.getUser(self.request.principal.id)
        self.setContentData(user)

    @uvcsite.action(u'Speichern')
    def handle_save(self):
        data, errors = self.extractData()
        if errors:
            self.flash('Es sind Fehler aufgetreten.')
            return
        um = getUtility(IUserManagement)
        um.updUserStamm(**data)
        self.flash('Ihre Daten wurden gespeichert.')
        self.redirect(self.application_url())

    @uvcsite.action(u'Abbrechen')
    def handle_cancel(self):
        self.flash('Die Aktion wurde abgebrochen.')
        self.redirect(self.application_url())
