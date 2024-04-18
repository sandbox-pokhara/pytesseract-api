import atexit
import os
from ctypes import CDLL
from ctypes import POINTER
from ctypes import c_bool
from ctypes import c_char_p
from ctypes import c_int
from ctypes import c_void_p
from ctypes import cdll
from functools import lru_cache
from typing import Any
from typing import Dict
from typing import Optional

from cv2.typing import MatLike

from pytesseract_api.capi_types import TessBaseAPI
from pytesseract_api.capi_types import TessPageSegMode
from pytesseract_api.exceptions import TesseractError


@lru_cache()
def find_tess_path() -> str:
    path = os.get_exec_path()
    for p in path:
        if p.lower().endswith("tesseract-ocr"):
            return p
    raise TesseractError("tesseract-ocr not found in PATH")


@lru_cache()
def get_tess_lib(lib_path: Optional[str]) -> CDLL:
    if lib_path is None:
        path = find_tess_path()
        lib_path = os.path.join(path, "libtesseract-5.dll")

    lib = cdll.LoadLibrary(lib_path)
    lib.TessBaseAPICreate.restype = POINTER(TessBaseAPI)
    lib.TessBaseAPICreate.argtypes = []
    lib.TessBaseAPIInit3.restype = c_int
    lib.TessBaseAPIInit3.argtypes = [
        POINTER(TessBaseAPI),
        c_char_p,
        c_char_p,
    ]
    lib.TessBaseAPIDelete.restype = None
    lib.TessBaseAPIDelete.argtypes = [POINTER(TessBaseAPI)]
    lib.TessBaseAPISetPageSegMode.restype = None
    lib.TessBaseAPISetPageSegMode.argtypes = [POINTER(TessBaseAPI), c_int]
    lib.TessBaseAPISetImage.restype = None
    lib.TessBaseAPISetImage.argtypes = [
        POINTER(TessBaseAPI),
        c_void_p,
        c_int,
        c_int,
        c_int,
        c_int,
    ]
    lib.TessBaseAPIGetUTF8Text.restype = c_char_p
    lib.TessBaseAPIGetUTF8Text.argtypes = [POINTER(TessBaseAPI)]
    lib.TessBaseAPISetVariable.restype = c_bool
    lib.TessBaseAPISetVariable.argtypes = [
        POINTER(TessBaseAPI),
        c_char_p,
        c_char_p,
    ]
    return lib


@lru_cache()
def get_tess_api(
    lib: CDLL,
    tessdata_path: Optional[str] = None,
    lang: str = "eng",
) -> Any:
    if tessdata_path is None:
        path = find_tess_path()
        tessdata_path = os.path.join(path, "tessdata")
    api = lib.TessBaseAPICreate()
    lib.TessBaseAPIInit3(api, tessdata_path.encode(), lang.encode())
    atexit.register(lambda: lib.TessBaseAPIDelete(api))
    return api


def get_image_data(img: MatLike) -> tuple[int, int, int, int, int]:
    depth = 1 if len(img.shape) < 3 else img.shape[2]
    return (
        img.ctypes.data,
        img.shape[1],
        img.shape[0],
        depth,
        depth * img.shape[1],
    )


def image_to_string(
    img: MatLike,
    lib_path: Optional[str] = None,
    tessdata_path: Optional[str] = None,
    lang: str = "eng",
    psm: TessPageSegMode = TessPageSegMode.PSM_SINGLE_BLOCK,
    variables: Dict[str, str] = {},
) -> str:
    # NOTE: ocr bugs on sliced image without this
    img = img.copy()
    data = get_image_data(img)

    lib = get_tess_lib(lib_path)
    api = get_tess_api(lib, tessdata_path=tessdata_path, lang=lang)
    for k, v in variables.items():
        lib.TessBaseAPISetVariable(api, k.encode(), v.encode())
    lib.TessBaseAPISetPageSegMode(api, psm.value)
    lib.TessBaseAPISetImage(api, *data)
    res: bytes = lib.TessBaseAPIGetUTF8Text(api)
    text = res.decode().strip()
    return text
