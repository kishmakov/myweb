import markdown
from markdown.util import etree as ET

REF_RE = r'\[ref (.+)\]'
REF_BEGIN = 'temp-math-begin'
REF_END = 'temp-math-end'

class BracesPre(markdown.preprocessors.Preprocessor):
    """ Escapes text for proper mathjax rendering. """

    ESCAPED_CHARS = ['{', '}', '[', ']', '(', ')']
    EM_CHARS = [' ', '\n', '.', ',', ';', ':', '_']

    def escape(self, text):
        result = []
        l = len(text)
        i = 0
        while i < l:
            if text[i] == '\\':
                if i + 1 == l:
                    result.append(text[i])
                    i += 1
                    continue

                if text[i + 1] == '\\':
                    result.append('\\\\\\\\')
                    i += 2
                    continue

                if text[i + 1] in self.ESCAPED_CHARS:
                    result.append('\\\\')
                    result.append(text[i + 1])
                    i += 2
                    continue

                result.append('\\')
                i += 1
                continue

            if text[i] == '_':
                if i + 1 == l or i == 0:
                    result.append(text[i])
                    i += 1
                    continue

                if text[i - 1] not in self.EM_CHARS and text[i + 1] not in self.EM_CHARS:
                    result.append('\_')
                    i += 1
                    continue

                result.append('_')
                i += 1
                continue

            result.append(text[i])
            i += 1
            continue

        return ''.join(result)

    def run(self, lines):
        result = []
        for line in lines:
            result.append(self.escape(line))

        return result

class BracesPost(markdown.postprocessors.Postprocessor):
    """ Escapes all occurences of '{{' and '}}' for django. """

    def run(self, text):
        text = text.replace('{{', '{% templatetag openvariable %}')
        text = text.replace('}}', '{% templatetag closevariable %}')
        text = text.replace(REF_BEGIN, '{{')
        text = text.replace(REF_END, '}}')
        text = text.replace('\_', '_')

        return text

class RefPattern(markdown.inlinepatterns.SimpleTextPattern):
    def __init__ (self, pattern):
        super(RefPattern, self).__init__(pattern)


    def handleMatch(self, m):
        def wrap(text):
            return REF_BEGIN + ' ' + text + ' ' + REF_END

        refed = 'ref.' + m.group(2).replace(' ', '.')
        cite_ref = 'cite_ref-' + wrap(refed + '.id')
        cite_note = '#cite_note-' + wrap(refed + '.id')

        span = ET.Element('span')
        a = ET.SubElement(span, 'a')

        span.set('id', cite_ref)

        a.set('href', cite_note)
        a.set('title', wrap(refed + '.title'))
        a.text = '[' + wrap(refed + '.id') + ']'
        return span

class DjangoExtension(markdown.extensions.Extension):
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add('ref', RefPattern(REF_RE), '<escape')
        md.preprocessors.add('braces', BracesPre(self), '>reference')
        md.postprocessors.add('braces', BracesPost(self), '>amp_substitute')

def makeExtension(configs={}):
    return DjangoExtension(configs=dict(configs))