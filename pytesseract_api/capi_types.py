from ctypes import Structure
from enum import Enum


class TessBaseAPI(Structure):
    ...


class TessPageSegMode(Enum):
    PSM_OSD_ONLY = 0
    PSM_AUTO_OSD = 1
    PSM_AUTO_ONLY = 2
    PSM_AUTO = 3
    PSM_SINGLE_COLUMN = 4
    PSM_SINGLE_BLOCK_VERT_TEXT = 5
    PSM_SINGLE_BLOCK = 6
    PSM_SINGLE_LINE = 7
    PSM_SINGLE_WORD = 8
    PSM_CIRCLE_WORD = 9
    PSM_SINGLE_CHAR = 10
    PSM_SPARSE_TEXT = 11
    PSM_SPARSE_TEXT_OSD = 12
    PSM_RAW_LINE = 13
    PSM_COUNT = 14
