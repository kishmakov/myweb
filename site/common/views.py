from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse

from settings import STATIC_URL, SITE_URL

#######################################################################################

def common_dict():
    return {
        'site_url' : SITE_URL,
        'static_url': STATIC_URL
    }

def welcome(request):
    dict = common_dict()
    t = get_template('welcome.html')
    c = RequestContext(request, dict)
    return HttpResponse(t.render(c))
