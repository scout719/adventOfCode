# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
from collections import deque
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
EXPECTED_2 = None

""" DAY 21 """

def day21_parse(data: list[str]):
    return data

def day21_info(grid):
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
    return start, rocks

def day21_solve(x, _):
    grid = x
    R = len(grid)
    C = len(grid[0])
    start, rocks = day21_info(grid)

    steps = 6 if R == 11 else 64
    q = set([start])
    D = [(0, 1), (1, 0), (-1, 0), (0, -1)]
    for _ in range(steps):
        n_q = set()
        for r, c in q:
            for dr, dc in D:
                rr, cc = r + dr, c + dc
                if 0 <= rr < R and 0 <= cc < C and (rr, cc) not in rocks:
                    n_q.add((rr, cc))
        q = n_q
    return len(q)

def day21_1(data):
    x = day21_parse(data)
    return day21_solve(x, False)

def day21_reachable(R, C, rocks, r, c, max_l):
    q: deque[tuple[tuple[int, int], int]] = deque([((r, c), 0)])
    seen = set()
    reacheable_odd = set()
    reacheable_even = set()
    while q:
        (r, c), steps = q.popleft()
        k = (r, c)
        if k in seen:
            continue
        seen.add(k)
        if steps % 2 == 1:
            reacheable_odd.add((k, steps))
        else:
            reacheable_even.add((k, steps))
        D = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        for dr, dc in D:
            rr, cc = (r + dr), (c + dc)
            if (rr, cc) not in rocks and 0 <= rr < R and 0 <= cc < C:
                q.append(((rr, cc), steps + 1))
    return ([x for x, steps in reacheable_odd if steps <= max_l],
            [x for x, steps in reacheable_even if steps <= max_l])

def day21_quadrant(R, C, rocks, st, mid_r, mid_c, corner_r, corner_c):
    # https://docs.google.com/spreadsheets/d/1St7OyhUKuvzdPOLTK7qejzADFwP-LLFuJOm5MUsJBQ4/edit?usp=sharing
    # Total of a quadrant of the diamond

    mid_odd, mid_even = day21_reachable(R, C, rocks, mid_r, mid_c, R + C)
    corner_odd, corner_even = day21_reachable(
        R, C, rocks, corner_r, corner_c, R + C)

    full_line = (st // R) - 1
    full_line_even = full_line // 2
    full_line_odd = full_line - full_line_even
    assert full_line_even <= full_line_odd
    extreme_half_full_is_odd = full_line_even == full_line_odd
    extreme_odd, extreme_even = day21_reachable(
        R, C, rocks, mid_r, mid_c, R - 1)
    extreme_half_full = len(
        extreme_odd) if extreme_half_full_is_odd else len(extreme_even)

    total_full = (full_line * (full_line + 1)) // 2
    full_diags = total_full - full_line
    y = max(0, (full_line - 2) if (full_line - 1) %
            2 == 0 else (full_line - 1))
    y = (y // 2) + 1
    full_diag_odd = y * y
    full_diag_even = full_diags - full_diag_odd

    half_full_partial = full_line
    half_empty_partial = full_line + 1

    half_empty_partial_is_odd = extreme_half_full_is_odd
    half_full_partial_is_odd = not extreme_half_full_is_odd
    half_empty_odd, half_empty_even = day21_reachable(
        R, C, rocks, corner_r, corner_c, (R // 2) - 1)
    half_full_odd, half_full_even = day21_reachable(
        R, C, rocks, corner_r, corner_c, (R - 1) + (R // 2))
    half_full = half_full_odd if half_full_partial_is_odd else half_full_even
    half_empty = half_empty_odd if half_empty_partial_is_odd else half_empty_even

    return full_line_odd * len(mid_odd) + \
        full_line_even * len(mid_even) + \
        extreme_half_full + \
        full_diag_even * len(corner_even) + \
        full_diag_odd * len(corner_odd) + \
        half_full_partial * len(half_full) + \
        half_empty_partial * len(half_empty)

def day21_2(data: list[str]):
    x = day21_parse(data)

    grid = x
    R = len(grid)
    C = len(grid[0])
    st = 26501365
    _, rocks = day21_info(grid)
    assert R == C
    # solution is hardcoded for:
    # odd size
    assert R % 2 == 1
    # odd steps
    assert st % 2 == 1
    # even quocient of steps over R
    assert (st // R) % 2 == 0
    # odd remainder of steps over R
    assert (st % R) % 2 == 1
    # remainder of steps just shy of half size
    assert (st % R) == R // 2
    # limits are all free
    # top
    assert all(grid[0][c] == "." for c in range(C))
    # right
    assert all(grid[r][C - 1] == "." for r in range(R))
    # bottom
    assert all(grid[R - 1][c] == "." for c in range(C))
    # left
    assert all(grid[r][0] == "." for r in range(R))
    # Lines crossing the middle also free
    # vertical
    assert all(grid[r][C // 2] in [".", "S"] for r in range(R))
    # horizontal
    assert all(grid[R // 2][c] in [".", "S"] for c in range(C))

    # R, st, rocks = 7, 31, set()

    # Diamond can be divided into 4 quadrants + the center piece
    # since we can go straight to the edges and navigate to each
    # corner of a 'sub-square'
    #       2
    #      122
    #     11222
    #    111C333
    #     44433
    #      443
    #       4
    #
    # Number of odd positions reached on center square
    center_odd, _ = day21_reachable(R, R, rocks, R // 2, R // 2, R + R)
    center = len(center_odd)

    # Number of positions of top left quadrant
    right_down_right = day21_quadrant(
        R, R, rocks, st, R // 2, R - 1, R - 1, R - 1)

    # Number of positions of top right quadrant
    down_down_left = day21_quadrant(R, R, rocks, st, R - 1, R // 2, R - 1, 0)

    # Number of positions of bottom right quadrant
    left_up_left = day21_quadrant(R, R, rocks, st, R // 2, 0, 0, 0)

    # Number of positions of bottom left quadrant
    up_up_right = day21_quadrant(R, R, rocks, st, 0, R // 2, 0, R - 1)

    # too low:
    #           614455686112700
    #           614455686112704
    #           614455686113074
    #           614455686113224

    # too high:
    #           631398149479603
    return center + right_down_right + down_down_left + left_up_left + up_up_right


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
