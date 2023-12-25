# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
import os
import sys
from typing import List, Tuple

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import day_with_validation  # NOQA: E402
from common.utils import main  # NOQA: E402

YEAR = 2023
DAY = 12
EXPECTED_1 = 21
EXPECTED_2 = 525152


""" DAY 12 """

def day12_parse(data: List[str]):
    rows = []
    for line in data:
        springs, sizes = line.split(" ")
        sizes = [int(x) for x in sizes.split(",")]
        rows.append([springs, sizes])
    return rows

def day12_valid(springs: str, sizes, strict: bool = False):
    groups = springs.split(".")
    lens = [len(g) for g in groups if g]
    if strict:
        return lens == sizes
    if len(lens) > len(sizes):
        return False
    # compare last sizes
    valid = True
    if len(lens) > 1:
        valid = lens[1:] == sizes[-(len(lens) - 1):]
    if len(lens) > 0:
        # first should be less or equal
        valid &= lens[0] <= sizes[-len(lens)]
    return valid

def day12_final(sizes, springs, mem):
    if not sizes:
        return 1 if all(c == "." or c == "?" for c in springs) else 0

    if not springs:
        return 0

    key = (tuple(sizes), springs)
    if key in mem:
        return mem[key]

    ans = 0
    curr = springs[0]
    if curr in [".", "?"]:
        # Just skip this
        ans += day12_final(sizes, springs[1:], mem)

    if curr in ["#", "?"]:
        # consume all broken in a row
        broken = sizes[0]
        if len(springs) >= broken:
            if all(spring in ["#", "?"] for spring in springs[:broken]):
                springs = springs[broken:]
                if springs:
                    if springs[0] in [".", "?"]:
                        ans += day12_final(sizes[1:], springs[1:], mem)
                    else:
                        # not a working spring consume
                        pass
                else:
                    # no working spring available to 'close'' the group
                    # If this was the last group, all is good
                    ans += 1 if len(sizes) == 1 else 0
            else:
                # no sequence of 'broken' springs to be consumed
                pass
        else:
            # not enough springs to consume
            pass
    mem[key] = ans
    return ans

def day12_solve(rows: List[Tuple[str, List[int]]]):
    ans = 0
    mem = {}
    for springs, sizes in rows:
        # append a . at the end to help the algorithm
        springs = springs
        ans += day12_final(sizes, springs, mem)
    return ans

def day12_1(data: List[str]):
    rows = day12_parse(data)
    return day12_solve(rows)

def day12_2(data: List[str]):
    rows = day12_parse(data)
    for i, row in enumerate(rows):
        rows[i][0] = (row[0] + "?") * 4 + row[0]
        rows[i][1] = row[1] * 5
    return day12_solve(rows)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
