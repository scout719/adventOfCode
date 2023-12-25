# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
import os
import sys
from typing import List

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import day_with_validation  # NOQA: E402
from common.utils import main  # NOQA: E402

YEAR = 2023
DAY = 11
EXPECTED_1 = 374
EXPECTED_2 = None


""" DAY 11 """

def day11_parse(data: List[str]):
    return [list(line) for line in data]

def day11_info(img):
    R = len(img)
    C = len(img[0])
    empty_r = []
    for r in range(R):
        if all(img[r][c] == "." for c in range(C)):
            empty_r.append(r)
    empty_c = []
    for c in range(C):
        if all(img[r][c] == "." for r in range(R)):
            empty_c.append(c)
    galaxies = []
    for r in range(R):
        for c in range(C):
            if img[r][c] == "#":
                galaxies.append((r, c))
    return empty_r, empty_c, galaxies

def day11_expand(galaxies, empty_r, empty_c, size):
    for i, r in enumerate(empty_r):
        r = r + i * (size)
        new_gal = []
        for rr, cc in galaxies:
            assert rr != r, r
            if rr > r:
                new_gal.append((rr + size, cc))
            else:
                new_gal.append((rr, cc))
        galaxies = new_gal
    for i, c in enumerate(empty_c):
        c = c + i * size
        new_gal = []
        for rr, cc in galaxies:
            assert cc != c, c
            if cc > c:
                new_gal.append((rr, cc + size))
            else:
                new_gal.append((rr, cc))
        galaxies = new_gal
    return galaxies

def day11_solve(img, size):
    size = size - 1
    empty_r, empty_c, galaxies = day11_info(img)
    galaxies = day11_expand(galaxies, empty_r, empty_c, size)

    ans = []
    for i, (r, c) in enumerate(galaxies):
        for j in range(i + 1, len(galaxies)):
            rr, cc = galaxies[j]
            dist = abs(rr - r) + abs(cc - c)
            if dist > 0:
                # ans = min(ans, dist)
                ans.append(dist)
    # 9530628 high
    # 9529422 high
    return sum(ans)

def day11_1(data):
    img = day11_parse(data)
    return day11_solve(img, 2)

def day11_2(data: List[str]):
    img = day11_parse(data)
    return day11_solve(img, 1000000)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
