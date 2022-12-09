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
DAY = 9
EXPECTED_1 = 88
EXPECTED_2 = 36


""" DAY 9 """

def day9_parse(data):
    x = []
    for line in data:
        d, a = line.split(" ")
        a = int(a)
        x.append((d, a))
    return x

def day9_board(rope):
    min_r = min([r for r, c in rope])
    max_r = max([r for r, c in rope])
    min_c = min([c for r, c in rope])
    max_c = max([c for r, c in rope])

    for r in range(min_r, max_r + 1):
        line = ""
        for c in range(min_c, max_c + 1):
            ch = "."
            if (r, c) in rope:
                ch = str(rope.index((r, c)))
            line += ch
        print(line)
    print()
    time.sleep(1)

def day9_move(rope):
    i = 0
    while i < len(rope) - 1:
        h = rope[i]
        t = rope[i + 1]

        if abs(h[0]-t[0]) == 2:
            dr = (h[0]-t[0])/abs(h[0]-t[0])
            dc = 0
            if abs(h[1]-t[1]) >= 1:
                dc = (h[1]-t[1])/abs(h[1]-t[1])
            t = (t[0] +dr, t[1]+dc)
        elif abs(h[1]-t[1]) == 2:
            dc = (h[1]-t[1])/abs(h[1]-t[1])
            dr = 0
            if abs(h[0]-t[0]) >= 1:
                dr = (h[0]-t[0])/abs(h[0]-t[0])
            t = (t[0] +dr, t[1]+dc)
        rope[i] = h
        rope[i + 1] = t
        i += 1
    return rope

def day9_1(data):
    data = day9_parse(data)
    h = (0, 0)
    t = (0, 0)
    v = set()
    for d, amt in data:
        for _ in range(amt):
            if d == "U":
                h = (h[0] - 1, h[1])
                if abs(t[0] - h[0]) == 2:
                    t = (t[0] - 1, h[1])
            elif d == "D":
                h = (h[0] + 1, h[1])
                if abs(t[0] - h[0]) == 2:
                    t = (t[0] + 1, h[1])
            elif d == "R":
                h = (h[0], h[1] + 1)
                if abs(t[1] - h[1]) == 2:
                    t = (h[0], t[1] + 1)
            elif d == "L":
                h = (h[0], h[1] - 1)
                if abs(t[1] - h[1]) == 2:
                    t = (h[0], t[1] - 1)
            v.add(t)
    return len(v)

def day9_2(data):
    data = day9_parse(data)
    rope = [(0, 0) for _ in range(10)]
    v = set([rope[-1]])
    for d, amt in data:
        for _ in range(amt):
            h = rope[0]
            if d == "U":
                h = (h[0] - 1, h[1])
            elif d == "D":
                h = (h[0] + 1, h[1])
            elif d == "R":
                h = (h[0], h[1] + 1)
            elif d == "L":
                h = (h[0], h[1] - 1)
            rope[0] = h
            rope = day9_move(rope)

            v.add(rope[-1])
    # 2128
    return len(v)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
