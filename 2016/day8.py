# -*- coding: utf-8 -*-
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable=wrong-import-position
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation, WHITE_SQUARE  # NOQA: E402

YEAR = 2016
DAY = 8
EXPECTED_1 = None
EXPECTED_2 = None

def day8_parse(data: list[str]):
    return data

def day8_print(screen):
    for l in screen:
        line = ""
        for p in l:
            line += WHITE_SQUARE if p else "."
        print(line)
    print()

def day8_solve(data, _):
    data = day8_parse(data)
    screen = [[False for _ in range(50)]for _ in range(6)]
    for inst in data:
        if inst.startswith("rect "):
            a, b = inst.strip("rect ").split("x")
            a, b = int(a), int(b)
            for r in range(b):
                for c in range(a):
                    screen[r][c] = True
        elif inst.startswith("rotate row y="):
            y, amt = inst.strip("rotate row y=").split(" by ")
            y, amt = int(y), int(amt)
            back = [] + screen[y]
            for i, c in enumerate(back):
                screen[y][(i + amt) % len(screen[y])] = c
        elif inst.startswith("rotate column x="):
            x, amt = inst.strip("rotate column x=").split(" by ")
            x, amt = int(x), int(amt)
            back = [screen[i][x] for i in range(len(screen))]
            for i, c in enumerate(back):
                screen[(i + amt) % len(screen)][x] = c

    day8_print(screen)
    return sum([screen[r][c] for c in range(len(screen[r])) for r in range(len(screen))])

def day8_1(data):
    return day8_solve(data, False)

def day8_2(data):
    return day8_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
