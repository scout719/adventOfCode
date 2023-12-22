# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
from collections import defaultdict, deque
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
EXPECTED_2 = None

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
        return set([(r, c)])

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

def day21_reachable(R, C, rocks, r, c, max_l):
    q2: deque[tuple[tuple[int, int], int]] = deque([((r, c), 0)])
    seen = set()
    reacheable_odd = set()
    reacheable_even = set()
    while q2:
        (r, c), l = q2.popleft()
        k = (r, c)
        if k in seen:
            continue
        seen.add(k)
        if l % 2 == 1:
            reacheable_odd.add((k,l))
        else:
            reacheable_even.add((k,l))
        D = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        for dr, dc in D:
            rr, cc = (r + dr), (c + dc)
            if (rr, cc) not in rocks and 0 <= rr < R and 0 <= cc < C:
                q2.append(((rr, cc), l + 1))
    return reacheable_odd, reacheable_even

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
    st = 26501365

    d = defaultdict(lambda: defaultdict(list))

    assert all(r != start[0] for r, c in rocks)
    assert all(c != start[1] for r, c in rocks)
    assert start == (R // 2, C // 2)
    assert R == C
    assert R % 2 == 1
    # R = 131
    print(start)

    center_odd, _ = day21_reachable(R, C, rocks, start[0], start[1], R+C)
    top_left_odd, _ = day21_reachable(R, C, rocks, 0, 0,R+C)
    top_right_odd, _ = day21_reachable(R, C, rocks, 0, C - 1,R+C)
    bottom_left_odd, _ = day21_reachable(R, C, rocks, R - 1, 0,R+C)
    bottom_right_odd, _ = day21_reachable(R, C, rocks, R - 1, C - 1,R+C)

    _, mid_top_even = day21_reachable(R, C, rocks, 0, C // 2,R+C)
    _, mid_bottom_even = day21_reachable(R, C, rocks, R - 1, C // 2,R+C)
    _, mid_left_even = day21_reachable(R, C, rocks, R // 2, 0,R+C)
    _, mid_right_even = day21_reachable(R, C, rocks, R // 2, C - 1,R+C)



    # reacheable_odd -> center
    # left_side
    max_len = st // R
    full_lines = max_len - 1  # remove center
    x = (max_len + 1) * (max_len) // 2
    full_diags = x - full_lines - 1

    half_empty = full_lines + 1 # R//2 moves left corner
    half_full = half_empty-1 # R moves left corner
    extremes = 4 
    extremes_half_full = 4 # R moves left sides
    # print(full_diags, full_lines)
    # print(top_left_odd, top_right_odd, bottom_left_odd, bottom_right_odd, mid_top_even, mid_bottom_even, mid_left_even, mid_right_even)
    return len(center_odd) + \
        full_lines * len(mid_bottom_even) + \
        full_lines * len(mid_top_even) + \
        full_lines * len(mid_left_even) + \
        full_lines * len(mid_right_even) + \
        full_diags * len(top_left_odd) + \
        full_diags * len(top_right_odd) + \
        full_diags * len(bottom_left_odd) + \
        full_diags * len(bottom_right_odd) + \
        half_empty * len([1 for (_,_), l in top_left_odd if l <= R//2]) + \
        half_empty * len([1 for (_,_), l in top_right_odd if l <= R//2]) + \
        half_empty * len([1 for (_,_), l in bottom_left_odd if l <= R//2]) + \
        half_empty * len([1 for (_,_), l in bottom_right_odd if l <= R//2]) + \
        half_full * len([1 for (_,_), l in top_left_odd if l <= R//2 + R]) + \
        half_full * len([1 for (_,_), l in top_right_odd if l <= R//2+ R]) + \
        half_full * len([1 for (_,_), l in bottom_left_odd if l <= R//2+ R]) + \
        half_full * len([1 for (_,_), l in bottom_right_odd if l <= R//2+ R]) + \
        extremes + \
        extremes_half_full * len([1 for (_,_), l in  if l <= R]) + \

    # for rrr in [start[0]]:#range(R):
    #     for ccc in [start[1]]:#range(C):
    #         if (rrr, ccc) in rocks:
    #             continue
    #         # if rrr != 0 and ccc != 0 and rrr != R - 1 and ccc != C - 1:
    #         #     continue
    #         start = (rrr, ccc)
    #         q: deque[tuple[tuple[int, int], int]] = deque([(start, 0)])
    #         seen = set()
    #         while q:
    #             (r, c), l = q.popleft()
    #             if (r, c) in seen:
    #                 continue
    #             seen.add((r, c))
    #             d[start][(r, c)].append(l)

    #             D = [(0, 1), (1, 0), (-1, 0), (0, -1)]
    #             for dr, dc in D:
    #                 rr, cc = (r + dr), (c + dc)

    #                 if 0 <= rr < R and 0 <= cc < C and (rr, cc) not in rocks:
    #                     q.append(((rr, cc), l + 1))
    # return len(d)

    # R//2
    # return len(day20_dp(start[0], start[1], st, R, C, rocks, {}))
""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
