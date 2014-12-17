from common.syntax_highlighter import syntax_brash

SCRIPT_PREFIX = '<script src="'
SCRIPT_SUFFIX = '" type="text/javascript"></script>'
STYLE_PREFIX = '<link href="'
STYLE_SUFFIX = '" rel="stylesheet" type="text/css">'

SH_CDN = 'http://cdnjs.cloudflare.com/ajax/libs/SyntaxHighlighter/3.0.83/'

SH_CSS = STYLE_PREFIX + SH_CDN + 'styles/shCore.css' + STYLE_SUFFIX
SH_JS = SCRIPT_PREFIX + SH_CDN + 'scripts/shCore.js' + SCRIPT_SUFFIX
SH_JS_KICK = '<script type="text/javascript">SyntaxHighlighter.all()</script>'
SH_JS_CPP = SCRIPT_PREFIX + SH_CDN + 'scripts/shBrushCpp.js' + SCRIPT_SUFFIX

def generate_context(name):
    result = { 'resources': [] }

    brash = syntax_brash(name)

    if brash != '':
        result['resources'].append(SH_CSS)
        result['resources'].append(SH_JS)
        result['resources'].append(SH_JS_KICK)

    if brash == 'c++':
        result['resources'].append(SH_JS_CPP)

    return result