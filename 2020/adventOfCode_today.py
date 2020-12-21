# -*- coding: utf-8 -*-
# pylint: disable=import-error
# pylint: disable=unused-import
# pylint: disable=wildcard-import
# pylint: disable=wrong-import-position
# pylint: disable=consider-using-enumerate
import functools
import math
import os
import sys
import time
from copy import deepcopy
from collections import defaultdict
from heapq import heappop, heappush

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
print(FILE_DIR)
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
sys.path.insert(0, FILE_DIR + "/../../")
import computer  # NOQA: E402
from common.utils import read_input, main, clear  # NOQA: E402
# pylint: enable=import-error
# pylint: enable=wrong-import-position
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


WHITE_SQUARE = "█"
WHITE_CIRCLE = "•"
BLUE_CIRCLE = f"{bcolors.OKBLUE}{bcolors.BOLD}•{bcolors.ENDC}"
RED_SMALL_SQUARE = f"{bcolors.FAIL}{bcolors.BOLD}■{bcolors.ENDC}"

""" DAY 21 """

def day21_parse(data):
    foods = []
    for line in data:
        # trh fvjkl sbzzf mxmxvkd (contains dairy)
        parts = line.split(" (contains ")
        foods.append((parts[0].split(" "), parts[1][:-1].split(", ")))
    return foods

from collections import defaultdict
from copy import deepcopy
def day21_1(data):
    data = read_input(2020, 2101)
    foods = day21_parse(data)
    table_a = defaultdict(set)
    table_i = defaultdict(set)
    print(foods)
    c = defaultdict(lambda:0)
    for ing,al in foods:
        for a in al:
            print(a)
            for i in ing:
                c[i] += 1
                table_a[a].add(i)
                table_i[i].add(a)
    lone = set()
    for i in table_i:
        if len(table_i[i]) == 1:
            lone.add(i)
    # for a in table:
    #     print(len(table[a]))

    # mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
    # trh fvjkl sbzzf mxmxvkd (contains dairy)
    # sqjhc fvjkl (contains soy)
    # sqjhc mxmxvkd sbzzf (contains fish)

    
    # mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
    # trh fvjkl sbzzf mxmxvkd (contains dairy)
    # sqjhc fvjkl (contains soy)
    # sqjhc mxmxvkd sbzzf (contains fish)

    #  kfcds, nhms, sbzzf, or trh
    print(c)
    print(table_i)
    print(table_a)
    ans =0
    
    for i in table_i.keys():
        poss = set(table_i[i])
        for a in table_i[i]:
            if not day21_test(i,a, table_a, table_i):
                poss.remove(a)
        if len(a) == 0:
            ans += c[i]
            table_i.pop(i, None)
    return ans


    return table_a

def day21_test(i,a, table_a, table_i):
    table_a = deepcopy(table_a)
    table_i = deepcopy(table_i)
    table_i.pop(i, None)

    changes = True
    curr_i = i
    curr_a = [a]
    while changes:
        changes = False
        for i2 in table_i:
            for a2 in curr_a:
                if a2 in table_i[i2]:
                    table_i[i2].remove(a2)
        
        for i2 in list(table_i.keys()):
            if len(table_i[i2]) == 0:
                print(i, a)
                return False
            if len(table_i[i2]) ==1:
                curr_a.append(list(table_i[i2])[0])
                table_i.pop(i2,None)
                changes = True
    return True

def day21_2(data):
    #data = read_input(2020, 2101)
    return None


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, globals(), 2020)
