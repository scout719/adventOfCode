# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2025
DAY = 1
EXPECTED_1 = 3
EXPECTED_2 = 6

def day1_parse(data: list[str]):
    return [(-1 if line[0] == 'L' else 1, int(line[1:])) for line in data]

def day1_solve(data, part2):
    moves = day1_parse(data)
    curr = 50
    max_ = 100
    times = 0
    for d, amt in moves:
        for t in range(amt):
            curr = (curr + d) % max_
            if curr == 0:
                if part2 or t == amt - 1:
                    times += 1

        # === Part 1 ===
        # curr = (curr + (d * amt)) % max_
        # if curr == 0:
        #     times += 1

        # === Part 2 Failed attempt ===
        # old = curr
        # curr = (curr + (d * amt)) % max_
        # times += amt // max_
        # if old > curr and d == 1:
        #     times += 1
        # elif old < curr and d == -1:
        #     times += 1
    return times

def day1_1(data):
    return day1_solve(data, False)

def day1_2(data):
    return day1_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
