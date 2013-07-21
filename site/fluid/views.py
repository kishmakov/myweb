from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse

from common.views import common_dict
from fluid.models import Chapter, Section, Subsection

def get_chapters():
    return Chapter.objects.all()

def get_subsection(num):
    return Subsection.objects.get(id=num)

def get_section(num):
    section = Section.objects.get(id=num)
    sub_nums = section.subnodes.split()
    subs = []
    for sn in sub_nums:
        subs.append(get_subsection(sn))

    return {'title': section.title,
            'subsections': subs}

def get_chapter(num):
    chapter = Chapter.objects.get(id=num)
    sections_nums = chapter.subnodes.split()
    sections = []
    for sn in sections_nums:
        sections.append(get_section(sn))
    return {'title': chapter.title,
            'keywords': 'buzz buzz buzz',
            'sections': sections}

def index(request):
    dict = common_dict()
    dict['topics'] = get_chapters()
    t = get_template('fluid/index.html')
    c = RequestContext(request, dict)
    return HttpResponse(t.render(c))

def note(request, num):
    dict = common_dict()
    dict['chapter'] = get_chapter(num)
    t = get_template('fluid/note.html')
    c = RequestContext(request, dict)
    return HttpResponse(t.render(c))