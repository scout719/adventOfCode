# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
from collections import defaultdict
from copy import deepcopy
from math import lcm
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import day_with_validation  # NOQA: E402
from common.utils import main  # NOQA: E402

YEAR = 2023
DAY = 21
EXPECTED_1 = 16
EXPECTED_2 = -1

""" DAY 21 """

def day21_parse(data: list[str]):
    return data

def day21_solve(x, part2):
    grid = x
    R = len(grid)
    C = len(grid[0])
    rocks = set()
    start = (-1, -1)
    for r in range(R):
        for c in range(C):
            if grid[r][c] == "#":
                rocks.add((r, c))
            elif grid[r][c] == "S":
                start = (r, c)
            else:
                assert grid[r][c] == "."

    st = 6 if R == 11 else 64
    q = set([start])
    seen = set()
    D = [(0, 1), (1, 0), (-1, 0), (0, -1)]
    for t in range(st):
        # print(q)
        n_q = set()
        for r, c in q:
            # seen.add((r, c))
            for dr, dc in D:
                rr, cc = r + dr, c + dc
                if 0 <= rr < R and 0 <= cc < C and (rr, cc) not in seen and (rr, cc) not in rocks:
                    n_q.add((rr, cc))
        q = n_q
    # print(q)
    return len(q)

    return None

def day21_1(data):
    x = day21_parse(data)
    return day21_solve(x, False)


def day20_dp(r, c, st, R, C, rocks, mem):
    if st == 0:
        return set([(r,c)])

    else:
        k = (r, c, st)
        if k in mem:
            return mem[k]

        D = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        ans = set()
        for dr, dc in D:
            rr, cc = (r + dr) % R, (c + dc) % C

            if (rr, cc) not in rocks:
                ans = ans.union(day20_dp(rr, cc, st - 1, R, C, rocks, mem))

        # print(rr,cc,st, ans)
        mem[k] = ans
        return ans

def day21_2(data: list[str]):
    x = day21_parse(data)
    grid = x
    R = len(grid)
    C = len(grid[0])
    rocks = set()
    start = (-1, -1)
    for r in range(R):
        for c in range(C):
            if grid[r][c] == "#":
                rocks.add((r, c))
            elif grid[r][c] == "S":
                start = (r, c)
            else:
                assert grid[r][c] == "."
    st = 5000
    return len(day20_dp(start[0], start[1], st, R,C,rocks, {}))


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
