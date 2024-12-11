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
DAY = 11
EXPECTED_1 = 55312
EXPECTED_2 = None

def day11_parse(data: list[str]):
    return [int(n) for n in data[0].split()]

def day11_split(stone):
    stone_s = str(stone)
    middle = len(stone_s) // 2
    return [int(stone_s[:middle]), int(stone_s[middle:])]

def day11_recurse(memory, stones, t):
    # Computes the number of stones generated by 'stones' in 't' steps
    if t == 0:
        return len(stones)

    # Apply the rules if it is a sigle stone
    if len(stones) == 1:
        stone = stones[0]
        if (stone, t) in memory:
            return memory[(stone, t)]

        ans = 0
        if stone == 0:
            ans = day11_recurse(memory, [1], t - 1)
        elif len(str(stone)) % 2 == 0:
            ans = day11_recurse(memory, day11_split(stone), t - 1)
        else:
            ans = day11_recurse(memory, [stone * 2024], t - 1)
        memory[(stone, t)] = ans
        return ans

    # Since each stone generation is independent of the neightbours
    # sum the number of stones generated by each stone in 't' steps
    return sum(day11_recurse(memory, [stone], t) for stone in stones)

def day11_solve(data, part2):
    stones = day11_parse(data)
    return day11_recurse({}, stones, 75 if part2 else 25)

def day11_1(data):
    return day11_solve(data, False)

def day11_2(data):
    return day11_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
