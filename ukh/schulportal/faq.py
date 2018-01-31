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

FAQITEMS = (
    FAQ('Frage', 'Antwort', order=1),
    FAQ('FRAGE2', 'Antwort2', order=2)
)


class FAQView(uvcsite.Page):
    grok.context(uvcsite.IUVCSite)
    grok.name('faq')

    title = u"FAQ"
    description = u"Oft gestellte Fragen"

    items = FAQITEMS
