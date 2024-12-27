# -*- coding: utf-8 -*-
from collections import deque
from copy import deepcopy
import functools
from hashlib import md5
import os
import sys
from typing import Counter

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable=wrong-import-position
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2016
DAY = 14
EXPECTED_1 = 22728
EXPECTED_2 = None # 22551

def day14_parse(data: list[str]):
    return data[0]

@functools.cache
def day14_get(salt, i, part2):
    val = md5(f"{salt}{i}".encode()).hexdigest()
    if not part2:
        return val

    for _ in range(2016):
        val = md5(val.encode()).hexdigest()
    return val

@functools.cache
def day14_is_key(salt, i, v, part2):
    for t in range(1, 1001):
        nxt = day14_get(salt, i + t, part2)
        if v * 5 in nxt:
            return True

    return False

def day14_solve(data, part2):
    data = day14_parse(data)
    salt = data

    i = 0
    keys_idx = []
    while len(keys_idx) < 64:
        nxt = day14_get(salt, i, part2)
        c = nxt[0]
        j = 0
        a, b, c = None, nxt[0], nxt[1]
        while j <= len(nxt) - 3:
            a, b, c = b, c, nxt[j + 2]
            if a == b == c:
                if day14_is_key(salt, i, a, part2):
                    keys_idx.append(i)
                break
            j += 1
        i += 1
    return keys_idx[-1]

def day14_1(data):
    # high 291
    # high 283
    return day14_solve(data, False)

def day14_2(data):
    return day14_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
