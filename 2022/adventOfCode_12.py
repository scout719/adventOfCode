# -*- coding: utf-8 -*-
# pylint: disable=import-error
# pylint: disable=unused-import
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# pylint: disable=wrong-import-position
# pylint: disable=consider-using-enumerate
import os
import sys
from collections import defaultdict
from heapq import heappop, heappush

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main, day_with_validation  # NOQA: E402
# pylint: enable=import-error
# pylint: enable=wrong-import-position

YEAR = 2022
DAY = 12
EXPECTED_1 = 31
EXPECTED_2 = 29

""" DAY 12 """

def day12_parse(data):
    grid = []
    for line in data:
        grid.append(list(line))
    return grid

def day12_compute(data):
    grid = day12_parse(data)
    R = len(grid)
    C = len(grid[0])
    D = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    end = (0, 0)
    start = (0, 0)
    lowest_starts = set()
    for r in range(R):
        for c in range(C):
            if grid[r][c] == "S":
                start = (r, c)
            elif grid[r][c] == "E":
                end = (r, c)
            elif grid[r][c] == "a":
                lowest_starts.add((r, c))
    grid[end[0]][end[1]] = chr(ord('z') + 1)
    grid[start[0]][start[1]] = chr(ord('a') - 1)

    queue = [(0, end)]
    visited_steps = defaultdict(int)
    while queue:
        curr_steps, curr_pos = heappop(queue)
        r, c = curr_pos
        if curr_pos in visited_steps and 0 < visited_steps[curr_pos] <= curr_steps:
            continue
        visited_steps[curr_pos] = curr_steps
        curr = grid[r][c]
        for dr, dc in D:
            rr = r + dr
            cc = c + dc
            if 0 <= rr < R and 0 <= cc < C:
                # -1 -> climbing a height of 1
                #  0 -> stay on same level
                # >1 -> dropping down any height
                if ord(grid[rr][cc]) - ord(curr) >= -1:
                    heappush(queue, (curr_steps + 1, (rr, cc)))
    return visited_steps, start, lowest_starts

def day12_1(data):
    vistited_steps, start, _ = day12_compute(data)
    return vistited_steps[start]

def day12_2(data):
    vistited_steps, _, lowerst_starts = day12_compute(data)

    return min(vistited_steps[(r, c)] for r, c in lowerst_starts if (r, c) in vistited_steps)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
