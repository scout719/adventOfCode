# -*- coding: utf-8 -*-
# pylint: disable=import-error
# pylint: disable=unused-import
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# pylint: disable=wrong-import-position
# pylint: disable=consider-using-enumerate
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main, day_with_validation  # NOQA: E402
# pylint: enable=import-error
# pylint: enable=wrong-import-position

YEAR = 2022
DAY = 14
EXPECTED_1 = 24
EXPECTED_2 = 93


""" DAY 14 """

def day14_parse(data):
    rocks = []
    for line in data:
        rock = line.split(" -> ")
        rock = [r.split(",") for r in rock]
        rock = [(int(x), int(y)) for x, y in rock]
        rocks.append(rock)
    return rocks

def day14_solve(data, part2):
    rocks_lines = day14_parse(data)
    rocks = set()
    # Build the rock lines
    for rock_line in rocks_lines:
        i = 0
        while i < len(rock_line) - 1:
            start_x, start_y = rock_line[i]
            end_x, end_y = rock_line[i + 1]
            dx, dy = end_x - start_x, end_y - start_y
            if dx != 0:
                dx = dx // abs(dx)
                for xx in range(start_x, end_x + dx, dx):
                    rocks.add((xx, start_y))
            elif dy != 0:
                dy = dy // abs(dy)
                for yy in range(start_y, end_y + dy, dy):
                    rocks.add((start_x, yy))
            i += 1

    start_x, start_y = (500, 0)
    max_y = max(y for x, y in rocks)
    rested = set()
    D = [(0, 1), (-1, 1), (1, 1)]
    while True:
        x, y = start_x, start_y
        keep_falling = True
        while keep_falling:
            clear = False
            for dx, dy in D:
                xx, yy = x + dx, y + dy
                if (xx, yy) not in rocks and (xx, yy) not in rested:
                    if part2 and yy == max_y + 2:
                        continue
                    clear = True
                    x, y = xx, yy
                    break
            keep_falling = clear and y < max_y + 3
        if y == max_y + 3:
            assert not part2
            return len(rested)
        else:
            rested.add((x, y))
            if part2 and (x, y) == (500, 0):
                return len(rested)


def day14_1(data):
    return day14_solve(data, part2=False)

def day14_2(data):
    return day14_solve(data, part2=True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
