# -*- coding: utf-8 -*-
# Copyright (c) 2007-2013 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite


grok.templatedir('templates')


class LandingPage(uvcsite.Page):
    grok.context(uvcsite.IUVCSite)
    grok.name('index')

    def update(self):
        import pdb; pdb.set_trace() 
