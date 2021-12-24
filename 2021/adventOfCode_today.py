# -*- coding: utf-8 -*-
# pylint: disable=import-error
# pylint: disable=unused-import
# pylint: disable=wildcard-import
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
from common.utils import read_input, main, clear  # NOQA: E402
from common.utils import day_with_validation, bcolors, WHITE_CIRCLE, WHITE_SQUARE  # NOQA: E402
from common.utils import BLUE_CIRCLE, RED_SMALL_SQUARE  # NOQA: E402
# pylint: enable=import-error
# pylint: enable=wrong-import-position

YEAR = 2021
DAY = 24
EXPECTED_1 = None
EXPECTED_2 = None


""" DAY 24 """

def day24_parse(data):
    P = []
    ops = []
    for line in data:
        parts = line.split(" ")
        inst = parts[0]
        op = ()
        if len(parts) == 2:
            P.append(ops)
            ops = []
            op = (inst, parts[1])
        else:
            assert len(parts) == 3
            snd = int(parts[2]) if parts[2].lstrip("-").isdigit() else parts[2]
            op = (inst, parts[1], snd)
        ops.append(op)
    P.append(ops)
    return P[1:]

def day24_resolve(b, mem):
    if isinstance(b, int):
        return b
    else:
        return mem[b]

def day24_exec(op, mem, inp):
    inst = op[0]
    if inst == "inp":
        mem[op[1]] = inp.pop()
    elif inst == "add":
        b = day24_resolve(op[2], mem)
        a = day24_resolve(op[1], mem)
        mem[op[1]] = a + b
    elif inst == "mul":
        b = day24_resolve(op[2], mem)
        a = day24_resolve(op[1], mem)
        mem[op[1]] = a * b
    elif inst == "div":
        b = day24_resolve(op[2], mem)
        a = day24_resolve(op[1], mem)
        mem[op[1]] = a // b
    elif inst == "mod":
        b = day24_resolve(op[2], mem)
        a = day24_resolve(op[1], mem)
        mem[op[1]] = a % b
    elif inst == "eql":
        b = day24_resolve(op[2], mem)
        a = day24_resolve(op[1], mem)
        if a == b:
            mem[op[1]] = 1
        else:
            mem[op[1]] = 0

def day24_generate(d):
    if d == 0:
        return [d for d in range(1, 10)]
    nums = []
    for i in range(1, 10):
        for n in day24_generate(d - 1):
            nums.append(i + n)
    return nums

def day24_solve(P):
    opts = day24_generate(13)
    return len(opts)
    while True:
        mem = {"w": 0, "x": 0, "y": 0, "z": 0}
        v = ""
        for _ in range(14):
            for c in range(1, 10):
                for op in P:
                    day24_exec(op, mem, [c])
                    if mem["z"]:
                        pass


def day24_1(data):
    data = day24_parse(data)
    return data

def day24_2(data):
    data = day24_parse(data)
    return None


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
