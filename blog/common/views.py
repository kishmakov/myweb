from common.context import entry_context, list_context

from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseNotFound

#######################################################################################

def list_view(request, section=0, tag=''):
    t = get_template('list_base.html')
    context = list_context(section, tag)

    if context is None:
        msg = '<p>Nothing found for tag "' + tag + '"</p>'
        msg += '<p><a href="/">Take me back</a>.</p>'
        return HttpResponseNotFound(msg)

    c = RequestContext(request, context)

    return HttpResponse(t.render(c))

def entry_view(request, name):
    t = get_template('entries/' + name + '.html')
    c = RequestContext(request, entry_context(name))

    return HttpResponse(t.render(c))
