# -*- coding: utf-8 -*-
import os
import sys
from collections import defaultdict

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable=wrong-import-position
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2015
DAY = 13
EXPECTED_1 = 330
EXPECTED_2 = None


""" DAY 13 """

def day13_parse(data):
    happiness_change = defaultdict(dict)
    for line in data:
        words = line.split()
        curr = words[0]
        gainOrLoss = words[2]
        val = int(words[3])
        if gainOrLoss == "lose":
            val = -val
        other = words[10][:-1]
        happiness_change[curr][other] = val

    return happiness_change

def day13_total(happiness, table):
    i = 0
    total = 0
    while i < len(table) - 1:
        total += happiness[table[i]][table[i + 1]]
        total += happiness[table[i + 1]][table[i]]
        i += 1
    total += happiness[table[-1]][table[0]]
    total += happiness[table[0]][table[-1]]
    return total

def day13_permutations(names):
    if len(names) == 1:
        return [names]
    curr = names[0]
    others = day13_permutations(names[1:])
    res = []
    for perm in others:
        for i in range(len(perm)):
            res.append(perm[:i] + [curr] + perm[i:])
    return res

def day13_1(data):
    happiness = day13_parse(data)
    all_perms = day13_permutations(list(happiness.keys()))
    best = 0
    for perm in all_perms:
        best = max(best, day13_total(happiness, perm))
    return best

def day13_2(data):
    happiness = day13_parse(data)
    for k in list(happiness.keys()):
        happiness["me"][k] = 0
        happiness[k]["me"] = 0
    all_perms = day13_permutations(list(happiness.keys()))
    best = 0
    for perm in all_perms:
        best = max(best, day13_total(happiness, perm))
    return best


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
