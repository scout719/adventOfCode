# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
from collections import defaultdict
from heapq import heappop, heappush
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import day_with_validation  # NOQA: E402
from common.utils import main  # NOQA: E402

YEAR = 2023
DAY = 17
EXPECTED_1 = 102
EXPECTED_2 = 94

""" DAY 17 """

def day17_parse(data: list[str]):
    return [[int(x) for x in line] for line in data]

def day17_solve(city, part2):
    min_straight = 0
    max_straight = 3
    if part2:
        min_straight = 4
        max_straight = 10

    R = len(city)
    C = len(city[0])

    # down, right, up , left
    DR = [1, 0, -1, 0]
    DC = [0, 1, 0, -1]

    # heur, heat, r, c, d, straigth_left
    q = []
    # right
    q.append((R + C, 0, 0, 0, 1, max_straight))
    # down
    q.append((R + C, 0, 0, 0, 0, max_straight))
    seen = set()
    while q:
        curr = heappop(q)
        _, heat, r, c, d, straigth_rem = curr
        if (r, c) == (R - 1, C - 1):
            return heat
        k = (r, c, d, straigth_rem)
        if k in seen:
            continue
        seen.add(k)

        dirs = [(d + 1) % 4, (d - 1) % 4]
        if max_straight - straigth_rem < min_straight:
            # must continue straight
            dirs = []
        if straigth_rem > 0:
            # can keep going straight
            dirs.append(d)
        for dd in dirs:
            dr, dc = DR[dd], DC[dd]
            rr, cc = r + dr, c + dc
            if not (0 <= rr < R and 0 <= cc < C):
                continue
            n_straight_rem = straigth_rem - 1 if dd == d else max_straight - 1
            n_heat = heat + city[rr][cc]
            n_heur = heat + (R - rr) + (C - cc)
            heappush(q, (n_heur, n_heat, rr, cc, dd, n_straight_rem))
        # right
    return None

def day17_1(data):
    city = day17_parse(data)
    return day17_solve(city, False)

def day17_2(data: list[str]):
    city = day17_parse(data)
    return day17_solve(city, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
