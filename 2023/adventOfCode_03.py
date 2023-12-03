# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
import os
import sys
from collections import defaultdict
from typing import List

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import day_with_validation  # NOQA: E402
from common.utils import main  # NOQA: E402

YEAR = 2023
DAY = 3
EXPECTED_1 = 4361
EXPECTED_2 = 467835


""" DAY 3 """

def day3_parse(data: List[str]):
    valid_parts = []
    gears_map = defaultdict(list)
    for r, line in enumerate(data):
        c = 0
        while c < len(line):
            while c < len(line) and not line[c].isdigit():
                c += 1
            if c == len(line):
                break
            part = ""
            start = c
            while c < len(line) and line[c].isdigit():
                part += line[c]
                c += 1
            size = len(part)
            part = int(part)
            DR = [-1, 0, 1]
            DC = list(range(- 1, size + 1))
            added = False
            for dc in DC:
                cc = start + dc
                for dr in DR:
                    rr = r + dr
                    if 0 <= rr < len(data) and \
                       0 <= cc < len(line) and \
                       not (data[rr][cc].isdigit() or data[rr][cc] == ".") and \
                       not added:
                        added = True
                        valid_parts.append(part)
                        if data[rr][cc] == "*":
                            gears_map[(rr, cc)].append(part)
    return valid_parts, gears_map

def day3_1(data: List[str]):
    valid_parts, _ = day3_parse(data)
    return sum(valid_parts)

def day3_2(data: List[str]):
    _, gears_map = day3_parse(data)
    ans = 0
    for k in gears_map:
        if len(gears_map[k]) == 2:
            ans += gears_map[k][0] * gears_map[k][1]

    return ans


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
