# -*- coding: utf-8 -*-
import os
import sys

from collections import defaultdict

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable-next=wrong-import-position
from common.utils import main, day_with_validation  # NOQA: E402

YEAR = 2022
DAY = 23
EXPECTED_1 = 110
EXPECTED_2 = 20

""" DAY 23 """

def day23_parse(data):
    occupied = set()
    for r, line in enumerate(data):
        for c, char in enumerate(line):
            if char == "#":
                occupied.add((r, c))
    return occupied

def day23_print(occupied):
    min_r = min(r for r, c in occupied)
    max_r = max(r for r, c in occupied)
    min_c = min(c for r, c in occupied)
    max_c = max(c for r, c in occupied)
    for r in range(min_r, max_r + 1):
        line = ""
        for c in range(min_c, max_c + 1):
            if (r, c) in occupied:
                line += "#"
            else:
                line += "."
        print(line)
    print()

def day23_solve(data, max_t):
    occupied = day23_parse(data)
    R = max(r for r, c in occupied)
    C = max(c for r, c in occupied)
    D_around = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    D_proposal = [
        ([(-1, 0), (-1, -1), (-1, 1)], (-1, 0)),
        ([(1, 0), (1, -1), (1, 1)], (1, 0)),
        ([(-1, -1), (1, -1), (0, -1)], (0, -1)),
        ([(-1, 1), (0, 1), (1, 1)], (0, 1))
    ]
    for t in range(max_t):
        proposals = {}
        counter = defaultdict(int)
        for r, c in occupied:
            alone = True
            for dr, dc in D_around:
                rr, cc = r + dr, c + dc
                if (rr, cc) in occupied:
                    alone = False
                    break
            if alone:
                continue

            for D, (dr_, dc_) in D_proposal:
                alone = True
                for dr, dc in D:
                    rr, cc = r + dr, c + dc
                    if (rr, cc) in occupied:
                        alone = False
                        break
                if alone:
                    proposals[(r, c)] = (r + dr_, c + dc_)
                    counter[(r + dr_, c + dc_)] += 1
                    break
        D_proposal = D_proposal[1:] + [D_proposal[0]]
        new_occupied = set(list(occupied))
        moved = False
        for (r, c), (rr,cc) in proposals.items():
            if counter[(rr, cc)] == 1:
                new_occupied.add((rr, cc))
                new_occupied.remove((r, c))
                moved = True
        if not moved:
            return t + 1
        occupied = new_occupied

    min_r = min(r for r, c in occupied)
    max_r = max(r for r, c in occupied)
    min_c = min(c for r, c in occupied)
    max_c = max(c for r, c in occupied)
    return (max_r - min_r + 1) * (max_c - min_c + 1) - len(occupied)

def day23_1(data):
    return day23_solve(data, 10)

def day23_2(data):
    return day23_solve(data, int(1e9))


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
