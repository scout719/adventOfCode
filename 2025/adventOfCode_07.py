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
DAY = 7
EXPECTED_1 = 21
EXPECTED_2 = 40

def day7_parse(data: list[str]):
    grid = data
    start = data[0].find("S")
    return grid, start

def day7_timelines(DP, splits, grid, r, c):
    C = len(grid[0])
    if not 0 <= c < C:
        return 0

    if r >= len(grid):
        return 1

    if (r, c) in DP:
        return DP[(r, c)]

    total = 0
    if grid[r][c] == "^":
        splits.add((r, c))
        total = day7_timelines(DP, splits, grid, r, c - 1) + \
            day7_timelines(DP, splits, grid, r, c + 1)
    else:
        total = day7_timelines(DP, splits, grid, r + 1, c)

    DP[(r, c)] = total
    return total


def day7_solve(data, part2):
    grid, start = day7_parse(data)

    splits = set()
    res_part2 = day7_timelines({}, splits, grid, 0, start)

    return res_part2 if part2 else len(splits)

    # original part1
    # R = len(grid)
    # C = len(grid[0])
    # q: list[tuple[int, int]] = [(0, start)]
    # seen = set()
    # total = 0
    # while q:
    #     r, c = q.pop()
    #     if not (0 <= r < R and 0 <= c < C):
    #         continue
    #     if (r, c) in seen:
    #         continue
    #     seen.add((r, c))

    #     if grid[r][c] == "^":
    #         total += 1
    #         q.append((r, c - 1))
    #         q.append((r, c + 1))

    #     else:
    #         q.append((r + 1, c))

    # return total

def day7_1(data):
    return day7_solve(data, False)

def day7_2(data):
    return day7_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
