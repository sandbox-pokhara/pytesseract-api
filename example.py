import cv2

from pytesseract_api import image_to_string

img = cv2.imread("sample.png")
print("TessBaseAPIGetBoxText")
print(image_to_string(img, method="TessBaseAPIGetBoxText"))
print("TessBaseAPIGetLSTMBoxText")
print(image_to_string(img, method="TessBaseAPIGetLSTMBoxText"))
print("TessBaseAPIGetWordStrBoxText")
print(image_to_string(img, method="TessBaseAPIGetWordStrBoxText"))
print("TessBaseAPIGetUTF8Text")
print(image_to_string(img, method="TessBaseAPIGetUTF8Text"))
