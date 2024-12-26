# -*- coding: utf-8 -*-
from collections import defaultdict, deque
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable=wrong-import-position
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2016
DAY = 10
EXPECTED_1 = 2
EXPECTED_2 = 30

def day10_parse(data: list[str]):
    insts = {}
    bots = defaultdict(list)
    for line in data:
        parts = line.split(" ")
        if line.startswith("value"):
            # value 5 goes to bot 2
            value, bot = int(parts[1]), int(parts[5])
            bots[bot].append(value)
        else:
            assert line.startswith("bot")
            # bot 2 gives low to bot/output 1 and high to bot/output 0
            bot, low_type, low, high_type, high = int(
                parts[1]), parts[5], int(parts[6]), parts[10], int(parts[11])
            insts[bot] = (low_type, low, high_type, high)
    return insts, bots

def day10_solve(data, part2):
    data = day10_parse(data)
    insts, bots = data
    ready = deque()
    for bot, values in bots.items():
        assert len(values) <= 2
        if len(values) == 2:
            ready.append(bot)
    outputs = {}

    target_min, target_max = 17, 61
    if len(bots.keys()) == 2:
        target_min, target_max = 2, 5

    while ready:
        bot = ready.popleft()
        assert len(bots[bot]) == 2

        low_type, low, high_type, high = insts[bot]
        min_ = min(bots[bot])
        max_ = max(bots[bot])
        bots[bot].clear()
        if min_ == target_min and max_ == target_max and not part2:
            return bot

        if low_type == "bot":
            bots[low].append(min_)
            if len(bots[low]) == 2:
                ready.append(low)
        else:
            assert low_type == "output"
            outputs[low] = min_

        if high_type == "bot":
            bots[high].append(max_)
            if len(bots[high]) == 2:
                ready.append(high)
        else:
            assert high_type == "output"
            outputs[high] = max_

    return outputs[0] * outputs[1] * outputs[2]

def day10_1(data):
    return day10_solve(data, False)

def day10_2(data):
    return day10_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
