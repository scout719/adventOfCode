# -*- coding: utf-8 -*-
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable=wrong-import-position
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2016
DAY = 9
EXPECTED_1 = None
EXPECTED_2 = 241920

def day9_parse(data: list[str]):
    return data[0]

def day9_recurse(data, i, part2):
    if i >= len(data):
        return 0
    if data[i] == "(":
        j = 0
        while data[i + j] != "x":
            j += 1
        amt = int("".join(data[i + 1:i + j]))
        i += j
        j = 0
        while data[i + j] != ")":
            j += 1
        times = int("".join(data[i + 1:i + j]))
        i += j + 1
        i += amt

        if part2:
            amt = day9_recurse(data[i - amt:i], 0, part2)

        return amt * times + day9_recurse(data, i, part2)
    else:
        return 1 + day9_recurse(data, i + 1, part2)

def day9_solve(data, part2):
    data = day9_parse(data)
    return day9_recurse(data, 0, part2)

def day9_1(data):
    return day9_solve(data, False)

def day9_2(data):
    return day9_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
