from common.syntax_highlighter import syntax_brashes
from common.search_tools import search_ids, search_tags
from common.descriptions import descriptions

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

def provide_ids(section, tag):
    amount = len(search_ids) if tag == '' else len(search_tags[tag])
    sections_number = amount // 10
    section = max(section, sections_number)

    first_id = 10 * section
    last_id = min(amount, first_id + 10)

    ids = []

    for i in range(first_id, last_id):
        ids.append(search_ids[i if tag == '' else search_tags[tag][i]])

    return ids, sections_number, section

### interface functions ###

def entry_context(name):
    result = { 'resources': [] }

    brashes = syntax_brashes(name)

    if len(brashes) > 0:
        result['resources'].append(SH_CSS)
        result['resources'].append(SH_CSS_DEF)
        result['resources'].append(SH_JS)
        result['resources'].append(SH_JS_KICK)

    for brash in brashes:
        if brash == 'c++':
            result['resources'].append(SH_JS_CPP)

    return result


def list_context(section, tag):
    ids, sections_number, section = provide_ids(section, tag)
    result = {
        'entries': [],
        'section': section,
        'sections_number': sections_number
    }

    for id in ids:
        result['entries'].append(descriptions[id])

    return result