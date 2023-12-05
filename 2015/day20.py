# -*- coding: utf-8 -*-
from typing import Callable, Dict, Iterator, Union, Optional, List, ChainMap
import functools
import math
import os
from os.path import join
import sys
import time
from copy import deepcopy
from collections import Counter, defaultdict, deque
from heapq import heappop, heappush

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable=wrong-import-position
from common.utils import read_input, main, clear  # NOQA: E402
from common.utils import day_with_validation, bcolors, WHITE_CIRCLE, WHITE_SQUARE  # NOQA: E402
from common.utils import BLUE_CIRCLE, RED_SMALL_SQUARE  # NOQA: E402

YEAR = 2015
DAY = 20
EXPECTED_1 = 4
EXPECTED_2 = None


""" DAY 20 """

def day20_parse(data):
    return int(data[0])

def day20_divisors(n):
    res = []
    i = n
    while i > 0:
        if n % i == 0:
            res.append(i)
        i -= 1
    return res


def day20_1(data):
    data = day20_parse(data)
    i = 1
    curr = 1
    while curr < data:
        d = day20_divisors(i)
        curr2 = 0
        for d2 in d:
            curr2 += d2 * 10
        curr = curr2
        print(i, curr2, d)
        if curr2 >= data:
            return i
        i += 1
    curr = data // 2

    return data

def day20_2(data):
    data = day20_parse(data)
    return data


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
