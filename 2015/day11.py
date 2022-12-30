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
DAY = 11
EXPECTED_1 = "abcdffaa"
EXPECTED_2 = None


""" DAY 11 """

def day11_parse(data):
    return data[0]

def day11_next_word(word):
    word = list(word)
    valid = False
    while not valid:
        i = len(word) - 1
        keep_increasing = True
        while keep_increasing:
            if word[i] == "z":
                word[i] = "a"
                i -= 1
            else:
                word[i] = chr(ord(word[i]) + 1)
                keep_increasing = False

        # a sequence of 3
        for j in range(len(word) - 2):
            if ord(word[j]) + 1 == ord(word[j + 1]) and \
               ord(word[j + 1]) + 1 == ord(word[j + 2]):
                valid = True
                break
        if not valid:
            continue

        # Can't contain i, o or l
        if "i" in word or "o" in word or "l" in word:
            valid = False
            continue

        # at least 2 distinct pairs
        indexes = defaultdict(list)
        for idx, c in enumerate(word):
            indexes[c].append(idx)

        counter = 0
        for c, indexes in indexes.items():
            for j in range(len(indexes) - 1):
                if indexes[j] + 1 == indexes[j + 1]:
                    counter += 1
                    break
        valid = counter >= 2

    return "".join(word)

def day11_1(data):
    data = day11_parse(data)
    return day11_next_word(data)

def day11_2(data):
    data = day11_parse(data)
    data = day11_next_word(data)
    return day11_next_word(data)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
