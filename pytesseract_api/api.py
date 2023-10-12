import atexit
import os
from functools import lru_cache

from pytesseract_api.capi import CpyAPI
from pytesseract_api.capi_types import TessPageSegMode
from pytesseract_api.exceptions import TesseractError


@lru_cache()
def find_tess_path():
    path = os.get_exec_path()
    for p in path:
        if p.lower().endswith("tesseract-ocr"):
            return p
    raise TesseractError("tesseract-ocr not found in PATH")


@lru_cache()
def get_tess_api(lib_path=None, tessdata_path=None, lang="eng"):
    if lib_path is None:
        path = find_tess_path()
        lib_path = os.path.join(path, "libtesseract-5.dll")

    if tessdata_path is None:
        path = find_tess_path()
        tessdata_path = os.path.join(path, "tessdata")

    api = CpyAPI(lib_path)
    api.TessBaseAPIInit3(tessdata_path.encode(), lang.encode())
    atexit.register(api.TessBaseAPIDelete)
    return api


def get_image_data(img):
    depth = 1 if len(img.shape) < 3 else img.shape[2]
    return (
        img.ctypes.data,
        img.shape[1],
        img.shape[0],
        depth,
        depth * img.shape[1],
    )


def image_to_string(
    img,
    lib_path=None,
    tessdata_path=None,
    lang="eng",
    psm=TessPageSegMode.PSM_SINGLE_BLOCK,
):
    # NOTE: ocr bugs on sliced image without this
    img = img.copy()
    data = get_image_data(img)
    api = get_tess_api(
        lib_path=lib_path, tessdata_path=tessdata_path, lang=lang
    )
    api.TessBaseAPISetPageSegMode(psm)
    api.TessBaseAPISetImage(*data)
    res = api.TessBaseAPIGetUTF8Text()
    text = res.decode().strip()
    return text
