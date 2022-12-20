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
DAY = 10
EXPECTED_1 = 13140

EXPECTED_2 = ""

""" DAY 9 """

def day10_parse(data):
    inst = []
    for line in data:
        op = line.split()
        inst.append(op)
    return inst

def day10_cycle(x, val, p1, p2):
    if len(p1) > 0:
        x += p1.pop()
    p1 = p2
    p2 = [val]

    return x, p1, p2

def day10_draw(cycle, x, display):
    if not display:
        return

    sprite = [x in [c - 1, c, c + 1] for c in range(40)]
    r = (cycle - 1) // 40
    c = (cycle - 1) % 40
    if sprite[c]:
        display[r][c] = WHITE_SQUARE

def day10_print(display):
    for r in range(len(display)):
        line = ""
        for c in range(len(display[r])):
            line += display[r][c]
        print(line)
    print()

def day10_1(data):
    insts = day10_parse(data)
    x = 1
    cycle = 0
    p_1 = []
    p_2 = []
    total = 0
    for op in insts:
        if (cycle - 20) % 40 == 0:
            total += cycle * x
        if len(op) > 1:
            _, val = op
            val = int(val)
            x, p_1, p_2 = day10_cycle(x, val, p_1, p_2)
            cycle += 1
            if (cycle - 20) % 40 == 0:
                total += cycle * x
        x, p_1, p_2 = day10_cycle(x, 0, p_1, p_2)
        cycle += 1
    # 7040
    return total

def day10_2(data):
    insts = day10_parse(data)
    x = 1
    cycle = 0
    p_1 = []
    p_2 = []
    display = [[" " for _ in range(40)] for _ in range(6)]
    for op in insts:
        day10_draw(cycle, x, display)

        if len(op) > 1:
            _, val = op
            val = int(val)
            x, p_1, p_2 = day10_cycle(x, val, p_1, p_2)
            cycle += 1
            day10_draw(cycle, x, display)

        x, p_1, p_2 = day10_cycle(x, 0, p_1, p_2)
        cycle += 1

    day10_print(display)
    return ""


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
