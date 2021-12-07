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
# pylint: enable=import-error
# pylint: enable=wrong-import-position
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


WHITE_SQUARE = "█"
WHITE_CIRCLE = "•"
BLUE_CIRCLE = f"{bcolors.OKBLUE}{bcolors.BOLD}•{bcolors.ENDC}"
RED_SMALL_SQUARE = f"{bcolors.FAIL}{bcolors.BOLD}■{bcolors.ENDC}"

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

def day_with_validation(part, data):
    data_ex = read_input(YEAR, DAY * 100 + 1)
    expected_result = EXPECTED_1 if part == 1 else EXPECTED_2
    func = globals()[f"day{DAY}_{part}"]
    result = func(data_ex)
    if result != expected_result:
        print(f"{bcolors.FAIL}FAIL")
        print(result)
        print("SHOULD BE:")
        print(expected_result)
        print(f"{bcolors.ENDC}")
        return
    print(f"{bcolors.OKGREEN}SUCCESS{bcolors.ENDC}")
    print(f"{bcolors.OKBLUE}{func(data)}{bcolors.ENDC}")


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(1, data),
        f"day{DAY}_2": lambda data: day_with_validation(2, data),
    }, YEAR)
