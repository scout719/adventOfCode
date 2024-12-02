# -*- coding: utf-8 -*-
from math import ceil, cos, sqrt
import os
import sys
from typing import Counter

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable=wrong-import-position
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2015
DAY = 21
EXPECTED_1 = None
EXPECTED_2 = None


""" DAY 21 """

def day21_parse(data):
    hit_points = int(data[0].split(": ")[-1])
    damage = int(data[1].split(": ")[-1])
    armor = int(data[2].split(": ")[-1])
    return hit_points, damage, armor

def day21_simulate(hp, damage, armor, enemy_hp, enemy_damage, enemy_armor):
    my_turn = True
    while hp > 0 and enemy_hp > 0:
        if my_turn:
            enemy_hp -= max(1, damage - enemy_armor)
        else:
            hp -= max(1, enemy_damage - armor)
        my_turn = not my_turn
    return hp > 0

def day21_shop():
    """
    Weapons:    Cost  Damage  Armor
    Dagger        8     4       0
    Shortsword   10     5       0
    Warhammer    25     6       0
    Longsword    40     7       0
    Greataxe     74     8       0
    """
    weapons = [
        (8, 4, 0),
        (10, 5, 0),
        (25, 6, 0),
        (40, 7, 0),
        (74, 8, 0),
    ]

    """
    Armor:      Cost  Damage  Armor
    Leather      13     0       1
    Chainmail    31     0       2
    Splintmail   53     0       3
    Bandedmail   75     0       4
    Platemail   102     0       5
    """
    armor = [
        (13, 0, 1),
        (31, 0, 2),
        (53, 0, 3),
        (75, 0, 4),
        (102, 0, 5),
    ]

    """
    Rings:      Cost  Damage  Armor
    Damage +1    25     1       0
    Damage +2    50     2       0
    Damage +3   100     3       0
    Defense +1   20     0       1
    Defense +2   40     0       2
    Defense +3   80     0       3
    """
    rings = [
        (25, 1, 0),
        (50, 2, 0),
        (100, 3, 0),
        (20, 0, 1),
        (40, 0, 2),
        (80, 0, 3),
    ]

    return weapons, armor, rings

def day21_solve(data, part2):
    enemy_hp, enemy_damage, enemy_armor = day21_parse(data)
    weapons, armors, rings = day21_shop()

    # 1 weapon
    # up to 1 armor
    # up to 2 rings

    best_cost = 1e9 if not part2 else 0
    for w_idx, _ in enumerate(weapons):
        for a_idx in range(-1, len(armors)):
            for r1_idx in range(-1, len(rings)):
                for r2_idx in range(-1, len(rings)):
                    if r1_idx == r2_idx:
                        continue
                    cost = weapons[w_idx][0]
                    damage = weapons[w_idx][1]
                    armor = 0
                    if a_idx != -1:
                        cost += armors[a_idx][0]
                        armor += armors[a_idx][2]
                    if r1_idx != -1:
                        cost += rings[r1_idx][0]
                        damage += rings[r1_idx][1]
                        armor += rings[r1_idx][2]
                    if r2_idx != -1:
                        cost += rings[r2_idx][0]
                        damage += rings[r2_idx][1]
                        armor += rings[r2_idx][2]

                    if not part2:
                        if best_cost < cost:
                            continue
                    else:
                        if best_cost > cost:
                            continue

                    i_won = day21_simulate(
                        100, damage, armor, enemy_hp, enemy_damage, enemy_armor)
                    if (not part2 and i_won) or \
                       (part2 and not i_won):
                        best_cost = cost
    return best_cost

def day21_1(data):
    return day21_solve(data, False)

def day21_2(data):
    return day21_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
