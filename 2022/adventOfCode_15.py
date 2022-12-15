# -*- coding: utf-8 -*-
# pylint: disable=import-error
# pylint: disable=unused-import
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# pylint: disable=wrong-import-position
# pylint: disable=consider-using-enumerate
from typing import Callable, Dict, Iterator, Union, Optional, List, ChainMap
import functools
import math
import os
from os.path import join
import sys
import time
from copy import deepcopy
from collections import Counter, defaultdict, deque
from heapq import heappop, heappush

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main, day_with_validation  # NOQA: E402
# pylint: enable=import-error
# pylint: enable=wrong-import-position

YEAR = 2022
DAY = 15
EXPECTED_1 = None
EXPECTED_2 = None
EXPECTED_2 = 56000011


""" DAY 15 """

def day15_parse(data):
    s = []
    for line in data:
        # Sensor at x=2, y=18: closest beacon is at x=-2, y=15
        parts = line.split(":")
        sx = int(parts[0].split(",")[0].split("=")[1])
        sy = int(parts[0].split(",")[1].split("=")[1])
        cx = int(parts[1].split(",")[0].split("=")[1])
        cy = int(parts[1].split(",")[1].split("=")[1])
        s.append(((sx, sy), (cx, cy)))
    return s

def day15_1(data):
    s = day15_parse(data)
    t = 2000000
    return ""

    b_range_x = max(abs(bx - sx) for (sx, sy), (bx, by) in s)
    lo_x = min(sx for (sx, sy), (bx, by) in s)
    hi_x = max(sx for (sx, sy), (bx, by) in s)
    # return b_range_x, lo_x, hi_x
    n = set()
    for i in range(lo_x - b_range_x, hi_x + b_range_x + 1):
        y = t
        x = i
        for sen, b in s:
            sx, sy = sen
            bx, by = b
            dist = abs(sx - bx) + abs(sy - by)
            dist2 = abs(sx - x) + abs(sy - y)
            if dist2 <= dist and not (x == bx and y == by):
                n.add((x, y))
                break
    # 4797228
    # print(b_range_x, lo_x, hi_x)
    # print(n)
    return len([1 for x, y in n if y == t])

def day15_flood(cx,cy,dist,n, DP):
    print(dist)
    if dist < 0:
        return
    k = (cx,cy)
    if k in DP and DP[k] >= dist:
        return
    DP[k] = dist
    n.add((cx,cy))
    D = [(0,-1), (0,1), (-1,0), (1,0)]
    for dx,dy in D:
        day15_flood(cx+dx, cy+dy, dist-1, n, DP)


def day15_2(data):
    s = day15_parse(data)
    t = 2000000

    b_range_x = max(abs(bx - sx) for (sx, sy), (bx, by) in s)
    lo_x = min(sx for (sx, sy), (bx, by) in s)
    hi_x = max(sx for (sx, sy), (bx, by) in s)
    b_range_y = max(abs(by - sy) for (sx, sy), (bx, by) in s)
    lo_y = min(sy for (sx, sy), (bx, by) in s)
    hi_y = max(sy for (sx, sy), (bx, by) in s)
    # return b_range_x, lo_x, hi_x
    # n = set()
    # for i in range(lo_x - b_range_x, hi_x + b_range_x + 1):
    #     for j in range(lo_y - b_range_y, hi_y + b_range_y + 1):
    #         y = j
    #         x = i
    #         for sen, b in s:
    #             sx, sy = sen
    #             bx, by = b
    #             dist = abs(sx - bx) + abs(sy - by)
    #             dist2 = abs(sx - x) + abs(sy - y)
    #             if dist2 <= dist and not (x == bx and y == by):
    #                 n.add((x, y))
    #                 break
    # 4797228
    # print(b_range_x, lo_x, hi_x)
    # print(n)
    n = set(((bx,by) for (sx,sy),(bx,by) in s))
    r = 4000000
    r = 20

    n = set()
    DP = {}
    for sen, b in s:
        sx, sy = sen
        bx, by = b
        dist2 = abs(sx - bx) + abs(sy - by)
        q = [(sx,sy, dist2)]
        while q:
            # print(len(q))
            x,y,dist = q.pop()
            if dist < 0:
                continue
            k = (x,y)
            if k in DP and DP[k] >= dist:
                continue
            DP[k] = dist
            n.add((x,y))
            D = [(0,-1), (0,1), (-1,0), (1,0)]
            for dx,dy in D:
                q.append((x+dx, y+dy, dist-1))
    print("finished")
    for x in range(r+1):
        for y in range(r+1):
            if (x,y) not in n:
                return x*4000000+y
            # not_pos = False
            # for sen, b in s:
            #     sx, sy = sen
            #     bx, by = b
            #     dist = abs(sx - bx) + abs(sy - by)
            #     dist2 = abs(sx - x) + abs(sy - y)
            #     # if x == 2 and y == 10:
            #         # print(sx,sy,bx,by,dist,dist2)
            #     if dist2 <= dist and not (x == bx and y == by):
            #         not_pos = True
            #         break
            
            # if not not_pos and not (x,y) in n:
            #     # print(x,y)
            #     return x*4000000+y
    assert False
    # return len([1 for x, y in n if y == t])


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
