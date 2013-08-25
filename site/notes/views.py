from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse

from common.views import common_dict
from notes.models import MPNote, THNote

def table_by_name(name):
    if name == 'mp':
        return MPNote
    else:
        return THNote

def get_texts(table_name):
    table = table_by_name(table_name)
    return table.objects.all()

def get_text(table_name, id):
    table = table_by_name(table_name)
    return table.objects.get(id=id)

def four_colors(request):
    dict = common_dict()
    dict['ng_state_name'] = '{{state.name}}'
    dict['ng_name'] = '{{name}}'
    dict['ng_message'] = '{{message}}'
    dict['ng_coloring_color'] = '{{coloring.color}}'
    dict['ng_coloring_name'] = '{{coloring.name}}'
    dict['ng_isocode'] = '{{isocode}}'
    t = get_template('notes/four_colors.html')
    c = RequestContext(request, dict)
    return HttpResponse(t.render(c))

def metaphysics(request):
    dict = common_dict()
    dict['texts'] = get_texts('mp')
    t = get_template('notes/mp.html')
    c = RequestContext(request, dict)
    return HttpResponse(t.render(c))

def mp_note(request, num):
    dict = common_dict()
    dict['text'] = get_text('mp', num)
    t = get_template('notes/mp_note.html')
    c = RequestContext(request, dict)
    return HttpResponse(t.render(c))


def technology(request):
    dict = common_dict()
    dict['texts'] = get_texts('th')
    t = get_template('notes/th.html')
    c = RequestContext(request, dict)
    return HttpResponse(t.render(c))

def th_note(request, num):
    dict = common_dict()
    dict['text'] = get_text('th', num)
    t = get_template('notes/th_note.html')
    c = RequestContext(request, dict)
    return HttpResponse(t.render(c))
