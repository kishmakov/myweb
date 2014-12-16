from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse

#######################################################################################

def common_dict():
    return {}

def welcome(request):
    dict = common_dict()
    t = get_template('welcome.html')
    c = RequestContext(request, dict)

    return HttpResponse(t.render(c))

def entry(request, name):
    dict = common_dict()
    t = get_template('entries/' + name + '.html')
    c = RequestContext(request, dict)

    return HttpResponse(t.render(c))
