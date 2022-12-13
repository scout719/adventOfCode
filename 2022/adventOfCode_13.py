# -*- coding: utf-8 -*-
# pylint: disable=import-error
# pylint: disable=unused-import
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# pylint: disable=wrong-import-position
# pylint: disable=consider-using-enumerate
from struct import pack
from typing import Callable, Dict, Iterator, Union, Optional, List, ChainMap
import functools
import math
import os
from os.path import join
import sys
import time
from copy import deepcopy
from collections import Counter, defaultdict, deque
from heapq import heappop, heappush

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

def day13_compare(l, r):
    res = None
    if type(l) is int and type(r) is int:
        if l > r:
            res = False
        elif r > l:
            res = True
    elif type(l) is list and type(r) is list:
        in_order = None
        # print("oi")
        for n, ll in enumerate(l):
            if n >= len(r):
                in_order = False
                break
            rr = r[n]
            # print(ll,rr)

            comp = day13_compare(ll, rr)
            if not comp is None:
                in_order = comp
                break
        # in_order &= not len(r) > len(l)
        if in_order is None:
            if len(l) < len(r):
                in_order = True
            # if len(l) > len(r):
                # in_order = False
        res = in_order
    elif type(l) is int:
        res = day13_compare([l], r)
    else:
        res = day13_compare(l, [r])
    # print(l,r, res)
    return res

def day13_1(data):
    data = day13_parse(data)
    in_order = []
    for n, pair in enumerate(data):
        # print("###")
        res = day13_compare(pair[0], pair[1])
        if res is None or res:
            in_order.append(n+1)

    # 7066
    # 2804
    # 5509
    # 4894
    return sum(in_order)

def compare(item1, item2):
    r = day13_compare(item1, item2)
    if r is None:
        return 0
    return -1 if r else 1


def day13_2(data):    
    data = day13_parse(data)
    packets = []
    for pair in data:
        packets.append(pair[0])
        packets.append(pair[1])
    packets.append([[2]])
    packets.append([[6]])
    print(packets)
    # Calling
    from functools import cmp_to_key
    new_packs = sorted(data, key=cmp_to_key(compare))
    in_order = []
    print(new_packs)
    for n, packet in enumerate(new_packs):
        # print("###")
        res = day13_compare(packet, [[2]])
        if res is None:
            in_order.append(n+1)
        res = day13_compare(packet, [[6]])
        if res is None:
            in_order.append(n+1)
    # prin
    print(in_order)
    return in_order[0] * in_order[1]


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
