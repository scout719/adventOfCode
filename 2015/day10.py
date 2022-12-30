# -*- coding: utf-8 -*-
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable=wrong-import-position
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2015
DAY = 10
EXPECTED_1 = None
EXPECTED_2 = None


""" DAY 10 """

def day10_parse(data):
    l = [int(d) for d in data[0]]
    return l

def day10_solve(data, times):
    data = day10_parse(data)
    for _ in range(times):
        curr = data[0]
        i = 1
        l = 1
        new_data = []
        while i < len(data):
            if data[i] == curr:
                l += 1
            else:
                new_data.append(l)
                new_data.append(curr)
                curr = data[i]
                l = 1
            i += 1

        new_data.append(l)
        new_data.append(curr)
        data = new_data

    return len(data)

def day10_1(data):
    return day10_solve(data, 40)

def day10_2(data):
    return day10_solve(data, 50)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
