# -*- coding: utf-8 -*-
from math import ceil, sqrt
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable=wrong-import-position
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2015
DAY = 20
EXPECTED_1 = 4
EXPECTED_2 = None


""" DAY 20 """

def day20_parse(data):
    return int(data[0])

def day20_divisors(n):
    large_divisors: list = []
    for i in range(1, int(sqrt(n) + 1)):
        if n % i == 0:
            yield i
            if i * i != n:
                large_divisors.append(n / i)
    for divisor in reversed(large_divisors):
        yield divisor

def day20_1(data):
    data = day20_parse(data)

    house = 1
    while house < data:
        ans = 0
        ans = sum(day20_divisors(house)) * 10
        if ans >= data:
            # low: 448351
            #      448387
            return house
        house += 1

    assert False

def day20_2(data):
    data = day20_parse(data)
    return data


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
