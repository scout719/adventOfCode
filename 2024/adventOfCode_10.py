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
DAY = 10
EXPECTED_1 = 36
EXPECTED_2 = 81


""" DAY 10 """

def day10_parse(data: list[str]):
    return [[int(c) for c in l] for l in data]

def day10_solve(data, part2):
    grid = day10_parse(data)
    starts = defaultdict(list)
    D = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    R = len(grid)
    C = len(grid[0])
    q = []
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 0:
                q.append((r, c, r, c))
    while q:
        start_r, start_c, r, c = q.pop()
        if grid[r][c] == 9:
            starts[(start_r, start_c)].append((r, c))
        for dr, dc in D:
            rr, cc = r + dr, c + dc
            if 0 <= rr < R and 0 <= cc < C and grid[rr][cc] == grid[r][c] + 1:
                q.append((start_r, start_c, rr, cc))

    return sum(len(s if part2 else set(s)) for _, s in starts.items())

def day10_1(data):
    return day10_solve(data, False)

def day10_2(data):
    return day10_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
