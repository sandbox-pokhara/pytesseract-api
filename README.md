# pytesseract-api

Tesseract C-API in python, a faster alternative to pytesseract

## Installation

You can install the package via pip:

```bash
pip install pytesseract-api
```

## Usage

```python
import cv2

from pytesseract_api import image_to_string

img = cv2.imread("sample.png")
text = image_to_string(img)
print(text)
```

## Limitations

- Only supports opencv images as input as of now

## License

This project is licensed under the terms of the MIT license.

## Contact

If you want to contact me you can reach me at pradishbijukchhe@gmail.com.
