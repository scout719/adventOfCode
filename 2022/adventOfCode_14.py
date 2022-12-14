# -*- coding: utf-8 -*-
# pylint: disable=import-error
# pylint: disable=unused-import
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# pylint: disable=wrong-import-position
# pylint: disable=consider-using-enumerate
from ctypes.wintypes import SIZE
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
DAY = 14
EXPECTED_1 = 24
EXPECTED_2 = 93


""" DAY 14 """

def day14_parse(data):
    rocks = []
    for line in data:
        rock = line.split(" -> ")
        rock = [r.split(",") for r in rock]
        rock = [(int(x),int(y)) for x,y in rock]
        rocks.append(rock)
    return rocks

def day14_1(data):
    rocks_ = day14_parse(data)
    rocks = set()
    for r in rocks_:
        i = 0
        while i < len(r)-1:
            sx,sy = r[i]
            nx,ny = r[i+1]
            dx,dy = nx-sx, ny-sy
            if dx != 0:
                dx = dx//abs(dx)
                for xx in range(sx,nx+dx, dx):
                    rocks.add((xx,sy))
            elif dy != 0:
                dy = dy//abs(dy)
                for yy in range(sy,ny+dy, dy):
                    rocks.add((sx,yy))
            i += 1

    s_x, s_y = (500,0)
    max_y = max(y for x,y in rocks)
    r = set()
    D = [(0,1),(-1,1), (1,1)]
    # print(rocks)
    end = False
    while not end:
        c_x,c_y = s_x, s_y
        while True:
            # print(c_x, c_y)
            # if (c_x, c_y) in rocks or (c_x,c_y) in r:
            stopped = True
            for dx, dy in D:
                xx, yy = c_x + dx, c_y + dy
                # print(xx,yy, stopped)
                if (xx,yy) not in rocks and (xx,yy) not in r:
                    stopped = False
                    c_x,c_y = xx,yy
                    break
            if stopped:
                # print(c_x, c_y, stopped)
                r.add((c_x, c_y))
                break
            # c_y += 1
            # print(c_x, c_y, r, max_y)
            if c_y > max_y+1:
                end = True
                break

    return len(r)

def day14_2(data):
    rocks_ = day14_parse(data)
    rocks = set()
    for r in rocks_:
        i = 0
        while i < len(r)-1:
            sx,sy = r[i]
            nx,ny = r[i+1]
            dx,dy = nx-sx, ny-sy
            if dx != 0:
                dx = dx//abs(dx)
                for xx in range(sx,nx+dx, dx):
                    rocks.add((xx,sy))
            elif dy != 0:
                dy = dy//abs(dy)
                for yy in range(sy,ny+dy, dy):
                    rocks.add((sx,yy))
            i += 1

    s_x, s_y = (500,0)
    max_y = max(y for x,y in rocks)
    r = set()
    D = [(0,1),(-1,1), (1,1)]
    # print(rocks)
    end = False
    while not end:
        c_x,c_y = s_x, s_y
        while True:
            # print(c_x, c_y)
            # if (c_x, c_y) in rocks or (c_x,c_y) in r:
            stopped = True
            for dx, dy in D:
                xx, yy = c_x + dx, c_y + dy
                # print(xx,yy, stopped)
                if (xx,yy) not in rocks and (xx,yy) not in r and yy < max_y+2:
                    stopped = False
                    c_x,c_y = xx,yy
                    break
            if stopped:
                if(c_x,c_y) == (500,0):
                    return len(r)+1
                # print(c_x, c_y, stopped)
                r.add((c_x, c_y))
                break
            # c_y += 1
            # print(c_x, c_y, r, max_y)
            # if c_y > max_y+1:
            #     end = True
            #     break

    return len(r)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
