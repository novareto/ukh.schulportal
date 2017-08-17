# -*- coding: utf-8 -*-
# Copyright (c) 2007-2013 NovaReto GmbH
# cklinger@novareto.de

import grok

from zope import schema, interface
from zope.interface import directlyProvides
from uvc.configpanel import Configuration
from uvc.configpanel import IConfigurablePlugin
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IContextSourceBinder
from grokcore.component import provider

#
# Mitbenutzeransicht
#


class ISecuritySettings(interface.Interface):

    canView = schema.Bool(
        title=u"Ansicht für Mitbenutzer",
        description=u"Bitte klicken Sie hier falls Ihre\
            Mitbenutzer nur Ihre eigenen Dokumente sehen sollen"
    )


class HomefolderDisplayCoUserPlugin(grok.GlobalUtility):
    grok.name('securitysettings')
    grok.provides(IConfigurablePlugin)

    title = u"Ansichten Homefolder"
    description = u"Ansichten Homefolder"

    def __call__(self, *args, **kwargs):
        conf = Configuration(**kwargs)
        directlyProvides(conf, ISecuritySettings)
        return conf

    def getInterfaces(self):
        return [ISecuritySettings]

#
# Sortierungen für den Homefolder
#


@provider(IContextSourceBinder)
def getSortOn(context):
    return SimpleVocabulary((
        SimpleTerm('table-link-1', 'table-link-1', u'Titel'),
        SimpleTerm('table-state-3', 'table-state-3', u'Workflow Status'),
        SimpleTerm('table-modified-5', 'table-modified-5', u'Datum'),
        )
    )


@provider(IContextSourceBinder)
def getSortOrder(context):
    return SimpleVocabulary((
        SimpleTerm('ascending', 'ascending', u'Aufsteigend'),
        SimpleTerm('reverse', 'reverse', u'Absteigend')
        )
    )


class IFolderSorting(interface.Interface):

    sortOn = schema.Choice(
        title=u"Kriterium",
        description=u"Nach welchen Kriterium wollen Sie sortieren",
        source=getSortOn,
    )

    sortOrder = schema.Choice(
        title=u"Reihenfolge",
        source=getSortOrder,
    )


class HomefolderSortingPlugin(grok.GlobalUtility):
    grok.name('homefolder_sorting')
    grok.provides(IConfigurablePlugin)

    title = u"Sortierungen Homefolder"
    description = u"Sortierreihenfolge Homefolder"

    def __call__(self, *args, **kwargs):
        conf = Configuration(**kwargs)
        directlyProvides(conf, IFolderSorting)
        return conf

    def getInterfaces(self):
        return [IFolderSorting]
