from pyparsing import *


def _specifications_parser():
    html_breaks = Suppress(OneOrMore('<br>'))

    context_start = Suppress(Literal('<u>') & Literal('<b>'))
    context_end = Suppress(Literal('</u>') & Literal('</b>'))

    contextName = OneOrMore(Word(alphas.upper())).setParseAction(' '.join)
    contextHeader = context_start + contextName + context_end

    bylawCode = LineStart() + Regex(r'\d+[A-Z]*') + Suppress('.' + White())

    bylawContent = (OneOrMore(Word(printables), stopOn=bylawCode | contextHeader)).setParseAction(' '.join)

    bylaw = Group(bylawCode + bylawContent)

    parser = contextHeader + html_breaks + Group(OneOrMore(bylaw))

    return parser


def _exceptions_parser():
    html_breaks = Suppress(ZeroOrMore('<br>'))

    exceptionHeader = Suppress(Literal('<u>') & Literal('<b>')) + "EXCEPTIONS" + Suppress(Literal('</u>') & Literal('</b>'))

    exceptionCode = LineStart() + Regex(r'\d+[A-Z]*') + Suppress('.' + White())

    exceptionContent = (OneOrMore(Word(printables), stopOn=exceptionCode)).setParseAction(' '.join)

    exception = exceptionCode + exceptionContent

    parser = Suppress(exceptionHeader + html_breaks + exceptionContent) + OneOrMore(Group(exception))

    return parser


def _value_of_code(code):
    """Returns a float representation of the code fpr use in ordering"""
    if code[-1].isalpha():
        integer = int(code[:-1])

        # decimal equals 1/27 times the position of the letter in the alphabet
        # A -> 1/27, B -> 2/27, ..., Z -> 26/27
        decimal = (ord(code[-1].lower()) - ord('a') + 1) / 27
    else:
        integer = int(code)
        decimal = 0
    return integer + decimal


def parse_specifications(html_text):
    """Returns a list of all specifications represented as dicts

    Each dict contains the following elements:
        - context: The header that gives context to the scope of the specification
            Examples: "FRONT YARD", "BUILDING SETBACK FROM LOT LINES"
        - code: An alphanumeric value tied to each specification
        - text: The main text of the specification
    """
    with open('convert/test.txt', 'w') as f:
        f.write(html_text)

    parser = _specifications_parser()
    parsed_specs = parser.searchString(html_text)

    specs = []

    for context_header, bylaws in parsed_specs:
        for code, text in bylaws:
            spec_dict = {'context': context_header,
                         'code': code,
                         'text': text}
            specs.append(spec_dict)

    return specs


def parse_exceptions(html_text):
    """Returns a list of all exceptions represented as dicts

        Each dict contains the following elements:
            - code: An alphanumeric value tied to each exception
            - text: The main text of the exception
    """
    parser = _exceptions_parser()
    exceptions = parser.searchString(html_text)

    exceptions_to_keep = []
    highest_code = 0
    recent_exception = None
    for idx, e in enumerate(exceptions[0]):
        code_string = e[0]
        code_value = _value_of_code(code_string)

        if code_value > highest_code:
            if recent_exception is not None:
                exception_dict = {'code': recent_exception[0], 'text': recent_exception[1]}
                exceptions_to_keep.append(exception_dict)

            highest_code = code_value
            recent_exception = e
        else:
            text_to_add = e[0] + '\t' + e[1]
            recent_exception[1] += text_to_add

    exception_dict = {'code': recent_exception[0], 'text': recent_exception[1]}
    exceptions_to_keep.append(exception_dict)

    return exceptions_to_keep


if __name__ == '__main__':
    from convert.read_docx import DocxBylawReader
    reader = DocxBylawReader('convert/CCREST.docx')
    results = parse_specifications(reader.html_text)


