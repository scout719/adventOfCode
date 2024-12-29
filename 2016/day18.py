# -*- coding: utf-8 -*-
from collections import deque
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable=wrong-import-position
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2016
DAY = 18
EXPECTED_1 = 38
EXPECTED_2 = None

def day18_parse(data: list[str]):
    return data[0]

def day18_trap(mem, initial_row, row, col) -> bool:
    if col < 0 or col >= len(initial_row):
        return False

    if row == 0:
        assert col < len(initial_row)
        return initial_row[col] == "^"

    if (row, col) in mem:
        return mem[(row, col)]

    l = day18_trap(mem, initial_row, row - 1, col - 1)
    c = day18_trap(mem, initial_row, row - 1, col)
    r = day18_trap(mem, initial_row, row - 1, col + 1)

    res = (
        (l and c and not r) or
        (c and r and not l) or
        (l and not c and not r) or
        (r and not c and not l)
    )
    mem[(row, col)] = res
    return res

def day18_solve(data, part2):
    data = day18_parse(data)
    initial_row = data

    rows = 40
    if len(initial_row) <= 10:
        rows = 10

    if part2:
        rows = 400000

    ans = 0
    mem = {}
    for r in range(rows):
        l = ""
        for c in range(len(initial_row)):
            if not day18_trap(mem, initial_row, r, c):
                ans += 1
                l += "."
            else:
                l += "^"
        # print(l)
    return ans

def day18_1(data):
    return day18_solve(data, False)

def day18_2(data):
    return day18_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
