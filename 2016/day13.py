# -*- coding: utf-8 -*-
from collections import deque
from copy import deepcopy
import functools
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable=wrong-import-position
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2016
DAY = 13
EXPECTED_1 = None
EXPECTED_2 = None

def day13_parse(data: list[str]):
    return int(data[0])

def day13_wall(r, c, fav):
    x, y = c, r
    value = x * x + 3 * x + 2 * x * y + y + y * y
    value += fav
    cnt = 0
    while value != 0:
        cnt += value & 1
        value = value >> 1
    return cnt % 2 == 1

def day13_solve(data, part2):
    data = day13_parse(data)
    fav_number = data
    er, ec = 39, 31

    # fav_number = 10
    # er, ec = 4, 7

    r, c = 1, 1
    q: deque[tuple[int, int, int]] = deque([(0, 1, 1)])
    seen = set()
    p2 = set()
    while q:
        cost, r, c = q.popleft()
        if (r, c) in seen:
            continue
        seen.add((r, c))

        if not part2 and (r, c) == (er, ec):
            return cost

        if part2:
            if cost <= 50:
                print(len(seen))
                p2.add((r, c))
            if cost == 50:
                continue

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            rr, cc = r + dr, c + dc
            if rr < 0 or cc < 0 or day13_wall(r, c, fav_number):
                continue

            q.append((cost + 1, rr, cc))

    # high 291
    # high 283
    return len(p2)

def day13_1(data):
    # wrong 23
    # wrong 21
    return day13_solve(data, False)

def day13_2(data):
    return day13_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
