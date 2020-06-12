import docx
import re
import json

class Bylaw:
    def __init__(self, id_='', context='', text=''):
        self.id_ = id_.rstrip().rstrip('.')
        self.context = context
        self.text = text

    def save_as_txt(self, filename):
        with open(filename, 'w') as f:
            f.write(self.text)

    def save_as_json(self, filename):
        to_dump = {'context': self.context, 'code': self.id_, 'text': self.text}
        with open(filename, 'w') as f:
            json.dump(to_dump, f)


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

    bylaw_pattern = re.compile("^[0-9]+[A-Z]?\.\s+")

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
                if context == 'EXCEPTIONS':
                    read_bylaws = False
                    break

            if context:
                text_to_append = para.text
                matches = bylaw_pattern.findall(text_to_append)
                if matches:
                    if matches[0] == '1.':
                        print(para.text)
                    bylaw = Bylaw(id_=matches[0], context=context)
                    bylaws.append(bylaw)

                    text_to_append = text_to_append.lstrip(matches[0])

                if bylaw:
                    if not para.text.isspace() and not get_bylaw_context(para):
                        bylaw.text += text_to_append + '\n'

    return bylaws

if __name__ == '__main__':
    bylaws = get_bylaws('convert/CCREST.docx')

    for bylaw in bylaws:
        filename = f'assets/bylaws/{bylaw.id_}.json'
        bylaw.save_as_json(filename)

