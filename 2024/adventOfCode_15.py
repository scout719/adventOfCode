# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2024
DAY = 15
EXPECTED_1 = 10092
EXPECTED_2 = 368

def day15_parse(data: list[str]):
    grid = []
    i = 0
    while data[i]:
        grid.append(list(data[i]))
        i += 1
    i += 1

    moves = []
    for l in data[i:]:
        for m in l:
            M = {
                "v": (1, 0),
                "^": (-1, 0),
                ">": (0, 1),
                "<": (0, -1)}
            moves.append(M[m])
    return grid, moves

def day15(grid, r, c, dr, dc):
    if grid[r][c] == "#":
        return False
    if grid[r][c] == ".":
        grid[r][c] = "O"
        return True

    assert grid[r][c] == "O"
    moved = day15(grid, r + dr, c + dc, dr, dc)
    if moved:
        grid[r][c] = "O"
    return moved

def day15_solve(data, part2):
    data = day15_parse(data)
    grid, moves = data
    R = len(grid)
    C = len(grid[0])
    s_r, s_c = 0, 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == "@":
                s_r, s_c = r, c
                grid[r][c] = "."
                break
    r, c = s_r, s_c
    for dr, dc in moves:
        rr, cc = r + dr, c + dc
        if grid[rr][cc] == ".":
            r, c = rr, cc
        elif grid[rr][cc] == "O":
            moved = day15(grid, rr, cc, dr, dc)
            if moved:
                grid[rr][cc] = "."
                r, c = rr, cc
    ans = 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == "O":
                ans += r * 100 + c
    return ans

def day15_1(data):
    return day15_solve(data, False)

def day15_2(data):
    return day15_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
