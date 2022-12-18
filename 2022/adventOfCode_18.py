# -*- coding: utf-8 -*-
# pylint: disable=import-error
# pylint: disable=unused-import
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# pylint: disable=wrong-import-position
# pylint: disable=consider-using-enumerate
import functools
import math
import os
from os.path import join
import sys
import time
from copy import deepcopy
from collections import defaultdict
from heapq import heappop, heappush

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main, day_with_validation, WHITE_SQUARE  # NOQA: E402
# pylint: enable=import-error
# pylint: enable=wrong-import-position

YEAR = 2022
DAY = 18
EXPECTED_1 = 64
EXPECTED_2 = 58

""" DAY 18 """

def day18_parse(data):
    droplets = set()
    for line in data:
        words = line.split(",")
        droplets.add(tuple(int(c) for c in words))
    return droplets

def day18_1(data):
    droplets = day18_parse(data)
    D = [(0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)]
    ans = 0
    for x, y, z in droplets:
        for dx, dy, dz in D:
            xx, yy, zz = x + dx, y + dy, z + dz
            if not (xx, yy, zz) in droplets:
                ans += 1
    return ans

def day18_is_inside(x, y, z, DP, drops):
    if (x, y, z) in DP:
        return DP[(x, y, z)]

    xs = [xx for xx, yy, zz in drops]
    min_x = min(xs)
    max_x = max(xs)

    ys = [yy for xx, yy, zz in drops]
    min_y = min(ys)
    max_y = max(ys)

    zs = [zz for xx, yy, zz in drops]
    min_z = min(zs)
    max_z = max(zs)

    D = [(0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)]
    q = [(x, y, z)]
    visited = set()
    while q:
        xx, yy, zz = q.pop()
        if not (min_x <= xx <= max_x and min_y <= yy <= max_y and min_z <= zz <= max_z):
            for xxx,yyy,zzz in visited:
                DP[(xxx, yyy, zzz)] = False
            return False
        if (xx, yy, zz) in visited:
            continue
        visited.add((xx, yy, zz))
        if (xx, yy, zz) in drops:
            continue
        for dx, dy, dz in D:
            xxx, yyy, zzz = xx + dx, yy + dy, zz + dz
            q.append((xxx, yyy, zzz))
    for xxx,yyy,zzz in visited:
        DP[(xxx, yyy, zzz)] = True
    return True

def day18_2(data):
    droplets = day18_parse(data)
    D = [(0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)]
    ans = 0
    DP = {}
    for x, y, z in droplets:
        for dx, dy, dz in D:
            xx, yy, zz = x + dx, y + dy, z + dz
            if not (xx, yy, zz) in droplets and not day18_is_inside(xx, yy, zz, DP, droplets):
                ans += 1

    # 2080
    return ans


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
