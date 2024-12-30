# -*- coding: utf-8 -*-
from collections import deque
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable=wrong-import-position
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2016
DAY = 24
EXPECTED_1 = 14
EXPECTED_2 = None

def day24_parse(data: list[str]):
    grid = [list(line) for line in data]
    pos = {}
    walls = set()
    for r, line in enumerate(data):
        for c, char in enumerate(line):
            if char.isnumeric():
                pos[int(char)] = (r, c)
                grid[r][c] = "."
            elif char == "#":
                walls.add((r, c))
    return grid, pos, walls

def day24_solve(data, part2):
    data = day24_parse(data)
    grid, pos, walls = data
    r_pos = {v: k for k, v in pos.items()}
    R = len(grid)
    C = len(grid[0])

    sr, sc = pos[0]
    seen = set()
    q = deque()
    q.append((0, {0}, sr, sc))
    while q:
        steps, visited, r, c = q.popleft()
        key = (tuple(sorted(visited)), r, c)
        if key in seen:
            continue
        seen.add(key)

        if (r, c) in r_pos:
            visited.add(r_pos[(r, c)])

        if len(visited) == len(pos.keys()):
            if not part2:
                return steps
            else:
                if (r, c) == (sr, sc):
                    return steps

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            rr, cc = r + dr, c + dc
            if not (0 <= rr < R and 0 <= cc < C) or (rr, cc) in walls:
                continue
            q.append((steps + 1, set(visited), rr, cc))
    assert False

def day24_1(data):
    return day24_solve(data, False)

def day24_2(data):
    return day24_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
