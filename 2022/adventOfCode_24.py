# -*- coding: utf-8 -*-
import os
import sys
from collections import defaultdict, deque

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable-next=wrong-import-position
from common.utils import (WHITE_SQUARE,  # NOQA: E402
                          day_with_validation, main)

YEAR = 2022
DAY = 24
EXPECTED_1 = 18
EXPECTED_2 = 54

""" DAY 24 """

def day24_parse(data):
    blizzards = defaultdict(list)
    start_c = 0
    end_c = 0
    R = len(data)
    C = len(data[0])
    for r, line in enumerate(data):
        for c, char in enumerate(line):
            if r == 0:
                if char == ".":
                    start_c = c
            if r == len(data) - 1:
                if char == ".":
                    end_c = c
            if char == "<":
                blizzards[(r, c)].append((0, -1))
            if char == "v":
                blizzards[(r, c)].append((1, 0))
            if char == ">":
                blizzards[(r, c)].append((0, 1))
            if char == "^":
                blizzards[(r, c)].append((-1, 0))
    return blizzards, (start_c, end_c), (R, C)

def day24_print(r, c, blizzards, R, C):
    for rr in range(R):
        line = ""
        for cc in range(C):
            if len(blizzards[(rr, cc)]) == 0:
                if (rr, cc) == (r, c):
                    line += WHITE_SQUARE
                else:
                    if cc == 0 or cc == C - 1 or \
                       rr == 0 or rr == R - 1:
                        line += "#"
                    else:
                        line += " "
            elif len(blizzards[(rr, cc)]) > 1:
                line += str(len(blizzards[(rr, cc)]))
            else:
                dr, dc = blizzards[(rr, cc)][0]
                line += "<" if (dr, dc) == (0, -1) else \
                    ">" if (dr, dc) == (0, 1) else \
                    "v" if (dr, dc) == (1, 0) else "^"
        print(line)
    print()

def day24_get_blizzards(blizzards_mem, t, R, C):
    if t in blizzards_mem:
        return blizzards_mem[t]
    else:
        new_blizzards = defaultdict(list)
        for (r, c), blizzards_deltas in blizzards_mem[t - 1].items():
            for dr, dc in blizzards_deltas:
                rr, cc = r + dr, c + dc
                if rr == R - 1:
                    assert dr == 1
                    rr = 1
                elif rr == 0:
                    assert dr == -1
                    rr = R - 2
                elif cc == C - 1:
                    assert dc == 1
                    cc = 1
                elif cc == 0:
                    assert dc == -1
                    cc = C - 2

                new_blizzards[(rr, cc)].append((dr, dc))
        blizzards_mem[t] = new_blizzards
        return new_blizzards

def day24_solve(t, start_r, start_c, target_r, target_c, blizzards_mem, R, C):
    q = [(t, (start_r, start_c))]
    q = deque(q)
    D = [(1, 0), (0, 1), (0, -1), (-1, 0), (0, 0)]
    seen = set()
    while q:
        t, (r, c) = q.popleft()
        if (r, c) == (target_r, target_c):
            return t

        key = (r, c, t)
        if key in seen:
            continue
        seen.add(key)

        for dr, dc in D:
            rr, cc = r + dr, c + dc
            next_blizzards = day24_get_blizzards(blizzards_mem, t + 1, R, C)
            if len(next_blizzards[(rr, cc)]) > 0:
                continue
            if not (0 <= rr < R and 0 <= cc < C):
                continue
            if not ((rr == target_r and cc == target_c) or
                    (rr == start_r and cc == start_c)):
                if rr == 0:
                    continue
                if rr == R - 1:
                    continue
            if cc == 0:
                continue
            if cc == C - 1:
                continue
            q.append((t + 1, (rr, cc)))

def day24_1(data):
    blizzards, (start_c, end_c), (R, C) = day24_parse(data)

    blizzards_mem = {}
    blizzards_mem[0] = blizzards
    return day24_solve(0, 0, start_c, R - 1, end_c, blizzards_mem, R, C)

def day24_2(data):
    blizzards, (start_c, end_c), (R, C) = day24_parse(data)

    blizzards_mem = {}
    blizzards_mem[0] = blizzards
    t = day24_solve(0, 0, start_c, R - 1, end_c, blizzards_mem, R, C)
    t = day24_solve(t, R - 1, end_c, 0, start_c, blizzards_mem, R, C)
    t = day24_solve(t, 0, start_c, R - 1, end_c, blizzards_mem, R, C)
    return t


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
