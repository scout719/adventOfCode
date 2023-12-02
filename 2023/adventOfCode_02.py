# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
from collections import defaultdict
import os
import sys
from typing import List

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2023
DAY = 2
EXPECTED_1 = 8
EXPECTED_2 = 2286


""" DAY 2 """

def day2_parse(data: List[str]):
    games = defaultdict(int)
    for line in data:
        game, rest = line.split(": ")
        game = int(game.replace("Game ", ""))
        rest = rest.split("; ")
        sets = [s.split(", ") for s in rest]
        sets = [{c.split(" ")[1]: int(c.split(" ")[0])
                 for c in s} for s in sets]
        games[game] = sets
    return games

def day2_1(data: List[str]):
    games = day2_parse(data)
    red = 12
    green = 13
    blue = 14
    all_g = set(games.keys())
    for g in games:
        for s in games[g]:
            if "red" in s and s["red"] > red or \
               "green" in s and s["green"] > green or \
               "blue" in s and s["blue"] > blue:
                all_g -= set([g])
    return sum(all_g)

def day2_2(data):
    games = day2_parse(data)
    ans = 0
    for g in games:
        reds = max(s["red"] for s in games[g] if "red" in s)
        greens = max(s["green"] for s in games[g] if "green" in s)
        blues = max(s["blue"] for s in games[g] if "blue" in s)
        ans += reds * blues * greens

    return ans


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
