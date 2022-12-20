# -*- coding: utf-8 -*-
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable-next=wrong-import-position
from common.utils import day_with_validation, main  # NOQA: E402

YEAR = 2022
DAY = 20
EXPECTED_1 = 3
EXPECTED_2 = 1623178306


""" DAY 20 """

def day20_parse(data):
    values = []
    for value in data:
        values.append(int(value))
    return values

def day20_mix(original_list, index_mapping):
    i = 0
    while i < len(original_list):
        curr_value = original_list[i]
        if curr_value == 0:
            n_signal = 0
        else:
            n_signal = abs(curr_value) // curr_value
        # Wrap around
        actual_jumps = abs(curr_value) % (len(original_list) - 1)
        curr_value = actual_jumps * n_signal
        curr_i = index_mapping.index(i)
        j = 0
        while j != curr_value:
            pos1 = (curr_i + j) % len(original_list)
            pos2 = (curr_i + j + n_signal) % len(original_list)
            tmp = index_mapping[pos2]
            index_mapping[pos2] = index_mapping[pos1]
            index_mapping[pos1] = tmp
            j += n_signal
        i += 1

def day20_1(data):
    values = day20_parse(data)

    index_mapping = list(range(len(values)))
    zero_pos = values.index(0)
    day20_mix(values, index_mapping)
    new_zero_pos = index_mapping.index(zero_pos)
    return \
        values[index_mapping[(new_zero_pos + 1000) % len(index_mapping)]] + \
        values[index_mapping[(new_zero_pos + 2000) % len(index_mapping)]] + \
        values[index_mapping[(new_zero_pos + 3000) % len(index_mapping)]]


def day20_2(data):
    values = day20_parse(data)
    key = 811589153

    values = [value * key for value in values]
    index_mapping = list(range(len(values)))
    zero_pos = values.index(0)
    for _ in range(10):
        day20_mix(values, index_mapping)
    new_zero_pos = index_mapping.index(zero_pos)
    return \
        values[index_mapping[(new_zero_pos + 1000) % len(index_mapping)]] + \
        values[index_mapping[(new_zero_pos + 2000) % len(index_mapping)]] + \
        values[index_mapping[(new_zero_pos + 3000) % len(index_mapping)]]


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
