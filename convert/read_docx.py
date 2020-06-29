import os
import json
import docx
import pyparsing
import unidecode

import parsedocx


def is_blank(string):
    return string.isspace() or len(string) == 0


class Paragraph():
    richtext_format = {
        'bold': '<b>{text}</b>',
        'underline': '<u>{text}</u>',
        'italic': '<i>{text}</i>',
        'superscript': '<sup>{text}</sup>',
        'subscript': '<sub>{text}</sub>'
    }

    def __init__(self, para):
        self.paragraph = para

    @property
    def text(self):
        return self.paragraph.text

    @property
    def richtext(self):
        all_text = ''
        for r in self.paragraph.runs:
            text = r.text

            if is_blank(text):
                continue

            if r.bold:
                text = self.richtext_format['bold'].format(text=text)
            if r.underline:
                text = self.richtext_format['underline'].format(text=text)
            if r.font.superscript:
                text = self.richtext_format['superscript'].format(text=text)
            if r.font.subscript:
                text = self.richtext_format['subscript'].format(text=text)

            all_text += text
        return all_text

    @property
    def is_context(self):
        if self.text.isspace() or len(self.text) == 0:
            return False

        para = self.paragraph
        is_bold = all(run.bold for run in para.runs if not run.text.isspace())
        is_underline = all(run.underline for run in para.runs if not run.text.isspace())
        is_uppercase = all(run.text == run.text.upper() for run in para.runs if not run.text.isspace())

        return is_bold and is_underline and is_uppercase


class DocxBylawReader():
    def __init__(self, filename):
        self.doc = docx.Document(filename)
        self.paragraphs = [Paragraph(para) for para in self.doc.paragraphs]

    @property
    def html_text(self):
        all_text = '<br>\n'.join(para.richtext for para in self.paragraphs if not is_blank(para.richtext))
        return unidecode.unidecode(all_text)

    def save_specifications(self, path):
        for spec in parsedocx.parse_specifications(self.html_text):
            filename = os.path.join(path, f"{spec['code']}.json")
            with open(filename, 'w') as f:
                json.dump(spec, f)

    def save_exceptions(self, path):
        for exception in parsedocx.parse_exceptions(self.html_text):
            filename = os.path.join(path, f"{exception['code']}.json")
            with open(filename, 'w') as f:
                json.dump(exception, f)



if __name__ == '__main__':
    reader = DocxBylawReader('convert/CCREST.docx')
    reader.save_specifications('app/static/bylaws/specifications')
    reader.save_exceptions('app/static/bylaws/exceptions')

