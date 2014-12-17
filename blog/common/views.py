from common.context import generate_context

from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse

#######################################################################################

def welcome(request):
    t = get_template('welcome.html')
    c = RequestContext(request, {})

    return HttpResponse(t.render(c))

def entry(request, name):
    dict = generate_context(name)
    t = get_template('entries/' + name + '.html')
    c = RequestContext(request, dict)

    return HttpResponse(t.render(c))
