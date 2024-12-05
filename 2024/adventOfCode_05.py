# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
from collections import defaultdict
from email.policy import default
import enum
import os
import sys
from typing import Counter, List

from networkx import intersection

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2024
DAY = 5
EXPECTED_1 = 143
EXPECTED_2 = 123


""" DAY 5 """

def day5_parse(data: list[str]):
    i = 0
    ordering = defaultdict(set)
    while data[i]:
        fst, snd = data[i].split("|")
        ordering[int(fst)].add(int(snd))
        i += 1

    i += 1
    updates = []
    while i < len(data):
        pages = data[i].split(",")
        updates.append(list(int(p) for p in pages))
        i += 1

    return ordering, updates

def day5_valid(ordering, update):
    printed = set()
    valid = True
    for page in update:
        if len(printed.intersection(ordering[page])) != 0:
            valid = False
            break
        printed.add(page)
    return valid

def day5_solve(data, part2):
    ordering, updates = day5_parse(data)
    p1 = 0
    incorrect = []
    for update in updates:
        if day5_valid(ordering, update):
            page = update[len(update) // 2]
            p1 += page
        else:
            incorrect.append(update)

    if not part2:
        return p1

    p2 = 0
    for update in incorrect:
        left = set(update)
        correct = []
        while update:
            page = update.pop(0)
            if len(left.intersection(ordering[page])) == 0:
                # final list will be inverted
                # but since we only care about the middle page
                # it will not be relevant
                correct.append(page)
                left.remove(page)
            else:
                update.append(page)

        assert day5_valid(ordering, reversed(correct))

        page = correct[len(correct) // 2]
        p2 += page
    return p2

def day5_1(data):
    return day5_solve(data, False)

def day5_2(data):
    return day5_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
