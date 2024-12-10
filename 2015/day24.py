# -*- coding: utf-8 -*-
from cgitb import small
from collections import defaultdict
from email.policy import default
from heapq import heappop, heappush
from math import ceil, cos, prod, sqrt
import os
from struct import pack
import sys
from time import time
from typing import Counter

from pkg_resources import yield_lines

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable=wrong-import-position
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2015
DAY = 24
EXPECTED_1 = 99
EXPECTED_2 = 44


""" DAY 24 """

def day24_parse(data: list[str]):
    packages = []
    for l in data:
        packages.append(int(l))
    return packages

def day24_combinations(packages, target, space_left):
    if len(packages) == 1:
        if packages[0] == target:
            yield from [[packages[0]]]
        else:
            yield from []
    elif space_left == 0:
        yield from []
    else:
        for combination in day24_combinations(packages[1:], target - packages[0], space_left - 1):
            yield [packages[0]] + combination
        yield from day24_combinations(packages[1:], target, space_left)

def day24_solve(data, part2):
    packages = day24_parse(data)
    buckets = 4 if part2 else 3
    target_weight = sum(packages) // buckets
    space = len(packages) // buckets
    combinations = day24_combinations(packages, target_weight, space)
    return min((len(c), prod(c)) for c in combinations)[1]

def day24_1(data):
    return day24_solve(data, False)

def day24_2(data):
    return day24_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
