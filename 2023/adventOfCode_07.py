# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
import os
import sys
from collections import defaultdict
from functools import cmp_to_key
import math
from typing import List, Tuple, Set, Dict

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import day_with_validation  # NOQA: E402
from common.utils import main  # NOQA: E402

Card = Tuple[int, Set[int], Set[int]]

YEAR = 2023
DAY = 7
EXPECTED_1 = 6440
EXPECTED_2 = 5905


""" DAY 7 """

def day7_parse(data: List[str]):
    return [(line.split()[0], int(line.split()[1])) for line in data]

def day7_strength(card):
    M: List[str] = list(reversed(["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]))
    assert card in M, card
    return M.index(card)

def day7_strength2(card):
    M: List[str] = list(reversed(["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]))
    assert card in M, card
    return M.index(card)

def day7_type(hand):
    counts = defaultdict(int)
    for c in hand:
        counts[c]+=1
    s_counts = []
    for k,v in counts.items():
        s_counts.append((v,k))
    s_counts = sorted(s_counts, reverse=True)

    if len(s_counts) == 1:
        return 6
    if s_counts[0][0] == 4:
        return 5
    if s_counts[0][0] == 3 and s_counts[1][0] == 2:
        return 4
    if s_counts[0][0] == 3 and len(s_counts) == 3:
        return 3
    if s_counts[0][0] == 2 and s_counts[1][0] == 2:
        return 2
    if s_counts[0][0] == 2 and len(s_counts) == 4:
        return 1
    assert len(s_counts) == 5
    return 0

def day7_type2(hand):
    counts = defaultdict(int)
    for c in hand:
        counts[c]+=1
    s_counts = []
    for k,v in counts.items():
        if k == "J":
            continue
        s_counts.append([v,k])

    s_counts = sorted(s_counts, reverse=True)
    J_c = counts["J"]
    if len(s_counts) == 0:
        # only J
        s_counts = [[5,"J"]]
    s_counts[0][0] += J_c

    if len(s_counts) == 1:
        return 6
    if s_counts[0][0] == 4:
        return 5
    if s_counts[0][0] == 3 and s_counts[1][0] == 2:
        return 4
    if s_counts[0][0] == 3 and len(s_counts) == 3:
        return 3
    if s_counts[0][0] == 2 and s_counts[1][0] == 2:
        return 2
    if s_counts[0][0] == 2 and len(s_counts) == 4:
        return 1
    assert len(s_counts) == 5
    return 0

def day7_sort(a: Tuple[str,int],b: Tuple[str,int]) -> int:
    type_a = day7_type(a[0])
    type_b = day7_type(b[0])
    if type_a != type_b:
        return type_a-type_b
    for i in range(len(a[0])):
        s_a = day7_strength(a[0][i])
        s_b = day7_strength(b[0][i])
        if s_a != s_b:
            return s_a-s_b
    return 0

def day7_sort2(a: Tuple[str,int],b: Tuple[str,int]) -> int:
    type_a = day7_type2(a[0])
    type_b = day7_type2(b[0])
    if type_a != type_b:
        return type_a-type_b
    for i in range(len(a[0])):
        s_a = day7_strength2(a[0][i])
        s_b = day7_strength2(b[0][i])
        if s_a != s_b:
            return s_a-s_b
    return 0

def day7_1(data: List[str]):
    hands = day7_parse(data)
    hands = sorted(hands, key=cmp_to_key(day7_sort), reverse=False)
    hands_only = [hand[0] for hand in hands]
    assert len(hands_only) == len(set(hands_only))
    ans = 0
    for i, hand in enumerate(hands):
        ans += (i+1)*hand[1]
    # 247898031 low
    # 248843302 hig
    return ans

def day7_2(data: List[str]):
    hands = day7_parse(data)
    hands = sorted(hands, key=cmp_to_key(day7_sort2), reverse=False)
    hands_only = [hand[0] for hand in hands]
    assert len(hands_only) == len(set(hands_only))
    ans = 0
    for i, hand in enumerate(hands):
        ans += (i+1)*hand[1]
    return ans


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
