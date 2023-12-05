# -*- coding: utf-8 -*-
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable=wrong-import-position
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2015
DAY = 17
EXPECTED_1 = 4
EXPECTED_2 = 3


""" DAY 17 """

def day17_parse(data):
    return [int(line) for line in data]

def day17_solve(remaining, containers):
    if remaining == 0:
        return []

    result = []
    for i, container in enumerate(containers):
        if remaining == container:
            result.append([container])
        elif remaining > container:
            inner_results = day17_solve(
                remaining - container, containers[i + 1:])
            if inner_results:
                for inner_results in inner_results:
                    result.append([container] + inner_results)
    return result

def day17_1(data):
    containers = day17_parse(data)
    eggnog = 150
    if len(containers) == 5:
        eggnog = 25
    return len(day17_solve(eggnog, containers))

def day17_2(data):
    containers = day17_parse(data)
    eggnog = 150
    if len(containers) == 5:
        eggnog = 25
    combinations = day17_solve(eggnog, containers)
    min_containers = min(len(comb) for comb in combinations)

    return sum(1 for comb in combinations if len(comb) == min_containers)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
