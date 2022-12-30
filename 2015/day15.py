# -*- coding: utf-8 -*-
from copy import deepcopy
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable=wrong-import-position
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2015
DAY = 15
EXPECTED_1 = 62842880
EXPECTED_2 = None


""" DAY 15 """

def day15_parse(data):
    ingredients = {}
    for line in data:
        words = line.split()
        ingredient = words[0][:-1]
        capacity = int(words[2][:-1])
        durability = int(words[4][:-1])
        flavor = int(words[6][:-1])
        texture = int(words[8][:-1])
        calories = int(words[10])
        ingredients[ingredient] = (
            capacity, durability, flavor, texture, calories)
    return ingredients

def day15_perms(ingredients, total_ingredients):
    curr = ingredients[0]
    if len(ingredients) == 1:
        res = []
        for i in range(100 + 1):
            res.append({curr: i})
        return res

    perms = day15_perms(ingredients[1:], total_ingredients)
    res = []
    for perm in perms:
        remaining = 100 - sum(perm.values())
        if len(ingredients) == total_ingredients:
            new_perm = deepcopy(perm)
            new_perm[curr] = remaining
            res.append(new_perm)
        else:
            for i in range(remaining + 1):
                new_perm = deepcopy(perm)
                new_perm[curr] = i
                res.append(new_perm)
    return res

def day15_solve(data, max_calories):
    ingredients = day15_parse(data)
    perms = day15_perms(list(ingredients.keys()), len(ingredients))

    best = 0
    for perm in perms:
        total_capacity = 0
        total_durability = 0
        total_flavor = 0
        total_texture = 0
        total_calories = 0
        for ingredient, quantity in perm.items():
            capacity, durability, flavor, texture, calories = ingredients[ingredient]
            total_capacity += capacity * quantity
            total_durability += durability * quantity
            total_flavor += flavor * quantity
            total_texture += texture * quantity
            total_calories += calories * quantity
        if max_calories > 0 and total_calories != max_calories:
            continue
        totals = [total_capacity, total_durability,
                  total_flavor, total_texture]
        if any(total < 0 for total in totals):
            continue
        total_score = 1
        for total in totals:
            total_score *= total
        best = max(total_score, best)
    return best

def day15_1(data):
    return day15_solve(data, 0)

def day15_2(data):
    return day15_solve(data, 500)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
