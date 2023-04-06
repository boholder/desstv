"""Constants for SSTV specification and each supported mode"""

from enum import Enum
from typing import Type


class COL_FMT(Enum):
    # red, green, blue
    RGB = 1
    # green, blue, red
    GBR = 2
    # also known as "Y, R-Y, B-Y", or "YCrCb"
    YUV = 3
    # black, white
    BW = 4


class Martin(object):
    COLOR = COL_FMT.GBR
    SYNC_PULSE = 0.004862
    SYNC_PORCH = 0.000572
    SEP_PULSE = 0.000572
    CHAN_COUNT = 3
    CHAN_SYNC = 0

    HAS_START_SYNC = False
    HAS_HALF_SCAN = False
    HAS_ALT_SCAN = False

    # === difference between specific modes ===
    NAME: str
    # width: how many pixels per line
    LINE_WIDTH: int
    # height: how many lines
    LINE_COUNT: int

    # how long does it take to scan a channel
    # (not a line, one line contains three channels)
    SCAN_TIME: float
    # a factor to span the scan window of one pixel
    WINDOW_FACTOR: float


class M1(Martin):
    NAME = "Martin 1"

    LINE_WIDTH = 320
    LINE_COUNT = 256
    SCAN_TIME = 0.146432
    WINDOW_FACTOR = 2.34


class M2(Martin):
    NAME = "Martin 2"

    # two of four references say that M2's width is 160,
    # while the other two say that is 320, same as M1.
    LINE_WIDTH = 320
    LINE_COUNT = 256
    SCAN_TIME = 0.073216
    WINDOW_FACTOR = 4.68


def martin_additional(cls: Type[Martin]):
    cls.CHAN_TIME = Martin.SEP_PULSE + cls.SCAN_TIME

    cls.CHAN_OFFSETS = [Martin.SYNC_PULSE + Martin.SYNC_PORCH]
    cls.CHAN_OFFSETS.append(cls.CHAN_OFFSETS[0] + cls.CHAN_TIME)
    cls.CHAN_OFFSETS.append(cls.CHAN_OFFSETS[1] + cls.CHAN_TIME)

    cls.LINE_TIME = cls.CHAN_OFFSETS[2] + cls.CHAN_TIME
    cls.PIXEL_TIME = cls.SCAN_TIME / cls.LINE_WIDTH


martin_additional(M1)
martin_additional(M2)


class Scottie(object):
    COLOR = COL_FMT.GBR
    SYNC_PULSE = 0.009000
    SYNC_PORCH = 0.001500
    SEP_PULSE = 0.001500
    CHAN_COUNT = 3
    CHAN_SYNC = 2

    HAS_START_SYNC = True
    HAS_HALF_SCAN = False
    HAS_ALT_SCAN = False

    NAME: str
    LINE_WIDTH: int
    LINE_COUNT: int
    SCAN_TIME: float
    WINDOW_FACTOR: float


class S1(Scottie):
    NAME = "Scottie 1"
    LINE_WIDTH = 320
    LINE_COUNT = 256
    SCAN_TIME = 0.138240
    WINDOW_FACTOR = 2.48


class S2(Scottie):
    NAME = "Scottie 2"
    LINE_WIDTH = 320
    LINE_COUNT = 256
    SCAN_TIME = 0.088064
    WINDOW_FACTOR = 3.82


class SDX(Scottie):
    """
    The longer transmission time supports better image quality.
    Scottie DX is designed for long distance transmission.
    """

    NAME = "Scottie DX"
    LINE_WIDTH = 320
    LINE_COUNT = 256
    SCAN_TIME = 0.345600
    WINDOW_FACTOR = 0.98


def scottie_additional(cls: Type[Scottie]):
    cls.CHAN_TIME = Scottie.SEP_PULSE + Scottie.SCAN_TIME

    cls.CHAN_OFFSETS = [Scottie.SYNC_PULSE + Scottie.SYNC_PORCH + cls.CHAN_TIME]
    cls.CHAN_OFFSETS.append(cls.CHAN_OFFSETS[0] + cls.CHAN_TIME)
    cls.CHAN_OFFSETS.append(Scottie.SYNC_PULSE + Scottie.SYNC_PORCH)

    cls.LINE_TIME = Scottie.SYNC_PULSE + 3 * cls.CHAN_TIME
    cls.PIXEL_TIME = cls.SCAN_TIME / cls.LINE_WIDTH


scottie_additional(S1)
scottie_additional(S2)
scottie_additional(SDX)


class RobotColor(object):
    COLOR = COL_FMT.YUV
    SYNC_PULSE = 0.009000
    SYNC_PORCH = 0.003000
    SEP_PULSE = 0.004500
    SEP_PORCH = 0.001500
    CHAN_SYNC = 0

    HAS_START_SYNC = False
    HAS_HALF_SCAN = True

    NAME: str
    LINE_WIDTH: int
    LINE_COUNT: int
    SCAN_TIME: float
    WINDOW_FACTOR: float

    CHAN_COUNT: int
    HAS_ALT_SCAN: bool


class R36(RobotColor):
    NAME = "Robot 36 Color"

    LINE_WIDTH = 320
    LINE_COUNT = 240
    SCAN_TIME = 0.088000
    HALF_SCAN_TIME = SCAN_TIME / 2

    CHAN_COUNT = 2
    CHAN_TIME = RobotColor.SEP_PULSE + SCAN_TIME

    CHAN_OFFSETS = [RobotColor.SYNC_PULSE + RobotColor.SYNC_PORCH]
    CHAN_OFFSETS.append(CHAN_OFFSETS[0] + CHAN_TIME + RobotColor.SEP_PORCH)

    LINE_TIME = CHAN_OFFSETS[1] + HALF_SCAN_TIME
    PIXEL_TIME = SCAN_TIME / LINE_WIDTH
    HALF_PIXEL_TIME = HALF_SCAN_TIME / LINE_WIDTH

    WINDOW_FACTOR = 7.70
    HAS_ALT_SCAN = True


class R72(RobotColor):
    NAME = "Robot 72 Color"

    LINE_WIDTH = 320
    SCAN_TIME = 0.138000
    HALF_SCAN_TIME = SCAN_TIME / 2

    CHAN_COUNT = 3
    CHAN_TIME = RobotColor.SEP_PULSE + SCAN_TIME
    HALF_CHAN_TIME = RobotColor.SEP_PULSE + HALF_SCAN_TIME

    CHAN_OFFSETS = [RobotColor.SYNC_PULSE + RobotColor.SYNC_PORCH]
    CHAN_OFFSETS.append(CHAN_OFFSETS[0] + CHAN_TIME + RobotColor.SEP_PORCH)
    CHAN_OFFSETS.append(CHAN_OFFSETS[1] + HALF_CHAN_TIME + RobotColor.SEP_PORCH)

    LINE_TIME = CHAN_OFFSETS[2] + HALF_SCAN_TIME
    PIXEL_TIME = SCAN_TIME / LINE_WIDTH
    HALF_PIXEL_TIME = HALF_SCAN_TIME / LINE_WIDTH

    WINDOW_FACTOR = 4.88
    HAS_ALT_SCAN = False


VIS_MAP = {8: R36, 12: R72, 40: M2, 44: M1, 56: S2, 60: S1, 76: SDX}

# The calibration header with VIS(Vertical Interval Signaling) code
# (code that tells which mode this audio used)
# ------------------------------
# time(ms) freq(hz) meaning
# 300       1900    Leader tone
# 10        1200    Break
# 300       1900    Leader tone
# 30        1200    VIS start bit
# 7(+1) bits for indicating mode...
# 30        1200    VIS stop bit
# ------------------------------
LEADER_TONE_SIZE = 0.300
BREAK_SIZE = 0.010
VIS_BIT_SIZE = 0.030

# These OFFSET variables' values describe the start time point of each part
BREAK_OFFSET = LEADER_TONE_SIZE
SECOND_LEADER_OFFSET = BREAK_OFFSET + BREAK_SIZE
VIS_START_BIT_OFFSET = BREAK_OFFSET + SECOND_LEADER_OFFSET

# To be correct, the "VIS start bit" should not be included in the "header",
# we include it here for convenience
HDR_SIZE = VIS_START_BIT_OFFSET + VIS_BIT_SIZE

# Our custom frequency checking window size and skip size for finding the header
SEARCH_WINDOW_SIZE = 0.010
JUMP_SIZE = 0.002
