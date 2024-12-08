# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
from collections import defaultdict
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2024
DAY = 8
EXPECTED_1 = 14
EXPECTED_2 = 34


""" DAY 8 """

def day8_parse(data: list[str]):
    return data

def day8_solve(data, part2):
    data = day8_parse(data)

    R = len(data)
    C = len(data[0])
    antennas = defaultdict(list)
    for r in range(R):
        for c in range(C):
            if data[r][c] != ".":
                antennas[data[r][c]].append((r, c))

    antinodes = set()
    for _, pos in antennas.items():
        i = 0
        while i < len(pos):
            j = i + 1
            while j < len(pos):
                r1, c1 = pos[i]
                r2, c2 = pos[j]
                dr = r2 - r1
                dc = c2 - c1
                multipliers = [1]
                if part2:
                    multipliers = range(100)
                for k in multipliers:
                    new_r = r2 + k*dr
                    new_c = c2 + k*dc
                    if 0 <= new_r < R and 0 <= new_c < C:
                        antinodes.add((new_r,new_c))
                    new_r = r1 - k*dr
                    new_c = c1 - k*dc
                    if 0 <= new_r < R and 0 <= new_c < C:
                        antinodes.add((new_r,new_c))
                j += 1
            i += 1
    return len(antinodes)

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
