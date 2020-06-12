from PIL import Image
from PIL import ImageDraw
from pdf2image import convert_from_path
import pytesseract
import cv2
import io
import os
import PyPDF2
import numpy as np
from pprint import pprint


def data_from_images(images):
    for pagenum, img in enumerate(images):
        data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, config='--psm 6')
        for text, *box in zip(data['text'], data['left'], data['top'], data['width'], data['height']):
            if text:
                yield pagenum, text.rstrip('.'), box

if __name__ == '__main__':
    path = 'references/CCREST.pdf'

    imgs = convert_from_path(path, dpi=200)
    standards = imgs[43:66]
    exceptions = imgs[66:]

    width, height = standards[0].size

    cropped_standards = (s.crop((100, 0, 300, height)) for s in standards)

    data = data_from_images(cropped_standards)

    with open(path, 'rb') as file_in:
        pdf_dims = PyPDF2.PdfFileReader(file_in).getPage(0).mediaBox
        pdf_out = PyPDF2.PdfFileMerger()

        pdf_out.append(file_in)

        for d in data:
            print(d[1])
            title = PyPDF2.generic.TextStringObject(d[1])
            pagenum = PyPDF2.generic.NumberObject(d[0] + 43)

            fit = PyPDF2.generic.NameObject('/FitH')

            # PDF origin is at bottom left so subtract the destination height from the page height
            # we also need to scale the height because the pdf and image have different heights
            ratio = float(pdf_dims.getHeight()) / height
            pdf_height = (height - d[2][1]) * ratio
            # add an offset so that the top of the text isn't cut off
            pdf_height += 10

            dest = PyPDF2.generic.Destination(title, pagenum, fit, PyPDF2.generic.NumberObject(pdf_height))
            pdf_out.named_dests.append(dest)
    
        with open('assets/bookmarked.pdf', 'wb') as file_out:
            pdf_out.write(file_out)

