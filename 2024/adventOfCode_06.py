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
DAY = 6
EXPECTED_1 = 41
EXPECTED_2 = 6


""" DAY 6 """

def day6_parse(data: list[str]):
    return data

def day6_walk(data, start_r, start_c, start_d, obstacle_r, obstacle_c):
    R, C = len(data), len(data[0])
    D = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    r, c, d = start_r, start_c, start_d
    dr, dc = D[start_d]
    visited = set([(r, c, start_d)])
    while True:
        rr, cc = r + dr, c + dc
        if not (0 <= rr < R and 0 <= cc < C):
            return (False, set((r, c) for r, c, _ in visited))
        if data[rr][cc] == "#" or (rr, cc) == (obstacle_r, obstacle_c):
            d = (d + 1) % 4
            dr, dc = D[d]
        else:
            r, c = rr, cc
        if (r, c, d) in visited:
            return (True, set())
        visited.add((r, c, d))

def day6_solve(data, part2):
    data = day6_parse(data)
    R, C = len(data), len(data[0])
    start_r, start_c, start_d = 0, 0, 0
    dirs = [">", "v", "<", "^"]
    for r in range(R):
        for c in range(C):
            if data[r][c] in dirs:
                start_r, start_c, start_d = r, c, dirs.index(data[r][c])

    _, visited = day6_walk(data, start_r, start_c, start_d, -1, -1)

    if not part2:
        return len(visited)

    p2 = 0
    for obstacle_r, obstacle_c in visited:
        if (obstacle_r, obstacle_c) == (start_r, start_c):
            continue
        looped, _ = day6_walk(data, start_r, start_c,
                              start_d, obstacle_r, obstacle_c)
        if looped:
            p2 += 1

    return p2

def day6_1(data):
    return day6_solve(data, False)

def day6_2(data):
    return day6_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
