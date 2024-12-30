# -*- coding: utf-8 -*-
from collections import deque
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable=wrong-import-position
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2016
DAY = 25
EXPECTED_1 = None
EXPECTED_2 = None

def day25_parse(data: list[str]):
    insts: list[list[str]] = []
    for line in data:
        parts = line.split(" ")
        insts.append(parts)

    return insts

def day25_solve(data, part2):
    data = day25_parse(data)
    insts = data
    regs = {"a": 0, "b": 0, "c": 0, "d": 0}

    if part2:
        return "Merry Xmas! 🎅🏻"

    for t in range(int(1e9)):
        regs["a"] = t

        pc = 0
        success = True
        next_ = 0
        i = 0
        while success and pc < len(insts):
            op = insts[pc][0]
            if op == "cpy":
                x = insts[pc][1]
                y = insts[pc][2]
                value = int(x) if x.lstrip("-").isnumeric() else regs[x]
                if not y.isnumeric():
                    regs[y] = value
            elif op == "inc":
                x = insts[pc][1]
                regs[x] += 1
            elif op == "dec":
                x = insts[pc][1]
                regs[x] -= 1
            elif op == "jnz":
                x = insts[pc][1]
                y = insts[pc][2]
                value_x = int(x) if x.lstrip("-").isnumeric() else regs[x]
                value_y = int(y) if y.lstrip("-").isnumeric() else regs[y]
                if value_x != 0:
                    pc += value_y
                    continue
            elif op == "out":
                x = insts[pc][1]
                value = int(x) if x.lstrip("-").isnumeric() else regs[x]
                if value != next_:
                    success = False
                else:
                    i += 1
                    next_ = (next_ + 1) % 2
                    if i > int(100):
                        return t
            else:
                assert False, insts[pc]
            pc += 1

    assert False

def day25_1(data):
    return day25_solve(data, False)

def day25_2(data):
    return day25_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
