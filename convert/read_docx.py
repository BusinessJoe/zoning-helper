import docx
import re

class Bylaw:
    def __init__(self, id_='', context='', text=''):
        self.id_ = id_
        self.context = context
        self.text = text

    def save_as_html(self, filename):
        with open(filename, 'w') as f:
            f.write(self.text)


def get_bylaw_context(paragraph):
    """
    Returns paragraph text if the text is capitalized, bold and underlined. Returns an empty string otherwise or if
    the paragraph is only whitespace.
    """
    if paragraph.text.isspace():
        return ''

    is_bold = all(run.bold for run in paragraph.runs if not run.text.isspace())
    is_underline = all(run.underline for run in paragraph.runs if not run.text.isspace())
    is_uppercase = all(run.text == run.text.upper() for run in paragraph.runs if not run.text.isspace())

    if is_bold and is_underline and is_uppercase:
        return paragraph.text
    else:
        return ''


def get_bylaws(filename):
    doc = docx.Document(filename)

    bylaw_pattern = re.compile("^[0-9]+[A-Z]?\.")

    header_count = 0
    read_bylaws = False

    context = None
    bylaw = None
    bylaws = []
    for para in doc.paragraphs:
        if not read_bylaws:
            if 'PERFORMANCE STANDARD CHART - SCHEDULE "B"' in para.text:
                header_count += 1

            if header_count == 2:
                read_bylaws = True

        if read_bylaws:
            if get_bylaw_context(para):
                context = get_bylaw_context(para)

            if context:
                matches = bylaw_pattern.findall(para.text)
                if matches:
                    bylaw = Bylaw(id_=matches[0], context=context)
                    bylaws.append(bylaw)

                if bylaw:
                    if not para.text.isspace() and not get_bylaw_context(para):
                        bylaw.text += para.text + '\n'

    return bylaws

if __name__ == '__main__':
    bylaws = get_bylaws('CCREST.docx')

    for bylaw in bylaws:
        filename = f'html/{bylaw.id_}.html'
        bylaw.save_as_html(filename)

