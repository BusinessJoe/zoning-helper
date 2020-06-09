from PIL import Image
from PIL import ImageDraw
from pdf2image import convert_from_path
import pytesseract
import cv2
import os
import numpy as np
from pprint import pprint

# convert pdf to jpeg
images = convert_from_path("ionview.pdf")
images[0].save("ionview.jpg", 'JPEG')

image = cv2.imread("ionview.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

kernel = np.ones((2, 2), np.uint8)

#image = cv2.blur(image, (3, 3))
image = cv2.dilate(image, kernel, iterations=2)
#image = cv2.dilate(image, kernel, iterations=2)
filename = "intermediate.png"
#filename = f"{os.getpid()}.png"
print(filename)
cv2.imwrite(filename, image)

# Get image ocr data
image = Image.open(filename)
d = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

# Draw bounding boxes
image = image.convert(mode="RGB")
#image = Image.new("RGB", image.size, (255, 255, 255))
draw = ImageDraw.Draw(image)
n_boxes = len(d['level'])
for i in range(n_boxes):
    (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
    if len(d['text'][i].strip()):
        print(d['text'][i], w, h)
        draw.rectangle((x, y, x+w, y+h), outline="red", width=3)

image.save("boxes.png")
#text = pytesseract.image_to_string(image)

#os.remove(filename)

#with open('out.txt', 'w') as f:
#    f.write(text)
