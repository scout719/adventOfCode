# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2024
DAY = 3
EXPECTED_1 = 161
EXPECTED_2 = 48


""" DAY 3 """

def day3_parse(data) -> str:
    return "".join(data)

def day3_solve(data, part2):
    data = day3_parse(data)
    mults = []
    # if we're parsing numbers
    is_number = False
    # if we're parsing the first multiplier
    is_first = False
    # (part2) if mul operations are enabled
    enabled = True
    # To hold the first multiplier
    first = ""
    # To hold the second multiplier
    second = ""
    i = 0
    while i < len(data):
        if part2:
            if enabled and data[i:i + 7] == "don't()":
                enabled = False
                i += 7
                continue

            if not enabled and data[i:i + 4] == "do()":
                enabled = True
                i += 4
                continue

            if not enabled:
                i += 1
                continue

        reset = False
        if is_number:
            # Looking for numbers
            if data[i].isdigit():
                if is_first:
                    first += data[i]
                else:
                    second += data[i]
            elif data[i] == ",":
                if is_first:
                    is_first = False
                else:
                    reset = True
            elif data[i] == ")":
                if not is_first:
                    mults.append((int(first), int(second)))
                reset = True
            else:
                reset = True
        else:
            # Searching for a new mul op
            if data[i:i + 4] == "mul(":
                is_number = True
                is_first = True
                i += 4
                continue

            reset = True

        if reset:
            is_number = False
            is_first = False
            first = ""
            second = ""
        i += 1

    # low 28519300
    return sum(x * y for x, y in mults)

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
