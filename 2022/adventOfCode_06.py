# -*- coding: utf-8 -*-
# pylint: disable=import-error
# pylint: disable=unused-import
# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=wrong-import-position
# pylint: disable=consider-using-enumerate
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
from common.utils import main, day_with_validation  # NOQA: E402
# pylint: enable=import-error
# pylint: enable=wrong-import-position

YEAR = 2022
DAY = 6
EXPECTED_1 = 11
EXPECTED_2 = 26


""" DAY 6 """

def day6_parse(data):
    return data[0]

def day6_has_duplicated(curr):
    counter = defaultdict(int)
    for c in curr:
        counter[c] += 1
    return any([c > 1 for c in counter.values()])

def day6_solve(line, n_distinct):
    curr = line[:n_distinct]

    i = n_distinct
    while i < len(line):
        if day6_has_duplicated(curr):
            curr = curr[1:]
            curr += line[i]
        else:
            return i
        i += 1

def day6_1(data):
    line = day6_parse(data)
    return day6_solve(line, 4)

def day6_2(data):
    line = day6_parse(data)
    return day6_solve(line, 14)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
