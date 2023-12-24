# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
from collections import defaultdict, deque
from copy import deepcopy
from heapq import heappop, heappush
from math import lcm
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import WHITE_SQUARE, day_with_validation  # NOQA: E402
from common.utils import main  # NOQA: E402

YEAR = 2023
DAY = 24
EXPECTED_1 = 2  # None
EXPECTED_2 = -1  # None

""" DAY 24 """

def day24_parse(data: list[str]):
    hail = list()
    for line in data:
        pos, vel = line.split(" @ ")
        pos, vel = tuple([int(x) for x in pos.split(", ")]), tuple([int(x)
                                                                    for x in vel.split(", ")])
        hail.append((pos, vel))
    return hail

def day24_mnop(m: tuple[int, int, int], n: tuple[int, int, int], o: tuple[int, int, int], p: tuple[int, int, int]):
    (x1_1, y1_1, z1_1), (x1_2, y1_2, z1_2), (x2_1,
                                             y2_1, z2_1), (x2_2, y2_2, z2_2) = m, n, o, p
    res_x = (x1_1 - x1_2) * (x2_1 - x2_2)
    res_y = (y1_1 - y1_2) * (y2_1 - y2_2)
    res_z = (z1_1 - z1_2) * (z2_1 - z2_2)
    return res_x + res_y + res_z

def day24_mua(p1: tuple[int, int, int], p2: tuple[int, int, int], p3: tuple[int, int, int], p4: tuple[int, int, int]):
    d1343 = day24_mnop(p1, p3, p4, p3)
    d4321 = day24_mnop(p4, p3, p2, p1)
    d1321 = day24_mnop(p1, p3, p2, p1)
    d4343 = day24_mnop(p4, p3, p4, p3)
    d2121 = day24_mnop(p2, p1, p2, p1)
    ans_den = d2121 * d4343 - d4321 * d4321
    ans_num = d1343 * d4321 - d1321 * d4343
    return ans_num / ans_den if ans_den > 0 else None

def day24_mub(p1: tuple[int, int, int], p2: tuple[int, int, int], p3: tuple[int, int, int], p4: tuple[int, int, int]):
    d1343 = day24_mnop(p1, p3, p4, p3)
    d4321 = day24_mnop(p4, p3, p2, p1)
    d4343 = day24_mnop(p4, p3, p4, p3)
    mua = day24_mua(p1, p2, p3, p4)
    return (d1343 + mua * d4321) / d4343 if mua else None


def day24_solve(x, part2):
    hails: set[tuple[tuple[int, int, int], tuple[int, int, int]]] = x
    min_ = 200000000000000 if len(hails) == 300 else 7
    max_ = 400000000000000 if len(hails) == 300 else 27
    ans = 0
    for i, h1 in enumerate(hails):
        for j, h2 in enumerate(hails):
            if h1 >= h2:
                continue
            (x1_1, y1_1, z1_1), (vx1, vy1, vz1) = h1
            # print(h1[0], h1[1], h1[0]+h1[1])
            x1_2, y1_2, z1_2 = h1[0][0] + \
                h1[1][0], h1[0][1] + h1[1][1], h1[0][2] + h1[1][2]
            (x2_1, y2_1, z2_1), (vx2, vy2, vz2) = h2
            x2_2, y2_2, z2_2 = h2[0][0] + \
                h2[1][0], h2[0][1] + h2[1][1], h2[0][2] + h2[1][2]
            slope1 = (y1_2 - y1_1) / (x1_2 - x1_1)
            slope2 = (y2_2 - y2_1) / (x2_2 - x2_1)
            if slope1 == slope2:
                # parallel
                continue

            b1 = y1_1 - slope1 * x1_1
            b2 = y2_1 - slope2 * x2_1
            # slope1*x + b1 == slope2*x + b2
            # (slope1-slope2)*x == b2- b1
            # x == (b2-b1)/(slope1-slope2)
            x_inter = (b2 - b1) / (slope1 - slope2)
            y_inter = b1 + slope1 * x_inter

            if min_ <= x_inter <= max_ and min_ <= y_inter <= max_:
                # inside test area
                if vx1 > 0:
                    # left to right
                    if x1_1 < x_inter:
                        if vx2 > 0:
                            if x2_1 < x_inter:
                                ans += 1
                        else:
                            assert vx2 < 0
                            # right to left
                            if x2_1 > x_inter:
                                ans += 1
                else:
                    assert vx1 < 0
                    # right to left
                    if x1_1 > x_inter:
                        if vx2 > 0:
                            if x2_1 < x_inter:
                                ans += 1
                        else:
                            assert vx2 < 0
                            # right to left
                            if x2_1 > x_inter:
                                ans += 1
    # high:
    # 21463
    return ans

def day24_1(data):
    x = day24_parse(data)
    return day24_solve(x, False)

def day24_2(data: list[str]):
    x = day24_parse(data)
    return day24_solve(x, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
