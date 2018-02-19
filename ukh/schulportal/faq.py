# -*- coding: utf-8 -*-

import grok
import uvcsite


grok.templatedir('templates')


class FAQ(object):

    def __init__(self, q, a, order):
        self.question = q
        self.answer = a
        self.order = order

    def __repr__(self):
        return "<FAQ ITEM>"


HK7 = u"""
<h2>K7: Schulen (nur Lehrkräfte)</h2>
<h4><u>Lehrkräfte:</u></h4>
<p>Bitte tragen Sie die Zahl der Lehrkräfte ein, die an der Schule und ggf. an den Außenstellen der Schule tätig sind.
   Wir übernehmen Lehrgangsgebühren für die Teilnahme an</p>
<p>-  Erste-Hilfe-Fortbildungen im Sinne des DGUV Grundsatzes 304-001</p>
<p>-  Erste-Hilfe-Fortbildungen Schule</p>
<p>für 15 % des gesamten Kollegiums in einem Zeitraum von 2 Jahren.</p>
<p>Hinweis: Bitte zählen Sie Personal in anderen Bereichen, bspw. in der Schulbetreuung, Reinigung,
   Sekretariat oder Hausmeister nicht mit. Für dieses Personal beantragt der Arbeitgeber die Kostenübernahme
   der Lehrgangsgebühren bei der zuständigen Fach-Berufsgenossenschaft oder bei uns als Mitgliedsunternehmen.</p>
<p>Felder mit <b>*</b> sind Pflichtfelder, diese müssen gefüllt werden.</p>
"""




FAQITEMS_EH = (
    FAQ(u'Woher bekomme ich die Zugangsdaten zum Erste-Hilfe-Onlineverfahren?',
        u'Die Zugangsberechtigungen zur Antragstellung im jeweiligen Portal wurden \
        im November 2016 versendet. Bitte informieren Sie sich daher ggf. in Ihrem Betrieb, \
        wer für Ihren Bereich den Antrag zur Kostenübernahme stellt und die Zugangsdaten \
        hierfür erhalten hat. Bei der Erstanmeldung werden von jeder Antragstellerin und \
        jedem Antragsteller Kontaktdaten abgefragt. Somit gibt es pro Mitgliedsbetrieb \
        bzw. pro Schule nur einen festen Antragsteller. Ausnahmen sind Großstädte \
        und einige Landesbetriebe. Schulen erreichen das Erste-Hilfe-Onlineverfahren \
        über den Zugang zum Schulportal. \
        Liegen Ihrem Betrieb/Ihrer Schule keine Zugangsdaten vor, \
        kontaktieren Sie unser Servicetelefon unter 069 29972-440 \
        oder senden Sie uns eine E-Mail an Portal-Erste-Hilfe[at]ukh.de. \
        Bitte haben Sie Verständnis, dass wir zum Schutz der Betriebe und Schulen \
        grundsätzlich keine Zugangsdaten an private E-Mail-Adressen versenden. \
        Da es sich um einen geschützten Zugang (Benutzername und Passwort) handelt, \
        können die jeweiligen Zugangsdaten nur an die offizielle E-Mail-Adresse der Schule \
        oder den uns mitgeteilten Ansprechpartner des Betriebes versendet werden.',
        order=1),
    FAQ(u'Kontingent 7 – Erste Hilfe in Schulen',
        u'Müssen die Berechtigungsscheine bestimmten Fachlehrkräften übergeben werden? \
        Nein. Über die Verteilung der Berechtigungsscheine entscheidet jede Schule individuell, \
        abhängig vom bestehenden Bedarf. \
        An Ihrer Schule sind regelmäßig Integrationshelfer eingesetzt, die beim Schulträger \
        (nicht bei einem Sonder- oder /Heilpädagogischen Dienst oder im Rahmen des Elternarbeitgebermodells) \
        beschäftigt sind und die Sie gerne zum Ersthelfer aus- oder fortbilden möchten? \
        Eine Beantragung ist grundsätzlich durch die Schule oder den Schulträger möglich. \
        Sofern Sie als Schule beantragen möchten, berücksichtigen Sie die Anzahl der regelmäßig \
        eingesetzten Integrationshelfer bitte in Kontingent 7. Wichtig ist, dass keine Doppelbeantragung erfolgt. \
        Daher stimmen Sie sich bitte unbedingt mit Ihrem Schulträger ab, \
        wer sich um die Beantragung der Berechtigungsscheine für Integrationshelfer kümmert. \
        Etwaig zu Unrecht erhaltene Leistungen sind uns in Höhe der entstandenen Kosten zu erstatten.',
        order=2),
    FAQ(u'Kontingent 9 – Schulbetreuung',
        u'Wir sind eine Einrichtung zur Schülerbetreuung. Übernimmt die UKH auch für uns die Kosten für Erste-Hilfe-Lehrgänge? \
        Wir übernehmen Erste-Hilfe-Lehrgangsgebühren, sofern die Schüler*innen während des Besuchs \
        der Betreuung gesetzlich unfallversichert sind.',
        order=3),
    FAQ(u'Kontingent 9 – Schulbetreuung',
        HK7,
        order=4),
)





UAZ01 = u"""
<p>Die Anzeige ist zu erstatten, wenn ein Arbeitsunfall oder ein Wegeunfall</p>
<p>(z. B. Unfall auf dem Weg zwischen Wohnung und Arbeitsstätte)</p>
<p>eine Arbeitsunfähigkeit von mehr als 3 Kalendertagen oder den Tod eines Versicherten zur Folge hat.</p>
"""

UAZ02 = u"""
<p>Anzeigepflichtig ist der Unternehmer oder sein Bevollmächtigter.</p>
<p>Bevollmächtigte sind Personen, die vom Unternehmer zur Erstattung der Anzeige beauftragt sind.</p>
"""

UAZ03 = u"""
<p>Aufgrund der elektronischen Übermittlung erreicht die Unfallanzeige direkt die in der
   Unfallkasse Hessen</p>
<p>zuständige Fachabteilung zur weiteren Bearbeitung.</p>
"""

UAZ04 = u"""
<p>Unterliegt das Unternehmen der allgemeinen Arbeitsschutzaufsicht</p>
<p>(bei landwirtschaftlichen Unternehmen nur soweit sie Arbeitnehmer beschäftigen),</p>
<p>ist ein Exemplar an die für den Arbeitsschutz zuständige Landesbehörde</p>
<p>(z.B. Gewerbeaufsichtsamt, Staatliches Amt für den Arbeitsschutz) zu senden.</p>
<p>Unterliegt das Unternehmen der bergbehördlichen Aufsicht, erhält die zuständige untere Bergbehörde ein Exemplar.</p>
"""

UAZ05 = u"""
<p>Versicherte, für die eine Anzeige erstattet wird, sind auf ihr Recht hinzuweisen, dass sie eine Kopie der Anzeige verlangen können.</p>
<p>Fachkraft für Arbeitssicherheit und Betriebsarzt sind durch den Unternehmer oder seinen Bevollmächtigten zu informieren.</p>
<p>Da die Unfallanzeige durch Datenübermittlung erstattet wird, muss vor der Absendung ein Mitglied
   des Betriebs- oder Personalrats davon in Kenntnis gesetzt werden.</p>
"""

UAZ06 = u"""
<p>Die Unfallanzeige ist grundsätzlich nur über das Mitgliederportal der UKH auf elektronischem Wege zu übermitteln.</p>
<p>Der Versand per Post ist nur noch ausnahmsweise, z.B. bei Systemausfall, zulässig.</p>
"""

UAZ07 = u"""
<p>Der Unternehmer oder sein Bevollmächtigter hat die Anzeige binnen drei Tagen zu erstatten,
   nachdem er von dem Unfall Kenntnis erhalten hat.</p>
"""

UAZ08 = u"""
<p><b>Tödliche Unfälle, Massenunfälle und Unfälle mit schwerwiegenden Gesundheitsschäden</b> sind sofort</p>
<p>der Unfallkasse Hessen telefonisch unter 069/29972-440 oder per Mail ukh@ukh.de zu melden.</p>
<br>
<p>Unterliegt das Unternehmen der allgemeinen Arbeitsschutzaufsicht ist ebenfalls die für den Arbeitsschutz zuständige Landesbehörde</p>
<p>(z.B. Gewerbeaufsichtsamt, Staatliches Amt für den Arbeitsschutz) umgehend zu unterrichten.</p>
<p>Unterliegt das Unternehmen der bergbehördlichen Aufsicht, ist zusätzlich die zuständige Bergbehörde zu informieren.</p>
"""

FAQITEMS_UAZ = (
    FAQ(u'Wann ist eine Unfallanzeige zu erstatten?', UAZ01, order=1),
    FAQ(u'Wer hat die Unfallanzeige zu erstatten?', UAZ02, order=2),
    FAQ(u'Wer erhält die Unfallanzeige bei der elektronischen Übermittlung?', UAZ03, order=3),
    FAQ(u'Sind weitere Exemplare der Unfallanzeige erforderlich?', UAZ04, order=4),
    FAQ(u'Wer ist von der Unfallanzeige zu informieren?', UAZ05, order=5),
    FAQ(u'Wie ist die Unfallanzeige zu erstatten?', UAZ06, order=6),
    FAQ(u'Innerhalb welcher Frist ist die Unfallanzeige zu erstatten?', UAZ07, order=7),
    FAQ(u'Was ist bei schweren Unfällen, Massenunfällen und Todesfällen zu beachten?', UAZ08, order=8)
)


class FAQEHView(uvcsite.Page):
    grok.context(uvcsite.IUVCSite)
    grok.name('faqeh')
    title = u"FAQ"
    description = u"Fragen und Antworten zum Erste Hilfe Onlineverfahren"
    items = FAQITEMS_EH


class FAQUAZView(uvcsite.Page):
    grok.context(uvcsite.IUVCSite)
    grok.name('faquaz')
    title = u"FAQ"
    description = u"Häufig gestellte Fragen zur Unfallanzeige"
    items = FAQITEMS_UAZ
