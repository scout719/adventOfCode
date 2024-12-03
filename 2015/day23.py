# -*- coding: utf-8 -*-
from heapq import heappop, heappush
from math import ceil, cos, sqrt
import os
import sys
from typing import Counter

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable=wrong-import-position
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2015
DAY = 23
EXPECTED_1 = 0
EXPECTED_2 = None


""" DAY 23 """

def day23_parse(data: list[str]):
    insts = []
    for l in data:
        parts = l.split()
        inst = parts[0]
        r = None
        offset = None
        if inst in ["jie", "jio"]:
            r, offset = parts[1].strip(","), int(parts[2].replace("+", ""))
        elif inst in ["hlf", "tpl", "inc"]:
            r = parts[1]
        else:
            assert inst in ["jmp"]
            offset = int(parts[1].replace("+", ""))

        insts.append((inst, r, offset))

    return insts

def day23_solve(data, part2):
    insts = day23_parse(data)
    a, b = 0, 0
    if part2:
        a = 1
    i = 0
    while i < len(insts):
        inst, r, offset = insts[i]
        step = 1
        if inst == "hlf":
            if r == "a":
                a //= 2
            else:
                assert r == "b"
                b //= 2
        elif inst == "tpl":
            if r == "a":
                a *= 3
            else:
                assert r == "b"
                b *= 3
        elif inst == "inc":
            if r == "a":
                a += 1
            else:
                assert r == "b"
                b += 1
        elif inst == "jmp":
            step = offset
        elif inst == "jie":
            if r == "a" and a % 2 == 0:
                step = offset
            elif r == "b" and b % 2 == 0:
                step = offset
        elif inst == "jio":
            if r == "a" and a == 1:
                step = offset
            elif r == "b" and b == 1:
                step = offset
        i += step
    return b

def day23_1(data):
    return day23_solve(data, False)

def day23_2(data):
    return day23_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
