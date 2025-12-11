# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
from collections import defaultdict
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2025
DAY = 11
EXPECTED_1 = 5
EXPECTED_2 = 2

def day11_parse(data: list[str]):
    E = defaultdict(set)
    for line in data:
        left, right = line.split(": ")
        E[left] = set(right.split(" "))
    return E

def day11_paths(E, DP, curr, fft, dac):
    if curr == "out":
        if (fft and dac):
            return 1
        else:
            return 0

    key = (curr, fft, dac)
    if key in DP:
        return DP[key]

    ans = 0
    for out in E[curr]:
        ans += day11_paths(E, DP, out,
                           fft or (curr == "fft"),
                           dac or (curr == "dac"))

    DP[key] = ans
    return ans

def day11_solve(data, part2):
    E = day11_parse(data)

    if part2:
        return day11_paths(E, {}, "svr", False, False)

    # Simulate that we've passed through the requirements already
    return day11_paths(E, {}, "you", True, True)

def day11_1(data):
    return day11_solve(data, False)

def day11_2(data):
    return day11_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
