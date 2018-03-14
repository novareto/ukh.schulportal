# -*- coding: utf-8 -*-
import grok
import uvcsite

from zope.interface import Interface


grok.templatedir('templates')


class VideoView(uvcsite.Page):
    grok.context(Interface)
    grok.name('videoview')
