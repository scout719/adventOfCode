# -*- coding: utf-8 -*-
from collections import deque
from copy import deepcopy
import functools
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable=wrong-import-position
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2016
DAY = 12
EXPECTED_1 = 42
EXPECTED_2 = None

def day12_parse(data: list[str]):
    insts: list[list[str]] = []
    for line in data:
        parts = line.split(" ")
        insts.append(parts)

    return insts

def day12_solve(data, part2):
    data = day12_parse(data)
    insts = data
    regs = {"a": 0, "b": 0, "c": 0, "d": 0}

    if part2:
        regs["c"] = 1

    pc = 0
    while pc < len(insts):
        op = insts[pc][0]
        if op == "cpy":
            x = insts[pc][1]
            y = insts[pc][2]
            value = int(x) if x.isnumeric() else regs[x]
            regs[y] = value
        elif op == "inc":
            x = insts[pc][1]
            regs[x] += 1
        elif op == "dec":
            x = insts[pc][1]
            regs[x] -= 1
        elif op == "jnz":
            x = insts[pc][1]
            y = int(insts[pc][2])
            value = int(x) if x.isnumeric() else regs[x]
            if value != 0:
                pc += y
                continue
        else:
            assert False, insts[pc]
        pc += 1

    return regs["a"]

def day12_1(data):
    # wrong 23
    # wrong 21
    return day12_solve(data, False)

def day12_2(data):
    return day12_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
