# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
import os
import sys
from typing import List, Mapping, Tuple

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import day_with_validation  # NOQA: E402
from common.utils import main  # NOQA: E402

YEAR = 2023
DAY = 10
EXPECTED_1 = None
EXPECTED_2 = 10


""" DAY 10 """

def day10_parse(data: List[str]):
    return [[x for x in line] for line in data]

def day10_delta(pipe):
    M: Mapping[str, Tuple[Tuple[int, int], Tuple[int, int]]] = {
        "|": ((-1, 0), (1, 0)),
        "-": ((0, -1), (0, 1)),
        "L": ((-1, 0), (0, 1)),
        "J": ((-1, 0), (0, -1)),
        "7": ((1, 0), (0, -1)),
        "F": ((1, 0), (0, 1))
    }
    return M[pipe]

def day10_guess(grid):
    if len(grid) == 5:
        return "F"
    elif len(grid) == 9:
        return "F"
    elif len(grid) == 10:
        return "7"
    else:
        assert len(grid) == 140
        return "|"

def day10_loop(grid):
    R = len(grid)
    C = len(grid[0])
    start = (0, 0)
    for r in range(R):
        for c in range(C):
            if grid[r][c] == "S":
                grid[r][c] = day10_guess(grid)
                start = (r, c)
    seen = set()
    q: list[tuple[int, int]] = [start]
    while q:
        next_ = q.pop()
        if next_ in seen:
            if not q:
                # we have no more places to flood
                return seen
            continue
        seen.add(next_)
        r, c = next_
        (dr1, dc1), (dr2, dc2) = day10_delta(grid[r][c])
        rr1, cc1 = r + dr1, c + dc1
        rr2, cc2 = r + dr2, c + dc2
        # flood in both directions
        q.append((rr1, cc1))
        q.append((rr2, cc2))
    assert False

def day10_1(data: List[str]):
    grid = day10_parse(data)
    loop = day10_loop(grid)
    return len(loop) // 2

def day10_inside(r, c, loop, grid):
    inside = False
    last = None
    # Run upwards outside the map starting this position,
    # and track each time we cross a loop section
    while r >= 0:
        # crossing a - will always change the inside
        p = ["-"]
        if last == "L":
            # we're running over a pipe that came from the right
            # so if it goes to the left we need to change the inside
            p.append("7")
        elif last == "J":
            # we're running over a pipe that came from the left
            # so if it goes to the right we need to change the inside
            p.append("F")

        # Check if we cross something
        if (r, c) in loop and grid[r][c] in p:
            # reset 'history'
            last = None
            inside = not inside

        if grid[r][c] in ["L", "J"]:
            # we're about to start running over a pipe, so keep this information to be checked later
            last = grid[r][c]
        r -= 1
    return inside

def day10_2(data: List[str]):
    grid = day10_parse(data)

    loop = day10_loop(grid)
    R = len(grid)
    C = len(grid[0])
    ans = 0
    for r in range(R):
        for c in range(C):
            if not (r, c) in loop and day10_inside(r, c, loop, grid):
                ans += 1
    return ans


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
