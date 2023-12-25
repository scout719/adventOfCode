# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import day_with_validation  # NOQA: E402
from common.utils import main  # NOQA: E402

YEAR = 2023
DAY = 16
EXPECTED_1 = 46
EXPECTED_2 = 51

""" DAY 16 """

def day16_parse(data: list[str]):
    return [line for line in data]

def day16_solve(grid, s_r, s_c, s_dr, s_dc):
    R = len(grid)
    C = len(grid[0])
    q: list[tuple[int, int, int, int]] = [(s_r, s_c, s_dr, s_dc)]
    seen = set()
    while q:
        r, c, dr, dc = q[0]
        del q[0]
        if not (0 <= r < R) or not (0 <= c < C):
            continue
        k = (r, c, dr, dc)
        if k in seen:
            continue
        seen.add(k)
        p = grid[r][c]
        assert abs(dr) + abs(dc) == 1, f"r={r} c={c} dr={dr} dc={dc}"
        if p == "." or \
            (p == "-" and dr == 0) or \
                (p == "|" and dc == 0):
            q.append((r + dr, c + dc, dr, dc))
        elif p == "\\":
            if dr == 1:
                dr, dc = 0, 1
            elif dr == -1:
                dr, dc = 0, -1
            elif dc == 1:
                dr, dc = 1, 0
            else:
                assert dc == -1
                dr, dc = -1, 0
            q.append((r + dr, c + dc, dr, dc))
        elif p == "/":
            if dr == 1:
                dr, dc = 0, -1
            elif dr == -1:
                dr, dc = 0, 1
            elif dc == 1:
                dr, dc = -1, 0
            else:
                assert dc == -1
                dr, dc = 1, 0
            q.append((r + dr, c + dc, dr, dc))
        elif p == "|":
            assert abs(dc) == 1
            q.append((r + 1, c, 1, 0))
            q.append((r - 1, c, -1, 0))
        else:
            assert abs(dr) == 1 and p == "-"
            q.append((r, c + 1, 0, 1))
            q.append((r, c - 1, 0, -1))
    return len({(r, c) for r, c, _, _ in seen})

def day16_1(data):
    grid = day16_parse(data)
    return day16_solve(grid, 0, 0, 0, 1)

def day16_2(data: list[str]):
    grid = day16_parse(data)
    R = len(grid)
    C = len(grid[0])
    ans = 0
    for r in range(R):
        for c in range(C):
            if r == 0 or c == 0 or r == R - 1 or c == C - 1:
                dr = 1 if r == 0 else \
                    -1 if r == R - 1 else \
                    0
                dc = 1 if c == 0 else \
                    -1 if c == C - 1 else \
                    0
                D = [(dr, dc)]
                if abs(dr) + abs(dc) == 2:
                    # corner
                    D = [(dr, 0), (0, dc)]

                for ddr, ddc in D:
                    assert abs(ddr) + abs(ddc) == 1, \
                        f"r={r} c={c} dr={dr} dc={dc}"
                    energy = day16_solve(grid, r, c, ddr, ddc)
                    if energy > ans:
                        ans = energy
    return ans


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
