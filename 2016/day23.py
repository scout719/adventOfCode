# -*- coding: utf-8 -*-
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable=wrong-import-position
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2016
DAY = 23
EXPECTED_1 = 3
EXPECTED_2 = None

def day23_parse(data: list[str]):
    insts: list[list[str]] = []
    for line in data:
        parts = line.split(" ")
        insts.append(parts)

    return insts

def day23_solve(data, part2):
    data = day23_parse(data)
    insts = data
    regs = {"a": 0, "b": 0, "c": 0, "d": 0}
    regs["a"] = 7

    if part2:
        # Analized the program
        # tgl changes instructions on even steps counting down from 20
        # (c = 2 * b and b counts down from 10)
        a = 12
        # following loop does:
        a = a * 11 * 10 * 9 * 8 * 7 * 6 * 5 * 4 * 3 * 2 * 1
        # b = a  # cpy a b
        # b -= 1  # dec b
        # while True:
        #     d = a  # cpy a d
        #     # following loop does:
        #     a = a * b
        #     # a = 0  # cpy 0 a
        #     # while True:
        #     #     c = b  # cpy b c
        #     #     # following loop does:
        #     #     a = b
        #     #     # a += 1  # inc a
        #     #     # while True:
        #     #     #     a += 1  # inc a
        #     #     #     c -= 1  # dec c
        #     #     #     if c == 0:  # jnz c -2
        #     #     #         break
        #     #     d -= 1  # dec d
        #     #     if d == 0:  # jnz d -5
        #     #         break
        #     b -= 1  # dec b
        #     c = 2 * b  # cpy b c
        #     d = c  # cpy c d
        #     # tgl c
        #     c = -16  # cpy -16 c

        #     assert b > 0
        #     # loop while b is not 1
        #     # because when b is 1, c will be 2
        #     # and the following instruction will stop be a go to
        #     if b == 1:  # jnz 1 c -> cpy 1 c
        #         c = 1
        #         break

        # following loop does:
        a += 85 * 92
        # c = 85  # cpy 85 c
        # while True:
        #     d = 92  # jnz 92 d -> cpy 92 d
        #     # following loop does a += 92
        #     a += 92
        #     # while True:
        #     #     a += 1  # inc a
        #     #     d -= 1  # inc d -> dec d
        #     #     if d == 0:  # jnz d -2
        #     #         break
        #     c -= 1  # inc c -> dec c
        #     if c == 0:  # jnz c -5
        #         break
        return a

    pc = 0
    while pc < len(insts):
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
        elif op == "tgl":
            x = insts[pc][1]
            value = int(x) if x.lstrip("-").isnumeric() else regs[x]
            if pc + value >= len(insts):
                pc += 1
                continue
            target = insts[pc + value]
            if len(target) == 2:
                if target[0] == "inc":
                    target[0] = "dec"
                else:
                    target[0] = "inc"
            elif len(target) == 3:
                if target[0] == "jnz":
                    target[0] = "cpy"
                else:
                    target[0] = "jnz"
        else:
            assert False, insts[pc]
        pc += 1

    return regs["a"]

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
