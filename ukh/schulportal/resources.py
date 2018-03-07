# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2011 NovaReto GmbH

import grok

from js.jquery import jquery
from fanstatic import Library, Resource
from uvc.widgets import masked_input


library = Library('ukh.schulportal', 'static')
ukhcss = Resource(library, 'ukh.css', bottom=True)
ukhjs = Resource(library, 'main.js', depends=[jquery], bottom=True)
taxicss = Resource(library, 'taxigutscheine.css', bottom=True)
taxijs = Resource(library, 'taxigutscheine.js', depends=[masked_input], bottom=True)
