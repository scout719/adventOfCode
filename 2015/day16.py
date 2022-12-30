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
DAY = 16
EXPECTED_1 = None
EXPECTED_2 = None


""" DAY 16 """

def day16_parse(data):
    aunts = defaultdict(dict)
    for line in data:
        words = line.split()
        aunt_i = int(words[1][:-1])
        rest = line.split(f"{aunt_i}: ")[1]
        parts = rest.split(", ")
        for part in parts:
            compound, value = part.split(": ")
            value = int(value)
            aunts[aunt_i][compound] = value

    return aunts

def day16_1(data):
    target = {
        "children": 3,
        "cats": 7,
        "samoyeds": 2,
        "pomeranians": 3,
        "akitas": 0,
        "vizslas": 0,
        "goldfish": 5,
        "trees": 3,
        "cars": 2,
        "perfumes": 1,
    }
    aunts = day16_parse(data)
    for aunt_i, compounds in aunts.items():
        matches = 0
        for compound, value in compounds.items():
            if target[compound] == value:
                matches += 1
        if len(compounds) == matches:
            return aunt_i
    assert False

def day16_2(data):
    target = {
        "children": 3,
        "cats": 7,
        "samoyeds": 2,
        "pomeranians": 3,
        "akitas": 0,
        "vizslas": 0,
        "goldfish": 5,
        "trees": 3,
        "cars": 2,
        "perfumes": 1,
    }
    aunts = day16_parse(data)
    for aunt_i, compounds in aunts.items():
        matches = 0
        for compound, value in compounds.items():
            if compound in ["cats", "trees"]:
                if target[compound] < value:
                    matches += 1
            elif compound in ["pomeranians", "goldfish"]:
                if target[compound] > value:
                    matches += 1
            else:
                if target[compound] == value:
                    matches += 1
        if len(compounds) == matches:
            return aunt_i
    assert False


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
