from common.list_tools import search_ids, search_tags
from common.entry_tools import descriptions
from common.references import references

SCRIPT_PREFIX = '<script src="'
SCRIPT_SUFFIX = '" type="text/javascript"></script>'
STYLE_PREFIX = '<link href="'
STYLE_SUFFIX = '" rel="stylesheet" type="text/css">'

SH_CDN = 'http://cdnjs.cloudflare.com/ajax/libs/SyntaxHighlighter/3.0.83/'

SH_CSS = STYLE_PREFIX + SH_CDN + 'styles/shCore.css' + STYLE_SUFFIX
SH_CSS_DEF = STYLE_PREFIX + SH_CDN + 'styles/shThemeDefault.css' + STYLE_SUFFIX
SH_JS = SCRIPT_PREFIX + SH_CDN + 'scripts/shCore.js' + SCRIPT_SUFFIX
SH_JS_KICK = '<script type="text/javascript">SyntaxHighlighter.all()</script>'
SH_JS_CPP = SCRIPT_PREFIX + SH_CDN + 'scripts/shBrushCpp.js' + SCRIPT_SUFFIX
SH_JS_PYTHON = SCRIPT_PREFIX + SH_CDN + 'scripts/shBrushPython.js' + SCRIPT_SUFFIX

MJ_CDN = 'http://cdn.mathjax.org/mathjax/'

MJ_JS_KICK = '<script type="text/x-mathjax-config">MathJax.Hub.Config({ TeX: { equationNumbers: { autoNumber: "AMS" } } });</script>'
MJ_JS = SCRIPT_PREFIX + MJ_CDN + 'latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML' + SCRIPT_SUFFIX

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
        'tags': ['c++', 'haskell', 'python'],
        'resources': [SH_CSS, SH_CSS_DEF, SH_JS, SH_JS_KICK]
    },
    {
        'tags': ['mathjax'],
        'resources': [MJ_JS_KICK]
    }
]

tag_to_resources = {
    'c++' : [SH_JS_CPP],
    'mathjax': [MJ_JS],
    'python': [SH_JS_PYTHON],
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

    ref = {}
    ref_id_count = 0

    for rtag in rtags:
        ref_id_count += 1
        ref_type, ref_id = rtag.split(' ')
        if ref_type not in ref:
            ref[ref_type] = {}

        ref[ref_type][ref_id] = {
            'id': ref_id_count,
            'title': references[ref_type][ref_id]['title']
        }

    return {
        'tags': [split_tag(tag, '') for tag in descriptions[id]['navi_tags']],
        'resources': resources,
        'header': descriptions[id]['header'],
        'ref': ref
    }

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