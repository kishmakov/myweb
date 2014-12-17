from common.syntax_highlighter import syntax_brashes

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

def generate_context(name):
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