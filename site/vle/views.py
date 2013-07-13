from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse
from django.utils import simplejson
from django.db.models import Q

from common.views import common_dict

from models import SimpleFluid


def parse_request(request):
    dict = {}
    if request.method == 'GET':
        dict['query'] = request.GET.get('query', '')
        if dict['query'] == 'string':
            dict['string'] = request.GET.get('string', '')
        if dict['query'] == 'number':
            dict['number'] = request.GET.get('number', '')

    return dict

def data_base(request):
    dict = parse_request(request)
    fluids = []
    detailed = False
    if dict['query'] == 'string':
        string = dict['string']
        qname = Q(name__icontains=string)
        qnum = Q(cas_num__icontains=string)
        fluids = SimpleFluid.objects.filter(qname|qnum)[0:9]
    elif dict['query'] == 'number':
        detailed = True
        number = dict['number']
        fluid = SimpleFluid.objects.get(cas_num=number)
        fluids.append(fluid)
    else:
        fluids = SimpleFluid.objects.all()[0:9]

    lines = []

    for fluid in fluids:
        description = {
            'name' : fluid.name,
            'number' : fluid.cas_num,
            'formula' : fluid.formula
        }

        if detailed:
            description['tc'] = fluid.tc
            description['pc'] = fluid.pc
            description['vc'] = fluid.vc
            description['omega'] = fluid.omega

        lines.append(description)

    data = simplejson.dumps(lines)

    return HttpResponse(data, mimetype='application/json')

def gui(request):
    dict = common_dict()
    t = get_template('vle/pr.html')
    c = RequestContext(request, dict)
    return HttpResponse(t.render(c))


