# -*- coding: utf-8 -*-
# pylint: disable=import-error
# pylint: disable=unused-import
# pylint: disable=wildcard-import
# pylint: disable=wrong-import-position
# pylint: disable=consider-using-enumerate
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402
# pylint: enable=import-error
# pylint: enable=wrong-import-position

YEAR = 2022
DAY = 4
EXPECTED_1 = 2
EXPECTED_2 = 4


""" DAY 4 """

def day4_parse(data):
    pairs = []
    for line in data:
        _1, _2 = line.split(",")
        _1 = _1.split("-")
        _1 = [int(s) for s in _1]
        _2 = _2.split("-")
        _2 = [int(s) for s in _2]
        pairs.append((_1, _2))
    return pairs

def day4_1(data):
    data = day4_parse(data)
    count = 0
    for pair in data:
        _1, _2 = pair
        min_1, max_1 = _1
        min_2, max_2 = _2
        if min_1 <= min_2 <= max_2 <= max_1:
            count += 1
        elif min_2 <= min_1 <= max_1 <= max_2:
            count += 1
    return count

def day4_2(data):
    data = day4_parse(data)
    count = 0
    for pair in data:
        _1, _2 = pair
        min_1, max_1 = _1
        min_2, max_2 = _2
        if min_1 <= min_2 <= max_1:
            count += 1
        elif min_1 <= max_2 <= max_1:
            count += 1
        elif min_2 <= min_1 <= max_2:
            count += 1
        elif min_2 <= max_1 <= max_2:
            count += 1
    return count


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
