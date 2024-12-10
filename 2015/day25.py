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
DAY = 25
EXPECTED_1 = 21345942
EXPECTED_2 = None


""" DAY 25 """

def day25_parse(data: list[str]):
    # ... Enter the code at row 3010, column 3019.
    left, right = data[0].split(", column ")
    return int(left.split(" ")[-1]), int(right.strip("."))

def day25_solve(data, part2):
    row, column = day25_parse(data)
    # convert from format
    # 1 3 6
    # 2 5
    # 4
    # to format
    # 1
    # 2 3
    # 4 5 6
    target_row = row + column - 1
    target_column = column
    idx = 1
    pos = 0
    while idx < target_row:
        pos += idx
        idx += 1

    target_pos = pos + target_column - 1
    code = 20151125
    for _ in range(target_pos):
        code *= 252533
        code %= 33554393
    return code

def day25_1(data):
    return day25_solve(data, False)

def day25_2(data):
    return day25_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
