# -*- coding: utf-8 -*-
from math import sqrt
import os
import sys
from typing import Counter

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

def day20_sum_divisors_part2(n):
    ans = 0
    # only go up to 50 because:
    # consider i > 50 and n=i*k
    # if i < k, so k is also > 50
    # it means that n // i = k which is > 50 so the elf will not give any presents anymore
    # if i > k
    # we must have already passed by it on a previous iteration
    # and already counted it on the total sum
    for i in range(1, min(int(sqrt(n) + 1), 51)):
        if n % i == 0:
            other = n // i
            ans += other
    return ans

def day20_sum_divisors(n):
    # https://www.vedantu.com/question-answer/find-the-number-of-divisors-and-sum-of-divisors-class-12-maths-cbse-5f83028bed668270c0bd4ceb
    factors = day20_prime_factors(n)
    c = Counter(factors)
    t = 1
    for p in c.keys():
        s = 0
        for i in range(c[p] + 1):
            s += p**i
        t *= s

    return t

def day20_prime_factors(n):
    i = 2
    factors: list[int] = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors

def day20_1(data):
    data = day20_parse(data)

    house = 1
    while house < data:
        ans = 0
        ans = day20_sum_divisors(house) * 10
        if ans >= data:
            # low: 448351
            #      448387
            return house
        house += 1

    assert False

def day20_2(data):
    data = day20_parse(data)

    house = 1
    while house < data:
        ans = 0
        ans = day20_sum_divisors_part2(house) * 11
        if ans >= data:
            return house
        house += 1

    assert False


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
