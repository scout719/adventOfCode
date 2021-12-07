# -*- coding: utf-8 -*-
# pylint: disable=import-error
# pylint: disable=unused-import
# pylint: disable=wildcard-import
# pylint: disable=wrong-import-position
# pylint: disable=consider-using-enumerate
import functools
import math
import os
from os.path import join
import sys
import time
from copy import deepcopy
from collections import defaultdict
from heapq import heappop, heappush

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import read_input, main, clear  # NOQA: E402
from common.utils import day_with_validation, bcolors, WHITE_CIRCLE, WHITE_SQUARE  # NOQA: E402
from common.utils import BLUE_CIRCLE, RED_SMALL_SQUARE  # NOQA: E402
# pylint: enable=import-error
# pylint: enable=wrong-import-position

YEAR = 2021
DAY = 8
EXPECTED_1 = None
EXPECTED_2 = None

""" DAY 8 """

def day8_parse(data):
    return data

def day8_1(data):
    data = day8_parse(data)
    return data

def day8_2(data):
    data = day8_parse(data)
    return data


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, EXPECTED_2, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, EXPECTED_2, 2, data),
    }, YEAR)
