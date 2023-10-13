import cv2

from pytesseract_api import image_to_string

img = cv2.imread("sample.png")
text = image_to_string(img)

print(text)
