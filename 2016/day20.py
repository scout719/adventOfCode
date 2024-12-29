# -*- coding: utf-8 -*-
import os
import re
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable=wrong-import-position
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2016
DAY = 20
EXPECTED_1 = 3
EXPECTED_2 = 2

def day20_parse(data: list[str]):
    ranges = []
    for line in data:
        res = re.match(r"(\d+)-(\d+)", line)
        assert res is not None
        lo, hi = res.groups()
        ranges.append((int(lo), int(hi) + 1))
    return ranges

def day20_solve(data, part2):
    data = day20_parse(data)
    ranges = data
    max_ = 4294967295
    if len(ranges) < 10:
        max_ = 9
    curr = [(0, max_ + 1)]

    # ranges [lo,hi[
    for lo, hi in ranges:  # forbidden
        new_curr = []
        for lo2, hi2 in curr:
            if hi < lo2 or lo >= hi2:
                new_curr.append((lo2, hi2))
                continue
            if lo2 <= lo and hi < hi2:
                new_curr.append((lo2, lo))
                new_curr.append((hi, hi2))
            elif lo <= lo2 and hi <= hi2:
                new_curr.append((hi, hi2))
            elif lo2 <= lo and hi2 <= hi:
                new_curr.append((lo2, lo))
        curr = new_curr

    curr = [(lo, hi) for (lo, hi) in curr if lo != hi]
    if not part2:
        return curr[0][0]

    return sum(hi - lo for lo, hi in curr)

def day20_1(data):
    return day20_solve(data, False)

def day20_2(data):
    return day20_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
