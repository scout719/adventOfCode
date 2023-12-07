# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
import os
import sys
from typing import List

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import day_with_validation  # NOQA: E402
from common.utils import main  # NOQA: E402

YEAR = 2023
DAY = 5
EXPECTED_1 = 35
EXPECTED_2 = 46


""" DAY 5 """

def day5_parse(data: List[str]):
    seeds = [int(s) for s in data[0].split(": ")[1].split()]
    curr = []
    maps = []
    for line in data[2:]:
        if not line:
            maps.append(sorted(curr))
            curr = []
            continue

        if line.endswith("map:"):
            continue

        dest_start, src_start, range_ = line.split()
        curr.append((int(src_start), int(dest_start), int(range_)))

    maps.append(sorted(curr))
    return seeds, maps

def day5_1(data: List[str]):
    seeds, maps = day5_parse(data)
    low = None
    for seed in seeds:
        curr = seed
        for map_ in maps:
            for (src_start, dest_start, range_len) in map_:
                if src_start <= curr < src_start + range_len:
                    curr = dest_start + (curr - src_start)
                    break
        if (low is None) or (curr < low):
            low = curr
    # low 51515303
    return low

def day5_2(data: List[str]):
    seeds, maps = day5_parse(data)
    ranges = []
    for i in range(0, len(seeds), 2):
        start = seeds[i]
        range_ = seeds[i + 1]
        ranges.append((start, range_))

    for map_ in maps:
        new_ranges = []
        for lowerbound, range_len in ranges:
            left = lowerbound
            right = lowerbound + range_len - 1
            src_start, dest_start, range_ = map_[0]
            if left < src_start:
                # account for left side of ranges
                size = min(range_, right - left + 1)
                new_ranges.append((left, size))
                left = src_start

            while left <= right:
                found = False
                for (src_start, dest_start, range_) in map_:
                    if src_start <= left < src_start + range_:
                        upper_bound = min(right, src_start + range_ - 1)
                        size = min(range_, upper_bound - left + 1)
                        new_ranges.append(
                            (dest_start + (left - src_start), size))
                        left += size
                        found = True
                        break
                if not found:
                    # account for right side of ranges
                    size = right - left + 1
                    new_ranges.append((left, size))
                    left += size
        ranges = new_ranges
    return sorted(ranges)[0][0]


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
