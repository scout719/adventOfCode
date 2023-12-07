# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
import os
import sys
from collections import defaultdict
from typing import List

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import day_with_validation  # NOQA: E402
from common.utils import main  # NOQA: E402

YEAR = 2023
DAY = 7
EXPECTED_1 = 6440
EXPECTED_2 = 5905


""" DAY 7 """

def day7_parse(data: List[str]):
    return [(line.split()[0], int(line.split()[1])) for line in data]

def day7_strength(card, part2: bool):
    cards = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
    if part2:
        # J is the least valuable
        cards.remove("J")
        cards.append("J")
    S: List[str] = list(reversed(cards))
    assert card in S, card
    return S.index(card)

def day7_key(hand, part2):
    counts = defaultdict(int)
    for c in hand:
        counts[c] += 1
    s_counts = []
    for k, v in counts.items():
        if k == "J" and part2:
            # skip J's
            continue
        s_counts.append([v, k])

    s_counts = sorted(s_counts, reverse=True)

    if part2:
        # add J count to highest
        J_c = counts["J"]
        if len(s_counts) == 0:
            # only J
            s_counts = [[5, "J"]]
        s_counts[0][0] += J_c

    if len(s_counts) == 1:
        hand_type = 6
    elif s_counts[0][0] == 4:
        hand_type = 5
    elif s_counts[0][0] == 3 and s_counts[1][0] == 2:
        hand_type = 4
    elif s_counts[0][0] == 3 and len(s_counts) == 3:
        hand_type = 3
    elif s_counts[0][0] == 2 and s_counts[1][0] == 2:
        hand_type = 2
    elif s_counts[0][0] == 2 and len(s_counts) == 4:
        hand_type = 1
    else:
        assert len(s_counts) == 5
        hand_type = 0

    strengths = [day7_strength(card, part2) for card in hand]
    return hand_type, strengths

def day7_solve(data, part2):
    hands = day7_parse(data)
    hands = sorted(hands, key=lambda k: day7_key(k[0], part2), reverse=False)
    hands_only = [hand[0] for hand in hands]
    assert len(hands_only) == len(set(hands_only))
    ans = 0
    for i, hand in enumerate(hands):
        ans += (i + 1) * hand[1]
    return ans

def day7_1(data: List[str]):
    # 247898031 low
    # 248843302 hig
    return day7_solve(data, False)

def day7_2(data: List[str]):
    return day7_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
