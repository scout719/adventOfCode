# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import RED_SMALL_SQUARE, main  # NOQA: E402
from common.utils import day_with_validation, WHITE_SQUARE, BLUE_CIRCLE  # NOQA: E402


YEAR = 2024
DAY = 19
EXPECTED_1 = 6
EXPECTED_2 = 16

def day19_parse(data: list[str]):
    patterns, designs = "\n".join(data).split("\n\n")
    patterns = patterns.split(", ")
    return patterns, designs.split("\n")

def day19_ways(DP, patterns, design: str):
    if design == "":
        return 1

    if design in DP:
        return DP[design]

    ways = 0
    for pattern in patterns:
        if design.startswith(pattern):
            ways += day19_ways(DP, patterns, design[len(pattern):])

    DP[design] = ways
    return ways

def day19_solve(data, part2):
    data = day19_parse(data)
    patterns, designs = data
    ans = 0
    for design in designs:
        ways = day19_ways({}, patterns, design)
        if part2:
            ans += ways
        elif ways > 0:
            ans += 1
    return ans

def day19_1(data):
    return day19_solve(data, False)

def day19_2(data):
    return day19_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
