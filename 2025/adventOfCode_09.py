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
DAY = 9
EXPECTED_1 = 50
EXPECTED_2 = 24

def day9_parse(data: list[str]):
    tiles = []
    for line in data:
        x, y = line.split(",")
        x = int(x)
        y = int(y)
        tiles.append((x, y))
    return tiles

def day9_solve(data, part2):
    tiles = day9_parse(data)

    total = 0
    for i_, (x, y) in enumerate(tiles):
        for j, (xx, yy) in enumerate(tiles):
            if j <= i_:
                continue
            bottom = max(y, yy)
            left = min(x, xx)
            top = min(y, yy)
            right = max(x, xx)

            if (x, y) == (3, 1) and (xx, yy) == (2, 4):
                pass

            dx = (right - left) + 1
            dy = (bottom - top) + 1
            valid = True
            if part2:
                # check if any edge intersects this rectangle
                i = 0
                while i < len(tiles) and valid:
                    x2, y2 = tiles[i]
                    xx2, yy2 = tiles[(i + 1) % len(tiles)]
                    i += 1

                    assert x2 == xx2 or y2 == yy2
                    x2, xx2 = min(x2, xx2), max(x2, xx2)
                    y2, yy2 = min(y2, yy2), max(y2, yy2)

                    # Regarding the 'open' validation on the second part of each condition:
                    # Eg. for the upper side of the rectangle (line X-Y),
                    # if the edge starts at it (point B), but goes upwards (towards A),
                    # it is not crossing the rectangle, since the edges are part of the rectangle
                    # So it shouldn't invalidate the rectangle
                    # Visualization:
                    #       A
                    #       |
                    #  X----B----Y
                    #  |         |
                    #  |         |
                    #
                    # However, if the edge went downwards from B,
                    # it would cross the rectangle (and could even end inside it)
                    # So it should invalidate the rectangle
                    # Visualization:
                    #  X----B----Y
                    #  |    |    |
                    #  |    A    |
                    #  |         |

                    # Cross upper side:
                    if x2 == xx2 and left < x2 < right and y2 <= top < yy2:
                        valid = False
                    # Cross bottom side:
                    if x2 == xx2 and left < x2 < right and y2 < bottom <= yy2:
                        valid = False
                    # Cross left side:
                    if y2 == yy2 and top < y2 < bottom and x2 <= left < xx2:
                        valid = False
                    # Cross right side:
                    if y2 == yy2 and top < y2 < bottom and x2 < right <= xx2:
                        valid = False
            if valid:
                total = max(total, dx * dy)

    # low 1568657670
    return total

def day9_1(data):
    return day9_solve(data, False)

def day9_2(data):
    return day9_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
