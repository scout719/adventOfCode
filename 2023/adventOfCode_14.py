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
DAY = 14
EXPECTED_1 = 136
EXPECTED_2 = 64

""" DAY 14 """

def day14_parse(data: List[str]):
    return data

def day14_tilt(R, C, bould, square, dr, dc):
    n_bould = []
    # we need to sort on the opposite direction
    bould = sorted(bould, key=lambda e: -dr * e[0] + -dc * e[1])
    for r, c in bould:
        rr = r + dr
        cc = c + dc
        while 0 <= rr < R and 0 <= cc < C and (rr, cc) not in square and (rr, cc) not in n_bould:
            rr += dr
            cc += dc
        # we reached an invalid pos, go back once
        rr -= dr
        cc -= dc
        n_bould.append((rr, cc))
    assert len(bould) == len(
        n_bould), f"bould={sorted(bould)} n_bould={n_bould}"
    return n_bould

def day14_solve(grid, part2):
    R = len(grid)
    C = len(grid[0])
    bould = []
    square = set()
    for r in range(R):
        for c in range(C):
            if grid[r][c] == "O":
                bould.append((r, c))
            elif grid[r][c] == "#":
                square.add((r, c))
            else:
                assert grid[r][c] == "."
    if not part2:
        n_bould = day14_tilt(R, C, bould, square, -1, 0)
    else:
        n_bould = bould
        seen = {}
        seen_rev = {}
        cycles = 1000000000
        for i in range(cycles):
            k = tuple(n_bould)
            if k in seen:
                remaining = cycles - i
                size = i - seen[k]
                left = remaining % size
                target = seen[k] + left
                n_bould = seen_rev[target]
                break
            seen[k] = i
            seen_rev[i] = n_bould
            n_bould = day14_tilt(R, C, n_bould, square, -1, 0)
            n_bould = day14_tilt(R, C, n_bould, square, 0, -1)
            n_bould = day14_tilt(R, C, n_bould, square, 1, 0)
            n_bould = day14_tilt(R, C, n_bould, square, 0, 1)

    return sum(R - r for r, c in n_bould)

def day14_1(data):
    grid = day14_parse(data)
    return day14_solve(grid, False)

def day14_2(data: List[str]):
    grid = day14_parse(data)
    return day14_solve(grid, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
