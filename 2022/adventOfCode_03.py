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
from common.utils import day_with_validation # NOQA: E402
# pylint: enable=import-error
# pylint: enable=wrong-import-position

YEAR = 2022
DAY = 3
EXPECTED_1 = 157
EXPECTED_2 = 70


""" DAY 3 """

def day3_parse(data):
    rucksack = []
    for line in data:
        size = len(line)
        first, second = line[:int(size / 2)], line[int(size / 2):]
        rucksack.append((first, second))
    return rucksack

def day3_priority(item):
    if ord(item) <= ord("Z"):
        return ord(item) - ord("A") + 27
    else:
        return ord(item) - ord('a') + 1

def day3_1(data):
    data = day3_parse(data)
    total = 0
    for _1, _2 in data:
        for item in _2:
            if item in _1:
                total += day3_priority(item)
                break
    return total

def day3_2(data):
    data = day3_parse(data)
    total = 0
    i = 0
    while i < len(data):
        _1 = data[i][0] + data[i][1]
        _2 = data[i + 1][0] + data[i + 1][1]
        _3 = data[i + 2][0] + data[i + 2][1]
        i += 3
        for item in _1:
            if item in _2 and item in _3:
                total += day3_priority(item)
                break
    return total


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
