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
DAY = 8
EXPECTED_1 = 21
EXPECTED_2 = 8


""" DAY 8 """

def day8_parse(data):
    grid = []
    for line in data:
        grid.append([int(x) for x in line])
    return grid

def day8_blocking_tree(r, c, dr, dc, grid):
    R = len(grid)
    C = len(grid[0])
    tree = grid[r][c]
    rr = r + dr
    cc = c + dc
    while 0 <= rr < R and 0 <= cc < C:
        tree2 = grid[rr][cc]
        if tree2 >= tree:
            break
        rr += dr
        cc += dc
    return rr, cc

def day8_1(data):
    grid = day8_parse(data)
    R = len(grid)
    C = len(grid[0])
    D = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    visible = [[False for _ in range(C)] for _ in range(R)]
    for r in range(R):
        for c in range(C):
            for dr, dc in D:
                rr, cc = day8_blocking_tree(r, c, dr, dc, grid)
                if not (0 <= rr < R and 0 <= cc < C):
                    # Went out of bounds
                    visible[r][c] = True

    ans = 0
    for r in range(R):
        for c in range(C):
            if visible[r][c]:
                ans += 1
    return ans

def day8_2(data):
    grid = day8_parse(data)
    R = len(grid)
    C = len(grid[0])
    D = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    total = [[1 for _ in range(C)] for _ in range(R)]
    for r in range(R):
        for c in range(C):
            for dr, dc in D:
                rr, cc = day8_blocking_tree(r, c, dr, dc, grid)
                if not (0 <= rr < R and 0 <= cc < C):
                    # Went out of bounds
                    rr -= dr
                    cc -= dc
                total[r][c] *= abs(rr - r) * dr + abs(cc - c) * dc

    ans = 0
    for r in range(R):
        for c in range(C):
            if total[r][c] > ans:
                ans = total[r][c]
    return ans


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
