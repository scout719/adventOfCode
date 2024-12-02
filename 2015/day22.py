# -*- coding: utf-8 -*-
import os
import sys
from heapq import heappop, heappush

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable=wrong-import-position
from common.utils import day_with_validation  # NOQA: E402
from common.utils import main  # NOQA: E402

YEAR = 2015
DAY = 22
EXPECTED_1 = None
EXPECTED_2 = None


""" DAY 22 """

def day22_parse(data):
    hit_points = int(data[0].split(": ")[-1])
    damage = int(data[1].split(": ")[-1])
    return hit_points, damage

def day22_solve(data, part2):
    enemy_hp, enemy_damage = day22_parse(data)
    # spent_mana, my_turn, mana, hp, armor, effects, enemy_hp, enemy_damage
    q: list[tuple[int, bool, int, int, int, list[int], int, int]] = [
        (0, True, 500, 50, 0, [0, 0, 0], enemy_hp, enemy_damage)]
    # new_mana, damage, armor
    effects = [(0, 0, 7), (0, 3, 0), (101, 0, 0)]
    # cost, damage, armor, heal, effects (effect, timer)
    spells = [
        (53, 4, 0, 0, (None, 0)),
        (73, 2, 0, 2, (None, 0)),
        (113, 0, 0, 0, (0, 6)),
        (173, 0, 0, 0, (1, 6)),
        (229, 0, 0, 0, (2, 5)),
    ]
    while q:
        spent_mana, my_turn, mana, hp, armor, curr_effects, enemy_hp, enemy_damage = \
            heappop(q)
        if my_turn and part2:
            hp -= 1
        if hp <= 0:
            continue
        actual_armor = armor
        for i, timer in enumerate(curr_effects):
            extra_mana, extra_damage, extra_armor = effects[i]
            if timer > 0:
                mana += extra_mana
                actual_armor += extra_armor
                enemy_hp -= extra_damage
                curr_effects[i] -= 1

        if enemy_hp <= 0:
            return spent_mana

        if not my_turn:
            heappush(q, (spent_mana, not my_turn, mana, hp - max(1, enemy_damage -
                     actual_armor), armor, curr_effects + [], enemy_hp, enemy_damage))
        else:
            for cost, extra_damage, _, heal, (idx, timer) in spells:
                if idx is not None and curr_effects[idx] > 0:
                    continue

                if cost > mana:
                    continue

                new_effects = curr_effects + []
                if idx is not None:
                    new_effects[idx] = timer
                heappush(q, (spent_mana + cost, not my_turn, mana - cost, hp +
                         heal, armor, new_effects, enemy_hp - extra_damage, enemy_damage))

    # 628 low
    assert False

def day22_1(data):
    return day22_solve(data, False)

def day22_2(data):
    return day22_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
