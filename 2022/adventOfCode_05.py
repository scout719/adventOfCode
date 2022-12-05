# -*- coding: utf-8 -*-
# pylint: disable=import-error
# pylint: disable=unused-import
# pylint: disable=wildcard-import
# pylint: disable=wrong-import-position
# pylint: disable=consider-using-enumerate
import os
from os.path import join
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402
# pylint: enable=import-error
# pylint: enable=wrong-import-position

YEAR = 2022
DAY = 5
EXPECTED_1 = "CMZ"
EXPECTED_2 = "MCD"


""" DAY 5 """

def day5_parse(data):
    stacks = []
    assert (len(data[0]) + 1) % 4 == 0
    n_stacks = (len(data[0]) + 1) // 4
    stacks = [list() for _ in range(n_stacks)]
    curr_line = 0
    for line in data:
        i = 0
        while i < len(line):
            crate = line[i + 1]
            if crate != " ":
                assert i % 4 == 0
                stack_n = i // 4
                stacks[stack_n].append(crate)
            i += 4

        curr_line += 1
        if line == "":
            break

    for stack in stacks:
        stack.reverse()
        stack.pop(0)

    moves = []
    while curr_line < len(data):
        fst, snd = data[curr_line].split(" from ")
        amount = int(fst.split("move ")[-1])
        from_, to = snd.split(" to ")
        from_ = int(from_)
        to = int(to)
        moves.append((amount, from_, to))
        curr_line += 1

    return stacks, moves

def day5_1(data):
    stacks, moves = day5_parse(data)
    for amount, from_, to in moves:
        for _ in range(amount):
            crate = stacks[from_ - 1].pop()
            stacks[to - 1].append(crate)

    return "".join([s[-1] for s in stacks])

def day5_2(data):
    stacks, moves = day5_parse(data)
    for amount, from_, to in moves:
        crates = []
        for _ in range(amount):
            crate = stacks[from_ - 1].pop()
            crates.append(crate)
        crates.reverse()
        for crate in crates:
            stacks[to - 1].append(crate)

    return "".join([s[-1] for s in stacks])


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
