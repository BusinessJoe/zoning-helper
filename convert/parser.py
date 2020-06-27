from pyparsing import *


# Include newlines
#ParserElement.setDefaultWhitespaceChars(' \t')

html_breaks = Suppress(ZeroOrMore(Literal('<br>')))
context_start = Suppress('<u><b>')
context_end = Suppress('</b></u>')

contextName = Group(context_start + OneOrMore(Word(alphas.upper())).setParseAction(' '.join)('name') + context_end + html_breaks)

bylawCode = Group(LineStart() + Regex(r'\d+[A-Z]*') + Suppress('.' + White()))

bylawContent = (OneOrMore(Word(printables), stopOn=bylawCode | contextName)).setParseAction(' '.join)

bylaw = Group(bylawCode('code') + bylawContent('body'))

parser = contextName('context') + Group(OneOrMore(bylaw))('bylaws')

if __name__ == '__main__':
    from read_docx import DocxBylawReader
    reader = DocxBylawReader('CCREST.docx')

    result = parser.searchString(reader.html_text)
    print(result.dump())

    with open('test.txt', 'w') as f:
        f.write(reader.html_text)

