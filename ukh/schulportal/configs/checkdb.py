 # -*- coding: utf-8 -*-

import grok

from z3c.saconfig import Session
from zope.interface import Interface
from configs.database_setup import users


class CheckDatabaseConnectivity(grok.View):
    grok.context(Interface)
    grok.name('checkdb')
    grok.require('zope.Public')

    def render(self):
        session = Session()
        return str(session.query(users).count())
