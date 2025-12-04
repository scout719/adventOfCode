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
DAY = 4
EXPECTED_1 = 13
EXPECTED_2 = 43

def day4_parse(data: list[str]):
    R = len(data)
    C = len(data[0])
    rolls = set()
    for r in range(R):
        for c in range(C):
            if data[r][c] == "@":
                rolls.add((r, c))

    return rolls

def day4_adj(r, c, rolls):
    total = 0
    D = [-1, 0, 1]
    for dr in D:
        for dc in D:
            if dr == dc == 0:
                continue
            rr, cc = r + dr, c + dc
            if (rr, cc) in rolls:
                total += 1
    return total

def day4_solve(data, part2):
    rolls = day4_parse(data)

    changed = True
    total = 0
    while changed:
        changed = False
        new_rolls = set()

        for r, c in rolls:
            amt = day4_adj(r, c, rolls)
            if amt < 4:
                total += 1
                if part2:
                    changed = True
            else:
                if part2:
                    new_rolls.add((r, c))

        rolls = new_rolls

    return total

def day4_1(data):
    return day4_solve(data, False)

def day4_2(data):
    return day4_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
