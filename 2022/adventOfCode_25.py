# -*- coding: utf-8 -*-
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable=wrong-import-position
from common.utils import day_with_validation, main   # NOQA: E402

YEAR = 2022
DAY = 25
EXPECTED_1 = "2=-1=0"
EXPECTED_2 = None

""" DAY 25 """

def day25_parse(data):
    numbers = []
    for line in data:
        numbers.append(line)
    return numbers

def day25_in_snafu(number):
    exponent = 1
    while exponent < number:
        exponent *= 5
    exponent //= 5

    rest = number
    digits = []
    while exponent != 0:
        digit = rest // exponent
        rest = rest - (digit * exponent)
        exponent //= 5
        digits.append(digit)

    for i in range(len(digits) - 1, 0, -1):
        exponent = digits[i]
        if exponent == 3:
            digits[i - 1] += 1
            digits[i] = "="
        elif exponent == 4:
            digits[i - 1] += 1
            digits[i] = "-"
        elif exponent == 5:
            digits[i - 1] += 1
            digits[i] = "0"
        else:
            assert exponent in [2, 1, 0], exponent
            digits[i] = str(exponent)

    if digits[0] == 3:
        digits[0] = "="
        digits = ["1"] + digits
    elif digits[0] == 4:
        digits[0] = "-"
        digits = ["1"] + digits
    elif digits[0] == 5:
        digits[0] = "0"
        digits = ["1"] + digits
    else:
        assert digits[0] in [0, 1, 2], digits
        digits[0] = str(digits[0])
    return "".join(digits)

def day25_1(data):
    numbers = day25_parse(data)
    total = 0
    for number in numbers:
        exponent = 1
        value_base_10 = 0
        for i in range(len(number) - 1, -1, -1):
            digit = number[i]
            if digit == "0":
                pass
            elif digit == "1":
                value_base_10 += exponent
            elif digit == "2":
                value_base_10 += 2 * exponent
            elif digit == "-":
                value_base_10 -= exponent
            else:
                assert digit == "="
                value_base_10 -= 2 * exponent
            exponent *= 5
        assert number == day25_in_snafu(value_base_10), \
            (number, value_base_10, day25_in_snafu(value_base_10))
        total += value_base_10
    return day25_in_snafu(total)

def day25_2(_):
    return "Merry Christmas!"


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
