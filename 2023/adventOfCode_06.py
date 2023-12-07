# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
import os
import sys
import math
from typing import List

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import day_with_validation  # NOQA: E402
from common.utils import main  # NOQA: E402

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
        # y = (curr_t-x)*x = curr_t*x - x^2
        # a = -1 b = curr_t c = 0
        # y = -b +- sqrt(b^2 - 4ac ) /a*c
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

def day6_quadratic_roots(a: float, b: float, c: float):
    # y = 0 -> x = -b +- sqrt(b^2 - 4ac) / 2a
    ac = a * c
    b_sqr = b * b
    sqrt = math.sqrt(b_sqr - 4 * ac)
    # Keep only integer part
    return math.floor((-b + sqrt) / (2 * a)), math.floor((-b - sqrt) / (2 * a))

def day6_2(data: List[str]):
    times, dists = day6_parse(data)
    T = ""
    for t in times:
        T += str(t)
    D = ""
    for d in dists:
        D += str(d)

    # original
    # times = [int(T)]
    # dists = [int(D)]
    # return day6_solve(times, dists)

    # y -> extra distance covered beyond record
    # when pressing for x milliseconds
    # y = (curr_t-x)*x - (dist+1) = curr_t*x - x^2 - (dist+1)
    # a = -1 b = curr_t c = -(dist+1)
    a = -1
    b = int(T)
    c = -(int(D) + 1)

    left, right = day6_quadratic_roots(a, b, c)
    return right - left


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
