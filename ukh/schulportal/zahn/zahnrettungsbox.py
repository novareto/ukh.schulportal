# -*- coding: utf-8 -*-

import grok
import uvcsite
import zope.component

from zope.interface import Interface
from zope import schema
from ukh.schulportal.resources import zahnjs
from zeam.form.base import NO_VALUE, Error
from time import strptime

grok.templatedir('templates')


KEY = "zahnrettung"


MT = u"""Sehr geehrte Damen Und Herren,

wir benötigen Ersatz für unsere Zahnrettungsbox.

Adresse:

%s

%s
%s


Ansprechpartner:

%s
%s
%s


Unfalltag:

%s


Zahnverletzung:

%s



Diese Nachricht wurde über das Schulportal der Unfallkasse Hessen versendet.
"""


class IZahnrettungsBox(Interface):
    adrname1 = schema.TextLine(title=u'-',)
    adrname2 = schema.TextLine(title=u'-',)
    adrname3 = schema.TextLine(title=u'-',)
    anspname1 = schema.TextLine(title=u'-',)
    anspname2 = schema.TextLine(title=u'-',)
    anspname3 = schema.TextLine(title=u'-',)
    unfalltag = schema.TextLine(title=u'Tag des Unfalls *',)
    verletzung = schema.TextLine(title=u'Zahn komplett ausgeschlagen (Avulsion) oder nur ein Stück abgebrochen (Fraktur) oder sonstige Verletzung *',)


class ZahnrettungsboxInfo(uvcsite.Form):
    grok.context(Interface)
    grok.name('zahnrettungsbox')
    label = u"Zahnrettungsbox"

    @uvcsite.action('Abbrechen')
    def handle_cancel(self):
        self.flash(u'Die Aktion wurde abgebrochen.')
        self.redirect(self.application_url())

    @uvcsite.action('Zahnrettungsbox anfordern')
    def handle_send(self):
        self.redirect(self.url(self.context, 'zahnrettungsboxview'))


class ZahnrettungsBoxView(uvcsite.Form):
    grok.implements(IZahnrettungsBox)
    grok.context(Interface)
    grok.name('zahnrettungsboxview')
    label = u"Zahnrettungsbox"

    @property
    def fields(self):
        adr = self.request.principal.getAdresse()
        fields = uvcsite.Fields(IZahnrettungsBox)
        fields['adrname1'].defaultValue = adr['iknam1'].strip() + ' ' + adr['iknam2'].strip() + ' ' + adr['iknam3'].strip()
        fields['adrname2'].defaultValue = adr['ikstr'].strip() + ' ' + str(adr['ikhnr']).strip()
        fields['adrname3'].defaultValue = str(adr['ikhplz']).strip() + ' ' + adr['ikhort'].strip()
        fields['adrname1'].mode = "hiddendisplay"
        fields['adrname2'].mode = "hiddendisplay"
        fields['adrname3'].mode = "hiddendisplay"
        fields['anspname1'].defaultValue = adr['anr'].strip() + ' ' + adr['vname'].strip() + ' ' + adr['nname'].strip()
        fields['anspname2'].defaultValue = adr['vwhl'] + ' ' + adr['tlnr']
        fields['anspname3'].defaultValue = adr['email'].strip()
        fields['anspname1'].mode = "hiddendisplay"
        fields['anspname2'].mode = "hiddendisplay"
        fields['anspname3'].mode = "hiddendisplay"
        return fields

    def update(self):
        zahnjs.need()

    @property
    def macros(self):
        return zope.component.getMultiAdapter(
            (self.context, self.request),
            name='fieldmacros'
        ).template.macros

    @uvcsite.action('Abbrechen')
    def handle_cancel(self):
        self.flash(u'Die Aktion wurde abgebrochen.')
        self.redirect(self.application_url())

    @uvcsite.action('Zahnrettungsbox anfordern')
    def handle_send(self):
        data, errors = self.extractData()
        if errors:
            return


        um = self.request.principal.getUM()
        acu = um.getUser(self.request.principal.id)
        adr = self.request.principal.getAdresse()
        from uvcsite.utils.mail import send_mail
        print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
        print acu
        print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
        print adr
        print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
        adrname = adr['iknam1'].strip() + ' ' + adr['iknam2'].strip() + ' ' + adr['iknam3'].strip()
        adrstrasse = adr['ikstr'].strip() + ' ' + str(adr['ikhnr']).strip()
        adrplzort = str(adr['ikhplz']).strip() + ' ' + adr['ikhort'].strip()
        acuname = acu['vname'].strip() + ' ' + acu['nname'].strip()
        acutel = acu['vwhl'].strip() + ' ' + acu['tlnr'].strip()
        acumail = acu['email'].strip()
        text = MT % (adrname, adrstrasse, adrplzort, acuname, acutel, acumail, data['unfalltag'], data['verletzung'])
        send_mail('extranet@ukh.de', ('m.seibert@ukh.de', 'seibim@web.de', acu['email'],), u"Bestellung Zahnrettungsbox", body=text)
        self.flash(u'Ihre Nachricht wurde an "info@zahnrettungskonzept.info" gesendet, eine Kopie ging an Ihre E-Mailadresse.')
        self.redirect(self.application_url())

    def validateData(self, fields, data):
        errors = super(ZahnrettungsBoxView, self).validateData(fields, data)
        for x in [['verletzung', u'Zahnverletzung']]:
            if data.get(x[0]) == NO_VALUE or data.get(x[0]) == '':
                t1 = u'Fehler im Feld " '
                t2 = x[1]
                t3 = u' " Das Feld darf nicht leer sein, bitte geben Sie einen Text ein.'
                errors.append(Error(u'Fehler!!!'))
                self.flash(t1 + t2 + t3)
        for x in [['unfalltag', u'Tag des Unfalls']]:
            if data.get(x[0]) == NO_VALUE or data.get(x[0]) == '':
                t1 = u'Fehler im Feld " '
                t2 = x[1]
                t3 = u' " Das Feld darf nicht leer sein, bitte geben Sie ein Datum ein.'
                errors.append(Error(u'Fehler!!!'))
                self.flash(t1 + t2 + t3)
        ######################################################################
        # CHECK Datum                                                        #
        ######################################################################
        for x in [['unfalltag', u'Tag des Unfalls']]:
            if data.get(x[0]) != NO_VALUE and data.get(x[0]) != '':
                d = False
                try:
                    strptime(data.get(x[0]), "%d.%m.%Y")
                    d = True
                except ValueError:
                    t1 = u'Fehler im Feld " '
                    t2 = x[1]
                    t3 = u' " Das Datum hat einen Fehler. Bitte überprüfen Sie das Datum!'
                    errors.append(Error(u'Fehler!!!'))
                    self.flash(t1 + t2 + t3)
                if d is True:
                    j = data.get(x[0])[6:8]
                    if j < '19' or j > '20':
                        t1 = u'Fehler im Feld " '
                        t2 = x[1]
                        t3 = u' " Die Jahreszahl ist falsch! Bitte ändern Sie das Datum.'
                        errors.append(Error(u'Fehler!!!'))
                        self.flash(t1 + t2 + t3)
        return errors
