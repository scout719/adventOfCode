# -*- coding: utf-8 -*-
import functools
import math
import os
import sys
import time
from collections import Counter, defaultdict, deque
from copy import deepcopy
from heapq import heappop, heappush
from os.path import join
from typing import Callable, ChainMap, Dict, Iterator, List, Optional, Union

from z3 import Abs, If, Int, Solver, Sum

from macpath import split

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable-next=wrong-import-position
from common.utils import day_with_validation, main  # NOQA: E402

YEAR = 2022
DAY = 19
EXPECTED_1 = 33
EXPECTED_2 = None


""" DAY 19 """

def day19_parse(data):
    x = []
    i = 0
    while i < len(data):
        line = data[i]
        # Blueprint 1:
        # Each ore robot costs 4 ore.
        # Each clay robot costs 2 ore.
        # Each obsidian robot costs 3 ore and 14 clay.
        # Each geode robot costs 2 ore and 7 obsidian.
        id = line.split("print ")[1]
        id = id.split(":")[0]
        # print(id)
        id= int(id)

        ore_costs = line.split("ore robot costs ")[1].split(".")[0]
        ore_parts = ore_costs.split(" and ")
        ore_materials = {}
        for part in ore_parts:
            c,t = part.split(" ")
            ore_materials[t] = int(c)
            
        clay_costs = line.split("clay robot costs ")[1].split(".")[0]
        clay_parts = clay_costs.split(" and ")
        clay_materials = {}
        for part in clay_parts:
            c,t = part.split(" ")
            clay_materials[t] = int(c)

        obsidiar_costs = line.split("obsidian robot costs ")[1].split(".")[0]
        obsidiar_parts = obsidiar_costs.split(" and ")
        obsidiar_materials = {}
        for part in obsidiar_parts:
            c,t = part.split(" ")
            obsidiar_materials[t] = int(c)

        geode_costs = line.split("geode robot costs ")[1].split(".")[0]
        geode_parts = geode_costs.split(" and ")
        geode_materials = {}
        for part in geode_parts:
            c,t = part.split(" ")
            geode_materials[t] = int(c)

        x.append((id, {"ore":ore_materials, "clay":clay_materials, "obsidian":obsidiar_materials, "geode":geode_materials}))
        i += 1

    return x

def day19_can_build(mats, blue):
    for m in blue:
        if mats[m] < blue[m]:
            return False
    return True

def day19_from_t(obj):
    a = defaultdict(int)
    for (t,c) in obj:
       a[t] = c
    return a
def day19_from_m(obj):
    a = []
    for t in obj:
       a.append((t, obj[t]))
    return tuple(a)

def day19_compute(blues, tm):
    # geodes, total ore, ore robots, total clay, clay robot, obsidian, obsidian robots, geode robots, t
    r_s = defaultdict(int)
    r_s["ore"] = 1
    q = [(tuple(), 0, tuple(), day19_from_m(r_s))]
    while q:
        c, t, mats_, robots_ =heappop(q)
        mats = day19_from_t(mats_)
        robots = day19_from_t(robots_)
        print(c, mats_, robots_)
        if t == tm:
            return mats["geode"]
        # print(t, len(q))
        
        for m in blues:
            print(mats_, blues[m])
            if day19_can_build(mats, blues[m]):
                n_m = deepcopy(mats)
                for r in robots:
                    n_m[r] += robots[r]
                for m2 in blues[m]:
                    # print(m2, m, n_m, blues[m][m2])
                    n_m[m2] -= blues[m][m2]
                n_r = deepcopy(robots)
                n_r[m] += 1
                n_c = (-mats["geode"], -robots["geode"], -mats["obsidian"], -robots["obsidian"], -mats["clay"], -robots["clay"], -mats["ore"], -robots["ore"])
                heappush(q, (n_c, t+1,  day19_from_m(n_m), day19_from_m(n_r)))
                break
        
        n_m = deepcopy(mats)
        for r in robots:
            n_m[r] += robots[r]
        n_r = deepcopy(robots)
        n_c = (-mats["geode"], -robots["geode"], -mats["obsidian"], -robots["obsidian"], -mats["clay"], -robots["clay"], -mats["ore"], -robots["ore"])
        heappush(q, (n_c, t+1, day19_from_m(n_m), day19_from_m(n_r)))

def day19_1(data):
    _x_ = day19_parse(data)
    ans = 0
    tm = 24
    
    # for i, blues in _x_:
    #     mats = defaultdict(int)
    #     robots = defaultdict(int)
    #     robots["ore"] = 1
    #     print(blues)
    #     for t in range(tm):
    #         print(t, mats, robots)
    #         mats["geode"] += robots["geode"]
    #         n_r = set()
    #         built = False
    #         if day19_can_build(mats, blues["geode"]):
    #             for m2 in blues["geode"]:
    #                 if mats[m2] < blues["geode"][m2]:
    #                     mats[m2]-= blues["geode"][m2]
    #             n_r.add("geode")
    #             built = True
                
    #         if not built and day19_can_build(mats, blues["obsidian"]):
    #             for m2 in blues["obsidian"]:
    #                 if mats[m2] >= blues["obsidian"][m2]:
    #                     mats[m2]-= blues["obsidian"][m2]
    #             n_r.add("obsidian")
    #             built = True
    #         if not built and day19_can_build(mats, blues["clay"]):
    #             for m2 in blues["clay"]:
    #                 mats[m2]-= blues["clay"][m2]
    #             n_r.add("clay")
    #             built = True
    #         if not built and day19_can_build(mats, blues["ore"]):
    #             for m2 in blues["ore"]:
    #                 if mats[m2] >= blues["ore"][m2]:
    #                     mats[m2]-= blues["ore"][m2]
    #             n_r.add("ore")
    #             built = True
    #         for m in robots:
    #             mats[m] += robots[m]
    #         for m in n_r:
    #             robots[m] += 1
    #     ans += mats["geode"]*i
    # return ans
            
                


    for i, blues in _x_:
        print(i)
        total = day19_compute(blues, tm)
        ans += total*i
    return ans

    return _x_

def day19_2(data):
    _x_ = day19_parse(data)
    return ""


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
