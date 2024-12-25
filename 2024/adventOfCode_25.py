# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
from collections import defaultdict, deque
from copy import deepcopy
import functools
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2024
DAY = 25
EXPECTED_1 = 3
EXPECTED_2 = None

def day25_parse(data: list[str]):
    parts = "\n".join(data).split("\n\n")
    locks = []
    keys = []
    for part in parts:
        part = part.split("\n")
        R = len(part)
        C = len(part[0])
        is_lock = all(c == "#" for c in part[0])
        curr = []
        for c in range(C):
            height = sum(part[r][c] == "#" for r in range(R))
            curr.append(height - 1)
        if is_lock:
            locks.append(curr)
        else:
            keys.append(curr)

    return locks, keys

def day25_solve(data, part2):
    data = day25_parse(data)
    locks, keys = data
    ans = 0
    for lock in locks:
        for key in keys:
            fit = all(pin_height + height < 6 for pin_height,
                      height in zip(lock, key))
            if fit:
                ans += 1
    return ans if not part2 else "Merry Xmas! 🎅🏻"

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
