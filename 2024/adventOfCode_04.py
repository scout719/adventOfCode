# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
from collections import defaultdict
from email.policy import default
import enum
import os
import sys
from typing import Counter, List

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2024
DAY = 4
EXPECTED_1 = 18
EXPECTED_2 = 9


""" DAY 4 """

def day4_parse(data: list[str]):
    return data

def day4_solve(data, part2):
    data = day4_parse(data)
    R, C = len(data), len(data[0])
    WORDS = [
        ["XMAS",
         "....",
         "....",
         "...."],
        ["SAMX",
         "....",
         "....",
         "...."],
        ["X...",
         "M...",
         "A...",
         "S..."],
        ["S...",
         "A...",
         "M...",
         "X..."],
        ["X...",
         ".M..",
         "..A.",
         "...S"],
        ["...X",
         "..M.",
         ".A..",
         "S..."],
        ["S...",
         ".A..",
         "..M.",
         "...X"],
        ["...S",
         "..A.",
         ".M..",
         "X..."],
    ]
    if part2:
        WORDS = [
            ["M.M",
             ".A.",
             "S.S"],
            ["M.S",
             ".A.",
             "M.S"],
            ["S.M",
             ".A.",
             "S.M"],
            ["S.S",
             ".A.",
             "M.M"]
        ]
    ans = 0
    for r in range(R):
        for c in range(C):
            for word in WORDS:
                found = True
                for dr, w_r in enumerate(word):
                    for dc, ch in enumerate(w_r):
                        rr, cc = r + dr, c + dc
                        if ch != ".":
                            if not (0 <= rr < R and 0 <= cc < C):
                                found = False
                                break
                            if data[rr][cc] != ch:
                                found = False
                                break
                    if not found:
                        break
                if found:
                    ans += 1
    return ans

def day4_original(data, _):
    # original part 1 solution
    data = day4_parse(data)
    R, C = len(data), len(data[0])
    DR = [-1, 0, 1]
    DC = [-1, 0, 1]
    WORD = "XMAS"
    ans = 0
    for r in range(R):
        for c in range(C):
            for dr in DR:
                for dc in DC:
                    if dr == dc == 0:
                        continue
                    found = True
                    for i, ch in enumerate(WORD):
                        rr, cc = r + dr * i, c + dc * i

                        if not (0 <= rr < R and 0 <= cc < C):
                            found = False
                            break

                        if not data[rr][cc] == ch:
                            found = False
                            break
                    if found:
                        ans += 1
    return ans

def day4_1(data):
    return day4_solve(data, False)

def day4_2(data):
    return day4_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
