# -*- coding: utf-8 -*-
# pylint: disable=import-error
# pylint: disable=unused-import
# pylint: disable=wildcard-import
# pylint: disable=wrong-import-position
# pylint: disable=consider-using-enumerate
import os
import sys
from collections import defaultdict
from heapq import heappop, heappush

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import read_input, main, clear  # NOQA: E402
from common.utils import day_with_validation, bcolors, WHITE_CIRCLE, WHITE_SQUARE  # NOQA: E402
from common.utils import BLUE_CIRCLE, RED_SMALL_SQUARE  # NOQA: E402
from common.utils import EXERCISE_TIMEOUT  # NOQA: E402
# pylint: enable=import-error
# pylint: enable=wrong-import-position

YEAR = 2015
DAY = 19
EXPECTED_1 = 7
EXPECTED_2 = 6


""" DAY 19 """

def day19_parse(data: list[str]):
    i = 0
    rules: defaultdict[str, list[str]] = defaultdict(list)
    while i < len(data):
        line = data[i]
        if not line:
            molecule = data[i + 1]
            break
        words = line.split()
        rules[words[0]].append(words[2])
        i += 1

    return rules, molecule

def day19_replace(molecule: str, rules: defaultdict):
    for key, values in rules.items():
        for replacement in values:
            idx = molecule.find(key)
            while idx != -1:
                yield molecule[:idx] + replacement + molecule[idx + len(key):]
                idx = molecule.find(key, idx + 1)

def day19_replace_reverse(molecule, rules):
    for key, values in rules:
        for replacement in values:
            idx = molecule.find(replacement)
            while idx != -1:
                yield molecule[:idx] + key + molecule[idx + len(replacement):]
                idx = molecule.find(replacement, idx + 1)

def day19_1(data):
    R, molecule = day19_parse(data)
    return len(set(day19_replace(molecule, R)))

def day19_iterative(rules, start, target):
    q: list[tuple[int, str]] = [(0, start)]
    seen = set()
    while q:
        steps, curr = heappop(q)
        if curr == target:
            return steps

        if curr in seen:
            continue
        seen.add((curr))

        for replacement in day19_replace_reverse(curr, rules):
            heappush(q, (steps + 1, replacement))
    return None

def day19_get_pairings(molecule):
    stack: list[int] = []
    for i in range(len(molecule)):
        if molecule[i:].startswith("Rn"):
            stack.append(i)
        elif molecule[i:].startswith("Ar"):
            return stack.pop(), i
    return None

def day19_recurse(R, steps: int, curr, target):
    if curr == target:
        return steps

    for rep in day19_replace_reverse(curr, R):
        total_steps = day19_recurse(R, steps + 1, rep, target)
        if total_steps:
            return total_steps

    return None

def day19_2(data):
    rules, molecule = day19_parse(data)
    # Reversing the rules makes it find the molecule faster 🤯
    items = list(reversed(list(rules.items())))
    return day19_recurse(items, 0, molecule, "e")


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
