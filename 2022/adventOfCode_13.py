# -*- coding: utf-8 -*-
# pylint: disable=import-error
# pylint: disable=unused-import
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# pylint: disable=wrong-import-position
# pylint: disable=consider-using-enumerate
from functools import cmp_to_key
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main, day_with_validation  # NOQA: E402
# pylint: enable=import-error
# pylint: enable=wrong-import-position

YEAR = 2022
DAY = 13
EXPECTED_1 = 13
EXPECTED_2 = 140


""" DAY 13 """

def day13_parse(data):
    pairs = []
    curr = []
    for line in data:
        if not line:
            pairs.append(curr)
            curr = []
        else:
            curr.append(eval(line))
    pairs.append(curr)
    return pairs

def day13_compare(left, right):
    # return None if they are equal
    result = None
    if isinstance(left, int) and isinstance(right, int):
        # both ints, compare between then
        if left > right:
            result = False
        elif right > left:
            result = True
    elif isinstance(left, list) and isinstance(right, list):
        # both lists, go through each item and compare
        # stop on the first non tie
        in_order = None
        i = 0
        while i < len(left) and i < len(right):
            left_e = left[i]
            right_e = right[i]

            comparison = day13_compare(left_e, right_e)
            if not comparison is None:
                in_order = comparison
                break
            i += 1
        if in_order is None:
            # All items were equal, so we must compare the lengths
            if len(left) < len(right):
                # ran out of left elements
                in_order = True
            elif len(left) > len(right):
                # ran out of right elements
                in_order = False
        result = in_order
    elif isinstance(left, int):
        result = day13_compare([left], right)
    else:
        result = day13_compare(left, [right])
    return result

def day13_1(pairs):
    pairs = day13_parse(pairs)
    in_order = []
    for i, pair in enumerate(pairs):
        result = day13_compare(pair[0], pair[1])
        if result is None or result:
            # in_order or equal
            in_order.append(i + 1)

    # 7066
    # 2804
    # 5509
    return sum(in_order)

def day13_cmp(item1, item2):
    r = day13_compare(item1, item2)
    if r is None:
        return 0
    return -1 if r else 1

def day13_2(pairs):
    pairs = day13_parse(pairs)
    packets = []
    for pair in pairs:
        packets.append(pair[0])
        packets.append(pair[1])
    packets.append([[2]])
    packets.append([[6]])
    sorted_packs = sorted(packets, key=cmp_to_key(day13_cmp))

    in_order = []
    for i, packet in enumerate(sorted_packs):
        res = day13_compare(packet, [[2]])
        if res is None:
            in_order.append(i + 1)
        res = day13_compare(packet, [[6]])
        if res is None:
            in_order.append(i + 1)
    return in_order[0] * in_order[1]


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
