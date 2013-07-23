from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse

from common.views import common_dict
from fluid.models import Chapter, Section, Subsection
from fluid.models import Link, Other, Paper, DataPaper, Book

def get_link_table(letter):
    if letter == 'o':
        return Other
    elif letter == 'b':
        return Book
    elif letter == 'p':
        return Paper
    elif letter == 'l':
        return Link
    else:
        return DataPaper

def get_chapters():
    return Chapter.objects.all()

def get_subsection(num):
    if num == '0':
        return {}
    return Subsection.objects.get(id=num)

def get_section(num):
    section = Section.objects.get(id=num)
    sub_nums = section.subnodes.split()
    subs = []
    for sn in sub_nums:
        subs.append(get_subsection(sn))

    return {
        'title': section.title,
        'subsections': subs
    }

def get_sections(nums):
    sections = []
    for num in nums:
        sections.append(get_section(num))

    return sections

def get_reference(num):
    num_letter = num[0]
    num_number = num[1:]
    table = get_link_table(num_letter)
    entry = table.objects.get(id=num_number)

    reference = {
        'title': entry.title,
        'link': entry.link,
        'description': entry.description
    }

    if hasattr(entry, 'authors'):
        reference['authors'] = entry.authors

    if hasattr(entry, 'year'):
        reference['year'] = entry.year

    if hasattr(entry, 'journal'):
        reference['journal'] = entry.journal

    if hasattr(entry, 'doi'):
        reference['doi'] = entry.doi

    if hasattr(entry, 'publisher'):
        reference['publisher'] = entry.publisher

    if hasattr(entry, 'isbn'):
        reference['isbn'] = entry.isbn

    return reference

def get_references(nums):
    references = []
    for num in nums:
        references.append(get_reference(num))

    return references

def get_chapter(num):
    chapter = Chapter.objects.get(id=num)
    return {
        'title': chapter.title,
        'keywords': chapter.keywords,
        'sections': get_sections(chapter.subnodes.split()),
        'references': get_references(chapter.references.split())
    }

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

def notations(request):
    dict = common_dict()
    t = get_template('fluid/notations.html')
    c = RequestContext(request, dict)
    return HttpResponse(t.render(c))

def get_books():
    return Book.objects.all()

def get_papers():
    return Paper.objects.all()

def get_data_papers():
    return DataPaper.objects.all()

def get_others():
    return Other.objects.all()

def get_links():
    return Link.objects.all()

def references(request):
    dict = common_dict()
    dict['books'] = get_books()
    dict['papers'] = get_papers()
    dict['others'] = get_others()
    t = get_template('fluid/references.html')
    c = RequestContext(request, dict)
    return HttpResponse(t.render(c))

def data_papers(request):
    dict = common_dict()
    dict['data_papers'] = get_data_papers()
    t = get_template('fluid/data_papers.html')
    c = RequestContext(request, dict)
    return HttpResponse(t.render(c))

def links(request):
    dict = common_dict()
    dict['links'] = get_links()
    t = get_template('fluid/links.html')
    c = RequestContext(request, dict)
    return HttpResponse(t.render(c))