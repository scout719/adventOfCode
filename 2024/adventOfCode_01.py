# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
from collections import defaultdict
from email.policy import default
import os
import sys
from typing import Counter, List

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2024
DAY = 1
EXPECTED_1 = 11
EXPECTED_2 = 31


""" DAY 1 """

def day1_parse(data):
    left, right = [], []
    for l in data:
        le, ri = l.split("   ")
        left.append(int(le))
        right.append(int(ri))
    return sorted(left), sorted(right)

def day1_1(data):
    left, right = day1_parse(data)
    dist = 0
    for i, v in enumerate(left):
        dist += abs(v - right[i])
    return dist

def day1_2(data):
    left, right = day1_parse(data)
    count = Counter(right)
    total = 0
    for k in left:
        total += k * count[k]
    return total


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
