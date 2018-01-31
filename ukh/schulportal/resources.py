# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2011 NovaReto GmbH

import grok

from js.jquery import jquery
from fanstatic import Library, Resource

library = Library('ukh.schulportal', 'static')
ukhcss = Resource(library, 'ukh.css', bottom=True)
ukhjs = Resource(library, 'main.js', depends=[jquery], bottom=True)
