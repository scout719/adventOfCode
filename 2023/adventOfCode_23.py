# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
from collections import defaultdict, deque
from copy import deepcopy
from heapq import heappop, heappush
from math import lcm
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import WHITE_SQUARE, day_with_validation  # NOQA: E402
from common.utils import main  # NOQA: E402

YEAR = 2023
DAY = 23
EXPECTED_1 = 94
EXPECTED_2 = 154

""" DAY 23 """

def day23_parse(data: list[str]):
    return data

def day23_show(grid):
    R = len(grid)
    C = len(grid[0])
    junc = set()

    for r in range(R):
        l = ""
        for c in range(C):
            ch = grid[r][c]
            l += WHITE_SQUARE if ch == "#" else " "
            if ch != "#" and r != 0 and r != R - 1:
                ct = 0
                D: list[tuple[int, int]] = [(0, 1), (1, 0), (0, -1), (-1, 0)]
                for _, (dr, dc) in enumerate(D):
                    rr, cc = r + dr, c + dc
                    if grid[rr][cc] != "#":
                        ct += 1
                if ct > 2:
                    junc.add((r, c))

        print(l)
    print((junc, len(junc)))

def day23_path(r, c, rr, cc, juncs, grid):
    q = [(r, c, 0)]
    D: list[tuple[int, int]] = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    R = len(grid)
    C = len(grid[0])
    paths = set()
    seen = set()
    while q:
        rrr, ccc, d = q.pop()
        if (rrr, ccc) in seen:
            continue
        seen.add((rrr, ccc))

        if (rrr, ccc) == (rr, cc):
            # originally was looking for the longest path
            return d

        if (rrr, ccc) in juncs and (rrr, ccc) != (r, c):
            continue

        for dr, dc in D:
            rrrr, cccc = rrr + dr, ccc + dc
            if 0 <= rrrr < R and 0 <= cccc < C and grid[rrrr][cccc] != "#":
                q.append((rrrr, cccc, d + 1))

    return max(paths) if paths else None

def day23_solve(x, part2):
    grid: list[list[str]] = x
    R = len(grid)
    C = len(grid[0])
    s_c = grid[0].index(".")
    e_c = grid[-1].index(".")

    D: list[tuple[int, int]] = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    paths = []
    q: list[tuple[int, int, int, list[tuple[int, int]]]] = [
        (0, s_c, 0, [])]
    while q:
        r, c, l, path = q.pop()
        if (r, c) == (R - 1, e_c):
            paths.append(len(path))
            continue
        for _, (dr, dc) in enumerate(D):
            rr, cc = r + dr, c + dc
            if (rr, cc) in path:
                continue
            if grid[rr][cc] == ".":
                q.append(
                        (rr, cc,
                         l + 1, path + [(rr, cc)]))
                continue
            ch = grid[rr][cc]
            if ch == ">" and dc == 1:
                q.append(
                    (rr, cc + 1, l + 2, path + [(rr, cc), (rr, cc + 1)]))
            elif ch == "<" and dc == -1:
                q.append(
                    (rr, cc - 1, l + 2, path + [(rr, cc), (rr, cc - 1)]))
            elif ch == "^" and dr == -1:
                q.append(
                    (rr - 1, cc, l + 2, path + [(rr, cc), (rr + 1, cc)]))
            elif ch == "v" and dr == 1:
                q.append(
                    (rr + 1, cc, l + 2, path + [(rr, cc), (rr - 1, cc)]))
            else:
                pass
    return max(paths)

def day23_1(data):
    x = day23_parse(data)
    return day23_solve(x, False)

def day23_2(data: list[str]):
    x = day23_parse(data)
    grid: list[str] = x
    R = len(grid)
    C = len(grid[0])
    s_c = grid[0].index(".")
    e_c = grid[-1].index(".")
    # day23_show(grid)
    juncs = set()

    for r in range(R):
        for c in range(C):
            ch = grid[r][c]
            if ch != "#" and r != 0 and r != R - 1:
                ct = 0
                D: list[tuple[int, int]] = [(0, 1), (1, 0), (0, -1), (-1, 0)]
                for i, (dr, dc) in enumerate(D):
                    rr, cc = r + dr, c + dc
                    if grid[rr][cc] != "#":
                        ct += 1
                if ct > 2:
                    juncs.add((r, c))
    E = defaultdict(set)
    Dist = {}
    l = juncs.union({(0, s_c), (R - 1, e_c)})
    for i, (r, c) in enumerate(l):
        for j, (rr, cc) in enumerate(l):
            if j <= i:
                continue
            d = day23_path(r, c, rr, cc, juncs, grid)
            if d:
                left = (r, c)
                right = (rr, cc)
                Dist[(left, right)] = d
                Dist[(right, left)] = d
                E[left].add(right)
                E[right].add(left)

    # DFS would not require a seen set for each elem since it explores a path at a time
    # so we could just use a single Bit array and, each time we finish going down
    # a path, unmark it
    q = [(0, 0, s_c, set())]
    paths = set()
    while q:
        l, r, c, path = q.pop()
        if (r, c) in path:
            continue
        path.add((r, c))

        if (r, c) == (R - 1, e_c):
            paths.add(l)
            continue
        for rr, cc in E[(r, c)]:
            if (rr, cc) in path:
                continue
            d = Dist[((r, c), (rr, cc))]
            q.append((l + d, rr, cc, set() | path))

    return max(paths)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
