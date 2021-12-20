# -*- coding: utf-8 -*-
# pylint: disable=import-error
# pylint: disable=unused-import
# pylint: disable=wildcard-import
# pylint: disable=wrong-import-position
# pylint: disable=consider-using-enumerate
import functools
import math
import os
from os.path import join
import sys
import time
from copy import deepcopy
from collections import Counter, defaultdict, deque
from heapq import heappop, heappush
from typing import ChainMap

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import read_input, main, clear  # NOQA: E402
from common.utils import day_with_validation, bcolors, WHITE_CIRCLE, WHITE_SQUARE  # NOQA: E402
from common.utils import BLUE_CIRCLE, RED_SMALL_SQUARE  # NOQA: E402
# pylint: enable=import-error
# pylint: enable=wrong-import-position

YEAR = 2021
DAY = 20
EXPECTED_1 = 35
EXPECTED_2 = None


""" DAY 20 """

def day20_parse(data):
    algo = data[0]

    img = []
    for line in data[2:]:
        img.append(line)

    return algo, img

def day20_get_pixel(algo, r, c, G, min_r, max_r, min_c, max_c, outside_lit):
    DR = [-1, 0, 1]
    DC = [-1, 0, 1]
    n = ""
    for dr in DR:
        for dc in DC:
            rr, cc = r + dr, c + dc

            if not (min_r <= rr <= max_r and min_c <= cc <= max_c):
                if outside_lit:
                    n += "1"
                else:
                    n += "0"
                continue
            if G[(rr, cc)]:
                n += "1"
            else:
                n += "0"
    v = int(n, 2)
    return algo[v]

def day20_print(G, R, C, extra, real, outside_lit):
    counter = 0
    for r in range(-extra, R + extra):
        line = ""
        for c in range(-extra, C + extra):
            if not (-real <= r < R + real and -real <= c < C + real):
                if outside_lit:
                    line += "#"
                    counter += 1
                else:
                    line += " "
                continue

            if G[(r, c)]:
                line += "#"
                counter += 1
            else:
                line += " "
        print(line + "|")
    print(counter)

def day20_1(data):
    # 5698 wrong
    # 5570 wrong
    # 5930 wrong
    # 5702 wrong
    algo, img = day20_parse(data)

    R = len(img)
    C = len(img[0])
    extra_r = 5
    extra_c = 5
    curr_min_r = 0
    curr_max_r = R - 1
    curr_min_c = 0
    curr_max_c = C - 1

    # print(img)
    # return

    G = defaultdict(bool)
    for r in range(R):
        for c in range(C):
            # print(r,c)

            if img[r][c] == "#":
                G[(r, c)] = True

    outside_lit = False
#######
    for t in range(2):
        G2 = defaultdict(bool)
        for r in range(curr_min_r - 1, curr_max_r + 2):
            for c in range(curr_min_c - 1, curr_max_c + 2):
                p = day20_get_pixel(algo, r, c, G, curr_min_r,
                                    curr_max_r, curr_min_c, curr_max_c, outside_lit)
                if p == "#":
                    G2[(r, c)] = True
        extra_r += 1
        extra_c += 1
        curr_min_r -= 1
        curr_max_r += 1
        curr_min_c -= 1
        curr_max_c += 1
        G = G2
        if algo[0] == "#":
            outside_lit = not outside_lit
        day20_print(G, R, C, extra_r, abs(curr_min_r), outside_lit)

    count = 0
    for r in range(-extra_r, R + extra_r + 1):
        for c in range(-extra_c, C + extra_c + 1):
            if G[(r, c)]:
                count += 1
    return count

def day20_2(data):
    data = day20_parse(data)
    return None


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
