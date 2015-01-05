from common.list_tools import search_ids, search_tags
from common.entry_tools import descriptions

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

MJ_CDN = 'http://cdn.mathjax.org/mathjax/'

MH_JS = SCRIPT_PREFIX + MJ_CDN + 'latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML' + SCRIPT_SUFFIX

def provide_ids(section_index, tag):
    per_page = 7

    amount = len(search_ids) if tag == '' else len(search_tags[tag])
    sections_number = ((amount - 1) // per_page) + 1
    section_index = max(1, min(int(section_index), sections_number))

    first_id = per_page * (section_index - 1)
    last_id = min(amount, first_id + per_page)

    ids = []

    for i in range(first_id, last_id):
        ids.append(search_ids[i if tag == '' else search_tags[tag][i]])

    return ids, sections_number, section_index, sorted(search_tags)

### interface functions ###

def entry_context(id):
    result = {
        'resources': [],
        'header': descriptions[id]['header'] }

    brashes = descriptions[id]['brashes']

    shON = False

    for brash in brashes:
        shON = shON or brash != 'mathjax'

    if shON > 0:
        result['resources'].append(SH_CSS)
        result['resources'].append(SH_CSS_DEF)
        result['resources'].append(SH_JS)
        result['resources'].append(SH_JS_KICK)

    for brash in brashes:
        if brash == 'c++':
            result['resources'].append(SH_JS_CPP)

        if brash == 'mathjax':
            result['resources'].append(MH_JS)


    return result

def list_context(section_id, tag):
    original_tag = tag.replace('_', ' ')
    ids, sections, section_index, tags = provide_ids(section_id, original_tag)
    split_tag = lambda x: {
        'link': x.replace(' ', '_'),
        'visible': x,
        'active': x != original_tag
    }

    result = {
        'descriptions': [],
        'sections_before': [i for i in range(1, section_index)],
        'section': section_index,
        'sections_after': [i + 1 for i in range(section_index, sections)],
        'tag': original_tag,
        'tags': [split_tag(tag) for tag in tags]
    }

    for id in ids:
        desc = {}
        for key, value in descriptions[id].items():
            if key != 'tags':
                desc[key] = value
            else:
                desc[key] = [split_tag(tag) for tag in value]

        result['descriptions'].append(desc)

    return result