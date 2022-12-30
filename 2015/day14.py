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
DAY = 14
EXPECTED_1 = None
EXPECTED_2 = 689


""" DAY 14 """

def day14_parse(data):
    reindeers = {}
    for line in data:
        words = line.split()
        reindeer = words[0]
        speed = int(words[3])
        fly_time = int(words[6])
        rest_time = int(words[13])
        reindeers[reindeer] = (speed, fly_time, rest_time)
    return reindeers

def day14_get_state(reindeers, reindeer, t):
    speed, fly_time, rest_time = reindeers[reindeer]
    i = 0
    distance = 0
    while i < t:
        curr = i % (fly_time + rest_time)
        if curr < fly_time:
            distance += speed
        i += 1
    return distance

def day14_1(data):
    reindeers = day14_parse(data)
    best = 0
    for reindeer in reindeers.keys():
        best = max(best, day14_get_state(reindeers, reindeer, 2503))
    return best

def day14_2(data):
    reindeers = day14_parse(data)
    score = defaultdict(int)
    max_t = 2503
    if len(reindeers) == 2:
        max_t = 1000
    for t in range(1, max_t):
        curr = [(r, day14_get_state(reindeers, r, t)) for r in reindeers]
        front = max([dist for _, dist in curr])
        leaders = [r for r, dist in curr if dist == front]
        for leader in leaders:
            score[leader] += 1
    return max(score.values())


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
