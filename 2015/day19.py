# -*- coding: utf-8 -*-
# pylint: disable=import-error
# pylint: disable=unused-import
# pylint: disable=wildcard-import
# pylint: disable=wrong-import-position
# pylint: disable=consider-using-enumerate
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
from difflib import SequenceMatcher


FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import read_input, main, clear  # NOQA: E402
from common.utils import day_with_validation, bcolors, WHITE_CIRCLE, WHITE_SQUARE  # NOQA: E402
from common.utils import BLUE_CIRCLE, RED_SMALL_SQUARE  # NOQA: E402
# pylint: enable=import-error
# pylint: enable=wrong-import-position

YEAR = 2015
DAY = 19
EXPECTED_1 = 7
EXPECTED_2 = 6


""" DAY 19 """

def day19_parse(data):
    i = 0
    R = defaultdict(list)
    while i < len(data):
        line = data[i]
        if not line:
            molecule = data[i + 1]
            break
        words = line.split()
        R[words[0]].append(words[2])
        i += 1

    return R, molecule

def day19_replace(molecule: str, R: defaultdict) -> set:
    res = set()
    for k, v in R.items():
        for r in v:
            idx = []
            i = 0
            while molecule.find(k, i) != -1:
                f = molecule.find(k, i)
                idx.append(f)
                i = f + 1

            for i in idx:
                curr = molecule[:i] + r + molecule[i + len(k):]
                res.add(curr)
    return res

def day19_replace_reverse(molecule: str, R: defaultdict) -> set:
    res = set()
    for k, v in R.items():
        for r in v:
            idx = []
            i = 0
            while molecule.find(r, i) != -1:
                f = molecule.find(r, i)
                idx.append(f)
                i = f + 1

            for i in idx:
                curr = molecule[:i] + k + molecule[i + len(r):]
                res.add(curr)
    return res

def day19_cost(e, molecule):
    i = 0
    while i < len(molecule) and i < len(e):
        if molecule[i] != e[i]:
            break
        i += 1
    return (-i)
    return (-len(e), -SequenceMatcher(None, e, molecule).ratio(), -i)

def day19_1(data):
    R, molecule = day19_parse(data)
    return len(day19_replace(molecule, R))

def day19_2(data):
    # R, molecule = day19_parse(data)

    # q = [(0, 0, molecule)]
    # seen = set()
    # while q:
    #     cost, steps, curr = heappop(q)
    #     if curr == "e":
    #         return steps

    #     # if len(curr) > len(molecule):
    #     #     continue

    #     if curr in seen:
    #         continue
    #     seen.add((curr))

    #     print(curr)
    #     for rep in day19_replace_reverse(curr, R):
    #         heappush(q, (len(rep), steps + 1, rep))
    #         # q.appendleft((steps + 1, rep))

    # assert False

    R, molecule = day19_parse(data)

    q = [(day19_cost("e", molecule), 0, "e")]
    seen = set()
    while q:
        cost, steps, curr = heappop(q)
        if curr == molecule:
            return steps

        if len(curr) >= len(molecule):
            continue

        if curr in seen:
            continue
        seen.add((curr))

        print(len(curr), curr)
        for rep in day19_replace(curr, R):
            heappush(q, (day19_cost(rep, molecule), steps + 1, rep))
            # q.appendleft((steps + 1, rep))

    assert False


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
