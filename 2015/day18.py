# -*- coding: utf-8 -*-
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable=wrong-import-position
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2015
DAY = 18
EXPECTED_1 = 4
EXPECTED_2 = 17


""" DAY 18 """

def day18_parse(data):
    lights = set()
    for r, row in enumerate(data):
        for c, col in enumerate(row):
            if col == "#":
                lights.add((r, c))

    return lights

def day18_1(data):
    lights = day18_parse(data)
    R = C = 100
    T = 100
    if len(lights) < 20:
        R = C = 6
        T = 4

    D = [-1, 0, 1]
    for _ in range(T):
        new_lights = set()
        for r in range(R):
            for c in range(C):
                neighbors_on = 0
                for dr in D:
                    for dc in D:
                        if dc == dr == 0:
                            continue
                        rr, cc = r + dr, c + dc
                        if (rr, cc) in lights:
                            neighbors_on += 1

                if (r, c) in lights and 2 <= neighbors_on <= 3:
                    new_lights.add((r, c))
                elif (r, c) not in lights and neighbors_on == 3:
                    new_lights.add((r, c))
        lights = new_lights
    return len(lights)

def day18_2(data):
    lights = day18_parse(data)
    R = C = 100
    T = 100
    if len(lights) < 20:
        R = C = 6
        T = 5

    corners = [(0, 0), (0, C - 1), (R - 1, 0), (R - 1, C - 1)]
    for r, c in corners:
        lights.add((r, c))

    D = [-1, 0, 1]
    for _ in range(T):
        new_g = set()
        for r in range(R):
            for c in range(C):
                neighbors_on = 0
                for dr in D:
                    for dc in D:
                        if dc == dr == 0:
                            continue
                        rr, cc = r + dr, c + dc
                        if (rr, cc) in lights:
                            neighbors_on += 1

                if (r, c) in lights and 2 <= neighbors_on <= 3:
                    new_g.add((r, c))
                elif (r, c) not in lights and neighbors_on == 3:
                    new_g.add((r, c))
                elif (r, c) in corners:
                    new_g.add((r, c))
        lights = new_g
    return len(lights)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
