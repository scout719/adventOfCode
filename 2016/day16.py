# -*- coding: utf-8 -*-
import functools
import math
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
DAY = 16
EXPECTED_1 = "01100"
EXPECTED_2 = None

def day16_parse(data: list[str]):
    return data[0]

def day16_generate(a: str):
    b = "".join(reversed(a)).replace(
        "0", "X").replace("1", "0").replace("X", "1")
    return a + "0" + b

@functools.cache
def day16_checksum(a):
    # 00000000000000000000
    #  . . . . . . . . . .
    #    .   .   .   .   .

    assert len(a) % 2 == 0
    if len(a) == 2:
        return "1" if a[0] == a[1] else "0"

    size = len(a)
    partition_size = 0
    while size % 2 == 0:
        partition_size += 1
        size = size // 2

    assert len(a) % 2**partition_size == 0
    if 2**partition_size == len(a):
        # if length is a perfect square
        # we need to downsize it to avoid loops
        partition_size -= 1

    checksum = ""
    i = 0
    while i < len(a):
        checksum += day16_checksum(a[i:i + 2**partition_size])
        i += 2**partition_size

    if len(checksum) % 2 == 0:
        # In perfect squares we need to do one final join
        assert 2**(partition_size + 1) == len(a)
        checksum = day16_checksum(checksum)

    assert len(checksum) % 2 != 0
    return checksum

def day16_solve(data, part2):
    data = day16_parse(data)
    initial = data
    sz = 272
    if len(initial) < 8:
        sz = 20

    if part2:
        sz = 35651584

    gen_data = initial
    while len(gen_data) < sz:
        gen_data = day16_generate(gen_data)

    gen_data = gen_data[:sz]
    return day16_checksum(gen_data)

def day16_1(data):
    return day16_solve(data, False)

def day16_2(data):
    return day16_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
