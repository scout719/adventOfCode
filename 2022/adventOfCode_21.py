# -*- coding: utf-8 -*-
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable-next=wrong-import-position
from common.utils import main, day_with_validation  # NOQA: E402

YEAR = 2022
DAY = 21
EXPECTED_1 = 152
EXPECTED_2 = 301

""" DAY 21 """

def day21_parse(data):
    monkeys = []
    for line in data:
        # drzm: hmdt - zczc
        # hmdt: 32
        monkey = line.split(":")[0]
        words = line.split()
        if len(words) == 2:
            op = [int(words[1])]
        else:
            op = words[1:]
        monkeys.append((monkey, op))
    return monkeys

def day21_1(data):
    monkeys = day21_parse(data)
    return day21_get_root(monkeys, {}, 1)

def day21_get_root(monkeys, values, part):
    if part == 2:
        monkeys = [(monkey, op)
                   for monkey, op in monkeys if monkey not in ["humn"]]

    for (monkey, op) in monkeys:
        if len(op) == 1:
            values[monkey] = op[0]

    while True:
        for (monkey, op) in monkeys:
            if len(op) == 1:
                continue
            if monkey in values:
                continue
            l, op, r = op
            if part == 2:
                if monkey == "root" and l in values:
                    values[r] = values[l]
                    return values[l]
                if monkey == "root" and r in values:
                    values[l] = values[r]
                    return values[r]
            if l in values and r in values:
                l = values[l]
                r = values[r]
                if op == "+":
                    values[monkey] = l + r
                if op == "-":
                    values[monkey] = l - r
                if op == "*":
                    values[monkey] = l * r
                if op == "/":
                    values[monkey] = l // r
                if monkey == "root" and part == 1:
                    return values[monkey]

def day21_solve_humn(monkeys, values):
    while True:
        for monkey, op in monkeys:
            if len(op) == 1:
                continue
            l, op, r = op
            if monkey in values and l in values and not r in values:
                l = values[l]
                if op == "+":
                    values[r] = values[monkey] - l
                if op == "-":
                    values[r] = l - values[monkey]
                if op == "*":
                    values[r] = values[monkey] // l
                if op == "/":
                    values[r] = l // values[monkey]
                if r == "humn":
                    return values[r]
            if monkey in values and r in values and not l in values:
                r = values[r]
                if op == "+":
                    values[l] = values[monkey] - r
                if op == "-":
                    values[l] = values[monkey] + r
                if op == "*":
                    values[l] = values[monkey] // r
                if op == "/":
                    values[l] = values[monkey] * r
                if l == "humn":
                    return values[l]

def day21_2(data):
    monkeys = day21_parse(data)

    values = {}
    monkeys = [(monkey, op)
               for monkey, op in monkeys if monkey not in ["humn"]]

    day21_get_root(monkeys, values, 2)
    return day21_solve_humn(monkeys, values)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
