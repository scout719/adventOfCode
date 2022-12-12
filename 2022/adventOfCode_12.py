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
DAY = 12
EXPECTED_1 = 31
EXPECTED_2 = 29


""" DAY 12 """

def day12_parse(data):
    grid = []
    for line in data:
        grid.append([c for c in line])
    return grid

def day12_compute(data):
    grid = day12_parse(data)
    R = len(grid)
    C = len(grid[0])
    D = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    end = (0, 0)
    start = (0,0)
    a_s = set()
    for r in range(R):
        for c in range(C):
            if grid[r][c] == "S":
                start = (r, c)
            elif grid[r][c] == "E":
                end = (r, c)
            elif grid[r][c] == "a":
                a_s.add((r,c))

    q = [(0, end)]
    visited = set()
    visited_m = defaultdict(int)
    grid[end[0]][end[1]] = chr(ord('z')+1)
    grid[start[0]][start[1]] = chr(ord('a')-1)
    while q:
        x = heappop(q)
        next_s, next_p = x
        r, c = next_p
        if (next_p) in visited_m and 0 < visited_m[next_p] <= next_s:
            continue
        visited.add(next_p)
        visited_m[next_p] = next_s
        curr = grid[r][c]
        for dr, dc in D:
            rr = r + dr
            cc = c + dc
            if 0<= rr <R and 0<=cc<C:
                if ord(grid[rr][cc]) - ord(curr) >= -1:
                    heappush(q, (next_s + 1, (rr, cc)))
    return visited_m, start, a_s

def day12_1(data):
    visited_m, start,_ = day12_compute(data)
    return visited_m[start]

def day12_2(data):
    visited_m, _, a_s = day12_compute(data)
    mins = set()
    for r,c in a_s:
        if (r,c) in visited_m:
            mins.add(visited_m[(r,c)])

    return min(mins)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
