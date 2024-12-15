# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2016
DAY = 7
EXPECTED_1 = 2
EXPECTED_2 = 3

def day7_parse(data: list[str]):
    ips = []
    for line in data:
        curr = ""
        outside, inside = [], []
        for _, c in enumerate(line):
            if c == "]":
                inside.append(curr)
                curr = ""
            elif c == "[":
                outside.append(curr)
                curr = ""
            else:
                curr += c
        outside.append(curr)
        ips.append((outside, inside))

    return ips

def day7_abba(sequence, size):
    i = 0
    matches: list[str] = []
    while i <= len(sequence) - size:
        if (sequence[i] == sequence[i + size - 1]) and \
           (sequence[i + 1] == sequence[i + size - 2]) and \
           (sequence[i] != sequence[i + 1]):
            matches.append("".join(sequence[i:i + size]))
        i += 1
    return matches

def day7_solve(data, part2):
    data = day7_parse(data)
    ips = data
    ans = 0
    size = 3 if part2 else 4
    for outside, inside in ips:
        outside_matches = []
        inside_matches = []
        for o in outside:
            outside_matches += day7_abba(o, size)
        for i in inside:
            inside_matches += day7_abba(i, size)
        if not part2:
            if len(outside_matches) > 0 and len(inside_matches) == 0:
                ans += 1
        else:
            for match in outside_matches:
                reverse_match = match[1] + match[0] + match[1]
                if reverse_match in inside_matches:
                    ans += 1
                    break
    return ans

def day7_1(data):
    return day7_solve(data, False)

def day7_2(data):
    # 247 high
    return day7_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
