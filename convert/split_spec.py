from PIL import Image
from pdf2image import convert_from_path
import pytesseract
import numpy as np

# yield locations and contents of non-empty text in an iterable of images
def data_from_images(images):
    for pagenum, img in enumerate(images):
        # the '--psm 6' tag seems to give good results
        data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, config='--psm 6')
        for text, *box in zip(data['text'], data['left'], data['top'], data['width'], data['height']):
            # empty text values aren't useful
            if text:
                yield {'pagenum': pagenum, 'text': text.rstrip('.'), 'rect': box}

def remove_whitespace(image, padding=10):
    gray = np.array(image.convert('L'))

    black_indices = np.where((gray < 50).any(axis=1))
    
    if len(black_indices[0]) != 0:
        first_black_idx = np.min(black_indices)
        last_black_idx = np.max(black_indices)
    else:
        return image.crop((0, 0, image.width, 0))

    return image.crop((0, first_black_idx - padding, image.width, last_black_idx + padding))

if __name__ == '__main__':
    path = 'references/CCREST.pdf'

    imgs = convert_from_path(path, dpi=200)
    standards = imgs[43:66]

    width, height = standards[0].size
    image_padding = 10

    cropped_standards = (s.crop((100, 0, 300, height)) for s in standards)
    data = list(data_from_images(cropped_standards))
    next_data = data[1:]

    path = "assets/bylaws/{name}.png"

    for current_d, next_d in zip(data, next_data):
        print(current_d['text'], current_d['pagenum'])
        if current_d['pagenum'] == next_d['pagenum']:
            first_image = standards[current_d['pagenum']]
            first_image = first_image.crop((0, current_d['rect'][1] - image_padding, width, next_d['rect'][1] - image_padding))
            first_image = remove_whitespace(first_image, image_padding)
            first_image.save(path.format(name=current_d['text']))
        else:
            first_image = standards[current_d['pagenum']]
            first_image = first_image.crop((0, current_d['rect'][1] - image_padding, width, height))
            first_image = remove_whitespace(first_image, image_padding)

            second_image = standards[next_d['pagenum']]
            second_image = second_image.crop((0, 0, width, next_d['rect'][1] - image_padding))
            second_image = remove_whitespace(second_image, image_padding)

            joined_image = Image.new('RGB', (width, first_image.height + second_image.height))
            joined_image.paste(first_image, (0, 0))
            joined_image.paste(second_image, (0, first_image.height))
            joined_image.save(path.format(name=current_d['text']))

    # handle last bylaw image as its own case
    image = standards[-1]
    image = image.crop((0, data[-1]['rect'][1] - image_padding, width, height))
    image = remove_whitespace(image, image_padding)
    image.save(path.format(name=data[-1]['text']))
