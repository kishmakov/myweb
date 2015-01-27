from common.list_tools import search_ids, search_tags
from common.entry_tools import descriptions
from common.references import references

def script(src, code, type='text/javascript'):
    result = '<script type="' + type + '"'
    if len(src) > 0:
        result += ' src="' + src + '"'
    return result + '>' + code + '</script>'

STYLE_PREFIX = '<link href="'
STYLE_SUFFIX = '" rel="stylesheet" type="text/css">'

SH_CDN = 'http://cdnjs.cloudflare.com/ajax/libs/SyntaxHighlighter/3.0.83/'
MJ_CDN = 'http://cdn.mathjax.org/mathjax/'

SH_CSS = STYLE_PREFIX + SH_CDN + 'styles/shCore.css' + STYLE_SUFFIX
SH_CSS_DEF = STYLE_PREFIX + SH_CDN + 'styles/shThemeDefault.css' + STYLE_SUFFIX

SH_JS = script(SH_CDN + 'scripts/shCore.js', '')
SH_JS_KICK = script('', 'SyntaxHighlighter.all()')

SH_JS_CPP = script(SH_CDN + 'scripts/shBrushCpp.js', '')
SH_JS_JS = script(SH_CDN + 'scripts/shBrushJScript.js', '')
SH_JS_PYTHON = script(SH_CDN + 'scripts/shBrushPython.js', '')
SH_JS_XML = script(SH_CDN + 'scripts/shBrushXml.js', '')

MJ_JS_KICK = script('', 'MathJax.Hub.Config({ TeX: { equationNumbers: { autoNumber: "AMS" } } });', 'text/x-mathjax-config')
MJ_JS = script(MJ_CDN + 'latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML', '')

def provide_ids(section_index, tag):
    per_page = 7

    if tag != '' and tag not in search_tags:
        return None, None, None, None

    amount = len(search_ids) if tag == '' else len(search_tags[tag])
    sections_number = ((amount - 1) // per_page) + 1
    section_index = max(1, min(int(section_index), sections_number))

    first_id = per_page * (section_index - 1)
    last_id = min(amount, first_id + per_page)

    ids = []

    for i in range(first_id, last_id):
        ids.append(search_ids[i if tag == '' else search_tags[tag][i]])

    return ids, sections_number, section_index, sorted(search_tags)

def split_tag(tag, active_tag):
    return {
        'link': tag.replace(' ', '_'),
        'visible': tag,
        'active': tag != active_tag
    }


### interface functions ###

tag_to_init = [
    {
        'tags': ['cpp', 'haskell', 'js', 'python', 'xml'],
        'resources': [SH_CSS, SH_CSS_DEF, SH_JS, SH_JS_KICK]
    },
    {
        'tags': ['mathjax'],
        'resources': [MJ_JS_KICK]
    }
]

tag_to_resources = {
    'cpp' : [SH_JS_CPP],
    'js': [SH_JS_JS],
    'mathjax': [MJ_JS],
    'python': [SH_JS_PYTHON],
    'xml': [SH_JS_XML],
}

def entry_context(id):
    resources = []
    stags = descriptions[id]['syntax_tags']
    rtags = descriptions[id]['ref_tags']

    for stag in stags:
        for init in tag_to_init:
            if init['tags'].count(stag) > 0:
                resources.extend(init['resources'])

    for stag in stags:
        if stag not in tag_to_resources:
            continue

        resources.extend(tag_to_resources[stag])

    result = {
        'tags': [split_tag(tag, '') for tag in descriptions[id]['navi_tags']],
        'resources': resources,
        'header': descriptions[id]['header'],
    }

    ref = {}
    ordered_ref = []

    ref_id_count = 0

    for rtag in rtags:
        ref_id_count += 1
        ref_type, ref_id = rtag.split(' ')
        if ref_type not in ref:
            ref[ref_type] = {}

        item = {
            'id': ref_id_count,
            'title': references[ref_type][ref_id]['title']
        }

        ref[ref_type][ref_id] = item

        item['cite_ref'] = '#cite_ref-{0}'.format(ref_id_count)
        item['cite_note'] = 'cite_note-{0}'.format(ref_id_count)

        ordered_ref.append(item)

    if len(ordered_ref) > 0:
        result['ref'] = ref
        result['ordered_ref'] = ordered_ref

    return result

def list_context(section_id, tag):
    original_tag = tag.replace('_', ' ')
    ids, sections, section_index, tags = provide_ids(section_id, original_tag)

    if ids is None:
        return None

    result = {
        'descriptions': [],
        'sections_before': [i for i in range(1, section_index)],
        'section': section_index,
        'sections_after': [i + 1 for i in range(section_index, sections)],
        'tag': original_tag,
        'tags': [split_tag(tag, original_tag) for tag in tags]
    }

    for id in ids:
        desc = {}
        for key, value in descriptions[id].items():
            if key == 'syntax_tags':
                continue

            if key == 'navi_tags':
                desc[key] = [split_tag(tag, original_tag) for tag in value]
                continue

            desc[key] = value

        result['descriptions'].append(desc)

    return result