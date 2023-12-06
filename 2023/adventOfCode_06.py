# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
import os
import sys
from collections import defaultdict
from typing import List, Tuple, Set, Dict

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import day_with_validation  # NOQA: E402
from common.utils import main  # NOQA: E402

Card = Tuple[int, Set[int], Set[int]]

YEAR = 2023
DAY = 6
EXPECTED_1 = 288
EXPECTED_2 = 71503


""" DAY 6 """

def day6_parse(data: List[str]):
    times = [int(x) for x in data[0].split(":")[1].split()]
    dists = [int(x) for x in data[1].split(":")[1].split()]

    return times, dists

def day6_solve(times: List[int], dists: List[int]):
    L = len(times)
    ans = 1
    for i in range(L):
        curr_t = times[i]
        wins = 0
        for t in range(curr_t):
            speed = t
            time = curr_t - t
            dist = speed * time
            if dist > dists[i]:
                wins += 1
        if wins > 0:
            ans *= wins
    return ans

def day6_1(data: List[str]):
    times, dists = day6_parse(data)
    return day6_solve(times, dists)

def day6_2(data: List[str]):
    times, dists = day6_parse(data)
    T = ""
    for t in times:
        T += str(t)
    D = ""
    for d in dists:
        D += str(d)
    times = [int(T)]
    dists = [int(D)]
    return day6_solve(times, dists)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
