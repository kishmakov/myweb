from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse
from django.db.models import Q

from common.views import common_dict
from notes.models import Notes

def get_texts(section):
    return Notes.objects.filter(section=section)

def get_text(id):
    print "is is {0}".format(id)
    return Notes.objects.get(id=id)

def metaphysics(request):
    dict = common_dict()
    dict['texts'] = get_texts('mp')
    t = get_template('notes/mp.html')
    c = RequestContext(request, dict)
    return HttpResponse(t.render(c))

def mp_note(request, num):
    dict = common_dict()
    dict['text'] = get_text(num)
    t = get_template('notes/mp_note.html')
    c = RequestContext(request, dict)
    return HttpResponse(t.render(c))


def technology(request):
    dict = common_dict()
    dict['texts'] = get_texts(u'th')
    t = get_template('notes/th.html')
    c = RequestContext(request, dict)
    return HttpResponse(t.render(c))
