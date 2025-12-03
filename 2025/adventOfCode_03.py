# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2025
DAY = 3
EXPECTED_1 = 357
EXPECTED_2 = 3121910778619

def day3_parse(data: list[str]):
    banks = []
    for line in data:
        bank = []
        for battery in line:
            bank.append(int(battery))
        banks.append(bank)
    return banks

def day3_solve(data, part2):
    banks = day3_parse(data)

    joltage_size = 2 if not part2 else 12
    total = 0
    for bank in banks:
        acc = 0
        for used in range(1, joltage_size + 1):
            # We must leave some batteries left at the end to fullfill the rest of the joltage
            remaining = joltage_size - used
            slice_idx = -remaining if remaining > 0 else len(bank)

            largest = max(bank[:slice_idx])
            acc = acc * 10 + largest

            # Drop all batteries up to the used one
            idx = bank.index(largest)
            bank = bank[idx + 1:]
        total += acc

    return total

def day3_1(data):
    return day3_solve(data, False)

def day3_2(data):
    return day3_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
