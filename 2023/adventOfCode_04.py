# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
import os
import sys
from typing import List, Tuple, Set, Dict

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import day_with_validation  # NOQA: E402
from common.utils import main  # NOQA: E402

Card = Tuple[int, Set[int], Set[int]]

YEAR = 2023
DAY = 4
EXPECTED_1 = 13
EXPECTED_2 = 30


""" DAY 4 """

def day4_parse(data: List[str]):
    cards: List[Card] = []
    for line in data:
        line = line.replace("  ", " ")
        parts = line.split(": ")
        game = int(parts[0].split(" ")[-1])
        win, have = parts[1].split(" | ")
        win = {int(x) for x in win.split(" ")}
        have = {int(x) for x in have.split(" ")}
        cards.append((game, win, have))

    return cards

def day4_1(data: List[str]):
    cards = day4_parse(data)
    ans = 0
    for _, win, have in cards:
        score = 0
        for curr_win in win:
            if curr_win in have:
                if score == 0:
                    score = 1
                else:
                    score *= 2
        ans += score

    return ans

def day4_solve(mem: Dict[int, int], cards: List[Card], curr: int):
    if curr in mem:
        return mem[curr]

    _, win, have = cards[curr]
    ans = 0
    next_award = curr + 1
    for w in win:
        for h in have:
            if w == h:
                # We get one more card
                ans += 1
                # Plus all the ones the new card wins us
                ans += day4_solve(mem, cards, next_award)
                next_award += 1

    mem[curr] = ans
    return ans

def day4_2(data: List[str]):
    cards = day4_parse(data)

    mem: Dict[int, int] = {}
    ans = 0
    for c in range(len(cards)):
        ans += day4_solve(mem, cards, c) + 1

    return ans


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
