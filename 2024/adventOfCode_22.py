# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
from collections import Counter, defaultdict, deque
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402


YEAR = 2024
DAY = 22
EXPECTED_1 = 37990510
EXPECTED_2 = 23

def day22_parse(data: list[str]):
    return [int(l) for l in data]

def day22_next(n):
    res = n * 64
    n = n ^ res % 16777216

    res = n // 32
    n = n ^ res % 16777216

    res = n * 2048
    n = n ^ res % 16777216

    return n

def day22_solve(data, part2):
    data = day22_parse(data)
    nums = data
    p1 = 0
    p2 = Counter()
    for n in nums:
        prev_price = n % 10
        seen = set()
        # changes = []
        last_4, last_3, last_2, last_1 = 0, 0, 0, 0
        for t in range(2000):
            n = day22_next(n)
            price = n % 10
            last_4 = last_3
            last_3 = last_2
            last_2 = last_1
            last_1 = price - prev_price
            prev_price = price
            if t >= 3:
                sequence = (last_4, last_3, last_2, last_1)
                if sequence not in seen:
                    seen.add(sequence)
                    p2[sequence] += price
        p1 += n
    if not part2:
        return p1

    return p2.most_common()[0][1]

def day22_1(data):
    return day22_solve(data, False)

def day22_2(data):
    return day22_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
