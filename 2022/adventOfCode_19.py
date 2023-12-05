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

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable-next=wrong-import-position
from common.utils import day_with_validation, main  # NOQA: E402

YEAR = 2022
DAY = 19
EXPECTED_1 = None  # 33
EXPECTED_2 = None

ORE = "ore"
CLAY = "clay"
OBSIDIAN = "obsidian"
GEODE = "geode"

ORE2 = 3
CLAY2 = 2
OBSIDIAN2 = 1
GEODE2 = 0

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
        id_ = line.split("print ")[1]
        id_ = id_.split(":")[0]
        # print(id)
        id_ = int(id_)

        ore_costs = line.split("ore robot costs ")[1].split(".")[0]
        ore_parts = ore_costs.split(" and ")
        ore_materials = {}
        for part in ore_parts:
            c, t = part.split(" ")
            ore_materials[t] = int(c)

        clay_costs = line.split("clay robot costs ")[1].split(".")[0]
        clay_parts = clay_costs.split(" and ")
        clay_materials = {}
        for part in clay_parts:
            c, t = part.split(" ")
            clay_materials[t] = int(c)

        obsidiar_costs = line.split("obsidian robot costs ")[1].split(".")[0]
        obsidiar_parts = obsidiar_costs.split(" and ")
        obsidiar_materials = {}
        for part in obsidiar_parts:
            c, t = part.split(" ")
            obsidiar_materials[t] = int(c)

        geode_costs = line.split("geode robot costs ")[1].split(".")[0]
        geode_parts = geode_costs.split(" and ")
        geode_materials = {}
        for part in geode_parts:
            c, t = part.split(" ")
            geode_materials[t] = int(c)

        x.append((id_, {ORE: ore_materials, CLAY: clay_materials,
                        OBSIDIAN: obsidiar_materials, GEODE: geode_materials}))
        i += 1

    return x

def day19_can_build(mats, blue):
    for m in blue:
        if mats[m] < blue[m]:
            return False
    return True

def day19_from_t(obj):
    a = defaultdict(int)
    for (t, c) in obj:
        a[t] = c
    return a
def day19_from_m(obj):
    a = []
    for t in obj:
        a.append((t, obj[t]))
    return tuple(a)

def day19_recurse(blues, tm, t, mats, robots):
    if t == tm:
        return mats[GEODE]

    # check which robots we can produce
    res = []
    for r_type in blues:
        if day19_can_build(mats, blues[r_type]):
            mats2 = deepcopy(mats)
            for mat in blues[r_type]:
                mats2[mat] -= blues[r_type][mat]
            robots2 = deepcopy(robots)
            for r_type2 in robots2:
                mats2[r_type2] += robots2[r_type2]
            robots2[r_type] += 1
            res.append(mats[GEODE] + day19_recurse(blues,
                                                   tm, t + 1, mats2, robots2))
    mats2 = deepcopy(mats)
    robots2 = deepcopy(robots)
    for r_type2 in robots2:
        mats2[r_type2] += robots2[r_type2]
    res.append(mats[GEODE] + day19_recurse(blues, tm, t + 1, mats2, robots2))

    return max(res)

# def day19_cost_aux(mats,curr, robot):
#     if mats[curr] > 0:
#         cost += max(0,robot[curr]-mats[curr])
#     else:
#         day19_cost_aux(mats, )

#             for mat2 in blues[mat]:
#                 if mats[mat2] > 0:
#                     cost += max(0,blues[mat][mat2]-mats[mat2])
#                 else:

def day19_cost(blue, mats, robots, t, tm):
    #
    # return t
    return (-robots[GEODE], -robots[OBSIDIAN], -robots[CLAY], -robots[ORE])
    return (
        max(0, mats[ORE] - blue[GEODE][ORE]) +
        max(0, mats[OBSIDIAN] - blue[GEODE][OBSIDIAN]),
        max(0, mats[ORE] - blue[OBSIDIAN][ORE]) +
        max(0, mats[CLAY] - blue[OBSIDIAN][CLAY]),
        max(0, mats[ORE] - blue[CLAY][ORE]),
        # max(0,mats[ORE] - blue[GEODE][ORE]) + max(0,mats[OBSIDIAN] - blue[GEODE][OBSIDIAN]),
    )
    if robots[CLAY] == 0:
        return max(blue[CLAY][ORE] - mats[ORE], 0)
    elif robots[OBSIDIAN] == 0:
        return max(max(blue[OBSIDIAN][ORE] - mats[ORE], blue[OBSIDIAN][CLAY]), 0)
    else:
        return max(max(blue[GEODE][ORE] - mats[ORE], blue[GEODE][OBSIDIAN] - mats[OBSIDIAN]), 0)
    return (max(blue[GEODE][ORE] // robots[ORE], blue[GEODE][OBSIDIAN] // robots[OBSIDIAN] if robots[OBSIDIAN] > 0 else int(1e9)), max(blue[OBSIDIAN][ORE] // robots[ORE], blue[OBSIDIAN][CLAY] // robots[CLAY] if robots[CLAY] > 0 else int(1e9)), blue[CLAY][ORE] // robots[ORE])
    return (mats[GEODE], mats[OBSIDIAN], mats[CLAY], mats[ORE])
    return (blue[GEODE][ORE] - mats[ORE] + blue[GEODE][OBSIDIAN] - mats[OBSIDIAN]), blue[OBSIDIAN][ORE] - mats[ORE] + blue[OBSIDIAN][CLAY] - mats[CLAY], blue[CLAY][ORE] - mats[ORE], t, day19_from_m(mats)
    # return (-robots[GEODE] * (tm - t), -robots[OBSIDIAN] * (tm - t), -robots[CLAY] * (tm - t), -robots[ORE] * (tm - t))
    return (max(blue[GEODE][ORE] - mats[ORE], blue[GEODE][OBSIDIAN] - mats[OBSIDIAN]), -1 if day19_can_build(mats, blue[GEODE]) else 0, max(blue[OBSIDIAN][ORE] - mats[ORE], blue[OBSIDIAN][CLAY] - mats[CLAY]), -1 if day19_can_build(mats, blue[OBSIDIAN]) else 0, blue[CLAY][ORE] - mats[ORE], -1 if day19_can_build(mats, blue[CLAY]) else 0, -robots[ORE], t, day19_from_m(mats))
    return (-robots[GEODE], max(blue[GEODE][ORE] - mats[ORE], blue[GEODE][OBSIDIAN] - mats[OBSIDIAN]), -robots[OBSIDIAN], max(blue[OBSIDIAN][ORE] - mats[ORE], blue[OBSIDIAN][CLAY] - mats[CLAY]), -robots[CLAY], blue[CLAY][ORE] - mats[ORE], -robots[ORE], day19_from_m(mats))
    # return (-robots[GEODE], t, -robots[OBSIDIAN], t, -robots[CLAY], t, -robots[ORE], t,  day19_from_m(mats))
    return (-robots[GEODE], -1 if day19_can_build(mats, blue[GEODE]) else 0, -robots[OBSIDIAN], -1 if day19_can_build(mats, blue[OBSIDIAN]) else 0, -robots[CLAY], -1 if day19_can_build(mats, blue[CLAY]) else 0, -robots[ORE], t, day19_from_m(mats))
    return (-mats[GEODE], -1 if day19_can_build(mats, blue[GEODE]) else 0, -robots[GEODE], -mats[OBSIDIAN], -1 if day19_can_build(mats, blue[OBSIDIAN]) else 0, -robots[OBSIDIAN], -mats[CLAY], -1 if day19_can_build(mats, blue[CLAY]) else 0, -robots[CLAY], -mats[ORE], t, mats)
    # with these robots, how long to each type
    t_to_geode = blue[GEODE][OBSIDIAN] // robots[OBSIDIAN] if robots[OBSIDIAN] > 0 else 1e9
    t_to_geode = max(t_to_geode, blue[GEODE][ORE] // robots[ORE])

    t_to_obsidian = blue[OBSIDIAN][CLAY] // robots[CLAY] if robots[CLAY] > 0 else 1e9
    t_to_obsidian = max(t_to_obsidian, blue[OBSIDIAN][ORE] // robots[ORE])

    t_to_clay = blue[CLAY][ORE] // robots[ORE]

    c = (t_to_geode, t_to_obsidian, t_to_clay, t)
    # print (c)
    return c
    if robots[OBSIDIAN] > 0:
        t_to_obsidian = blue[GEODE][OBSIDIAN] // robots[OBSIDIAN] if robots[OBSIDIAN] > 0 else 1e9
    t_to_obsidian = blue[GEODE][OBSIDIAN] // robots[OBSIDIAN] if robots[OBSIDIAN] > 0 else 1e9

    # how long until making an geode cracker?
    # need ore and obsidian
    # need_ore = ore_geode
    # need_obs = obs_geode
    # need_clay = 0
    # if no obsidian_robots:
    # need_ore += ore_obs*obs_geode
    # need_clay = obs_geode*clay_obs
    # if no clay:
    # need_ore += ore_clay*clay_obs*obs_geode
    #max(max(0,mats[ORE]-need_ore) // ore_robots, need_obs // obs_robots, need_clay // clay_robots)
    need_ore = blue[GEODE][ORE]
    need_obs = blue[GEODE][OBSIDIAN]
    need_clay = 0
    # if robots[OBSIDIAN] == 0:
    need_ore += blue[OBSIDIAN][ORE] * blue[GEODE][OBSIDIAN]
    need_clay += blue[OBSIDIAN][CLAY] * blue[GEODE][OBSIDIAN]
    # if robots[CLAY] == 0:
    need_ore += blue[CLAY][ORE] * blue[OBSIDIAN][CLAY] * blue[GEODE][OBSIDIAN]
    left_ore = max(mats[ORE] - need_ore,
                   0) // robots[ORE] if robots[ORE] > 0 else 1e9
    left_clay = max(mats[CLAY] - need_clay,
                    0) // robots[CLAY] if robots[CLAY] > 0 else 1e9
    left_obsidian = max(mats[OBSIDIAN] - need_obs,
                        0) // robots[OBSIDIAN] if robots[OBSIDIAN] > 0 else 1e9
    # print(need_obs, need_clay, need_ore)
    # print(left_obsidian, left_clay, left_ore, mats, robots)
    return (left_obsidian, left_clay, left_ore)

    #
    # A = max((ore-mats[ORE]),0)//ore_robots
    # if has obsidian
    # B = max(obsidian-mats[OBS]),0)//obsidian_robots
    # return max(A,B)
    # if no robot for obsidian
    # obsidian*mats[ORE]
    # need ore and clay
    # C = (ore-mats[ORE])//ore_robots
    # if has clay:
    # D = max(clay-mats[CLAY]),0)//clay_robots
    # return max(A+obsidian*C, obsidian*D)
    # if no clay robot
    # need ore
    # how long =  mats[ORE]
    # cost = 0
    # for mat in blue[GEODE]:
    #     if mats[mat] > 0:
    #         cost += max(0,blue[GEODE][mat]-mats[mat])
    #     else:
    #         for mat2 in blue[mat]:
    #             if mats[mat2] > 0:
    #                 cost += max(0,blue[mat][mat2]-mats[mat2])
    #             else:

    # for r_type in blue:

def day19_compute(blues, tm):
    # geodes, total ore, ore robots, total clay, clay robot, obsidian, obsidian robots, geode robots, t
    r_s = defaultdict(int)
    r_s["ore"] = 1
    q = [(tuple(), 0, tuple(), day19_from_m(r_s), [])]
    best = defaultdict(int)
    visited_GEODE = defaultdict(int)
    visited_OBSIDIAN = defaultdict(int)
    visited_CLAY = defaultdict(int)
    visited_ORE = defaultdict(int)
    visited2 = {}
    seen = set()
    best = defaultdict(int)
    ans = 0
    while q:
        c, t, mats_, robots_, path = heappop(q)
        mats = day19_from_t(mats_)
        robots = day19_from_t(robots_)
        # print(c, mats_, robots_)
        best[t] = max(best[t], mats["geode"])
        if t == tm and robots[GEODE] > 0:
            ans = max(ans, mats[GEODE])
            print(c)
            print("\n".join([str(p) for p in path]))
            assert False, tuple([mats[GEODE], robots_, mats_])
            return mats[GEODE]
            continue

        if robots[OBSIDIAN] > blues[GEODE][OBSIDIAN]:
            continue
        if robots[CLAY] > blues[OBSIDIAN][CLAY]:
            continue
        if robots[ORE] > blues[GEODE][ORE] + blues[OBSIDIAN][ORE] + blues[CLAY][ORE] + blues[ORE][ORE]:
            continue
        k = (t, tuple(sorted(mats_)), tuple(sorted(robots_)))
        if k in seen:
            # print("HIIT")
            continue
        seen.add(k)
        # if visited_GEODE[robots[GEODE]] < t:
        #     continue
        # elif visited_GEODE[robots[GEODE]] == t:

        # k = (robots[GEODE], 1 if day19_can_build(mats, blues[GEODE]) else 0, robots[OBSIDIAN], 1 if day19_can_build(mats, blues[OBSIDIAN]) else 0, robots[CLAY], 1 if day19_can_build(mats, blues[CLAY]) else 0, robots[ORE])#, mats[GEODE], mats[OBSIDIAN], mats[CLAY], mats[ORE])
        # if t in visited and visited[t] > k:
        #     print(t, k, visited[t])
        #     continue
        # print(t, k)
        # visited[t] = k

        # if best[t] > mats["geode"]:
        #     continue
        # k2 = (mats[GEODE], mats[OBSIDIAN], mats[CLAY], mats[ORE])
        # if t in visited2 and visited2[t] > k2:
        #     print(q)
        #     continue
        # visited2[t] = k2
        # print(t, len(q))

        for m in blues:
            # print(mats_, blues[m])
            if day19_can_build(mats, blues[m]):
                n_m = deepcopy(mats)
                for r in robots:
                    n_m[r] += robots[r]
                for m2 in blues[m]:
                    # print(m2, m, n_m, blues[m][m2])
                    n_m[m2] -= blues[m][m2]
                n_r = deepcopy(robots)
                n_r[m] += 1
                n_c = (t, -mats["geode"])
                n_c = day19_cost(blues, n_m, n_r, t + 1, tm)
                # if t + 1 == 9:
                # print(n_c)
                heappush(q, (n_c, t + 1, day19_from_m(n_m),
                             day19_from_m(n_r), path + [n_c]))
                # break

        n_m = deepcopy(mats)
        for r in robots:
            n_m[r] += robots[r]
        n_r = deepcopy(robots)
        n_c = (t, -mats["geode"])
        n_c = day19_cost(blues, n_m, n_r, t + 1, tm)
        # if t + 1 == 9:
        #     print(n_c)
        heappush(q, (n_c, t + 1, day19_from_m(n_m),
                     day19_from_m(n_r), path + [n_c]))
    return best[tm]

def day19_missing(blue, mats, robots):
    return max(0, blue[GEODE][OBSIDIAN] - robots[OBSIDIAN2])

    # how many t until GEODE
    if robots[OBSIDIAN2] > 0:
        return max(
            max(0, (blue[GEODE][ORE] - mats[ORE2]) // robots[ORE2]),
            max(0, (blue[GEODE][OBSIDIAN] - mats[OBSIDIAN2]) //
                robots[OBSIDIAN2]),
        )
    elif robots[CLAY2] > 0:
        # how many to a obsidian
        return max(
            max(0, (blue[OBSIDIAN][ORE] * blue[GEODE]
                    [OBSIDIAN] - mats[ORE2]) // robots[ORE2]),
            max(0, (blue[OBSIDIAN][CLAY] * blue[GEODE][OBSIDIAN] - mats[CLAY2]) // robots[CLAY2]))
    else:
        # how many to a clay
        return max(0, (blue[CLAY][ORE] * blue[OBSIDIAN][CLAY] * blue[GEODE][OBSIDIAN] - mats[ORE2]) // robots[ORE2])

        # blue[GEODE][OBSIDIAN]*blue[OBSIDIAN][ORE]
        # return max(max(0, (blue[GEODE][ORE] - mats[ORE])//robots[ORE]), max(0, blue[GEODE][OBSIDIAN] - mats[OBSIDIAN])//robots[OBSIDIAN])
    return (
        max(0, mats[ORE] - blue[GEODE][ORE]) +
        max(0, mats[OBSIDIAN] - blue[GEODE][OBSIDIAN]),
        max(0, mats[ORE] - blue[OBSIDIAN][ORE]) +
        max(0, mats[CLAY] - blue[OBSIDIAN][CLAY]),
        max(0, mats[ORE] - blue[CLAY][ORE]),
        max(0, mats[ORE], blue[ORE][ORE])
        # max(0,mats[ORE] - blue[GEODE][ORE]) + max(0,mats[OBSIDIAN] - blue[GEODE][OBSIDIAN]),
    )
def day19_convert(m):
    if m == GEODE:
        return GEODE2
    if m == OBSIDIAN:
        return OBSIDIAN2
    if m == CLAY:
        return CLAY2
    if m == ORE:
        return ORE2

def day19_can_build2(blue, mats):
    for m in blue:
        if mats[day19_convert(m)] < blue[m]:
            return False
    return True

def day19_solve2(blue, tm):
    # t, mats, robots
    q = [(0, 0, [0, 0, 0, 0],
          [0, 0, 0, 1])]
    ans = 0
    seen = set()
    best = defaultdict(lambda: 1e9)
    while q:
        _, t, mats, robots = heappop(q)

        if t == tm:
            ans = max(ans, mats[GEODE2])
            continue
        k = day19_missing(blue, mats, robots)
        if robots[OBSIDIAN2] > blue[GEODE][OBSIDIAN]:
            continue
        if robots[CLAY2] > blue[OBSIDIAN][CLAY]:
            continue
        if robots[ORE2] > blue[GEODE][ORE] + blue[OBSIDIAN][ORE] + blue[CLAY][ORE] + blue[ORE][ORE]:
            continue
        k = (t, tuple(mats), tuple(robots))
        if k in seen:
            continue
        seen.add(k)

        # print(t, mats, robots, k)

        # if k > best[t]:
        #     print(k, t)
        #     continue
        # # if k != 0:
        # best[t] = k

        for m in [GEODE, OBSIDIAN, CLAY, ORE]:
            if day19_can_build2(blue[m], mats):
                new_mats = deepcopy(mats)
                for m2 in blue[m]:
                    new_mats[day19_convert(m2)] -= blue[m][m2]
                new_robots = deepcopy(robots)
                for m2 in [GEODE2, OBSIDIAN2, CLAY2, ORE2]:
                    new_mats[m2] += robots[m2]
                new_robots[day19_convert(m)] += 1
                heappush(q, (day19_missing(blue, new_mats, new_robots),
                             t + 1, new_mats, new_robots))
                # break
        # if not day19_can_build2(blue[GEODE], mats):
        new_mats = deepcopy(mats)
        new_robots = deepcopy(robots)
        for m2 in [GEODE2, OBSIDIAN2, CLAY2, ORE2]:
            new_mats[m2] += robots[m2]
        heappush(q, (day19_missing(blue, new_mats, new_robots),
                     t + 1, new_mats, new_robots))
    return ans

def f(t_left, robots, mats, blues, DP, best):
    if t_left == 0:
        return mats[GEODE]

    k = (t_left, tuple(robots[m] for m in [GEODE, OBSIDIAN, CLAY, ORE]), tuple(
        mats[m] for m in [GEODE, OBSIDIAN, CLAY, ORE]))
    if k in DP:
        # print("yeah")
        return DP[k]

    # k2 = (k[1], k[2])
    # if k2 in best and best[k2] > t_left:
    #     return 0
    # best[k2] = t_left

    ans = 0

    # if robots[OBSIDIAN] >= blues[GEODE][OBSIDIAN] and robots[ORE] >= blues[GEODE][ORE]:
    #     print("HEY")
    #     new_robots = deepcopy(robots)
    #     new_mats = deepcopy(mats)
    #     for m in blues[GEODE]:
    #         new_mats[m] -= blues[GEODE][m]
    #     for m in robots:
    #         new_mats[m] += robots[m]
    #     new_robots[GEODE] +=1
    #     ans = f(t_left -1, new_robots, new_mats,blues, DP, best)

    #     DP[k] = ans
    #     return ans

    if day19_can_build(mats, blues[GEODE]):
        new_robots = deepcopy(robots)
        new_mats = deepcopy(mats)
        for m in blues[GEODE]:
            new_mats[m] -= blues[GEODE][m]
        for m in robots:
            new_mats[m] += robots[m]
        new_robots[GEODE] += 1
        ans = f(t_left - 1, new_robots, new_mats, blues, DP, best)

        DP[k] = ans
        return ans

    new_robots = deepcopy(robots)
    new_mats = deepcopy(mats)
    for m in robots:
        new_mats[m] += robots[m]
    ans = f(t_left - 1, new_robots, new_mats, blues, DP, best)

    if day19_can_build(mats, blues[OBSIDIAN]):
        if robots[OBSIDIAN] < blues[GEODE][OBSIDIAN]:
            new_robots = deepcopy(robots)
            new_mats = deepcopy(mats)
            for m in blues[OBSIDIAN]:
                new_mats[m] -= blues[OBSIDIAN][m]
            for m in robots:
                new_mats[m] += robots[m]
            new_robots[OBSIDIAN] += 1
            ans = max(ans, f(t_left - 1, new_robots,
                             new_mats, blues, DP, best))

    if day19_can_build(mats, blues[CLAY]):
        if robots[OBSIDIAN] < blues[GEODE][OBSIDIAN] and robots[CLAY] < blues[OBSIDIAN][CLAY]:
            new_robots = deepcopy(robots)
            new_mats = deepcopy(mats)
            for m in blues[CLAY]:
                new_mats[m] -= blues[CLAY][m]
            for m in robots:
                new_mats[m] += robots[m]
            new_robots[CLAY] += 1
            ans = max(ans, f(t_left - 1, new_robots,
                             new_mats, blues, DP, best))

    if day19_can_build(mats, blues[ORE]):
        if robots[ORE] < max(blues[GEODE][ORE], blues[OBSIDIAN][ORE], blues[CLAY][ORE], blues[ORE][ORE]):
            new_robots = deepcopy(robots)
            new_mats = deepcopy(mats)
            for m in blues[ORE]:
                new_mats[m] -= blues[ORE][m]
            for m in robots:
                new_mats[m] += robots[m]
            new_robots[ORE] += 1
            ans = max(ans, f(t_left - 1, new_robots,
                             new_mats, blues, DP, best))

    DP[k] = ans
    return ans

def f3(t_left, robots, mats, blues, DP, best):
    if t_left == 0 or (robots[OBSIDIAN] >= blues[GEODE][OBSIDIAN] and robots[ORE] >= blues[GEODE][ORE]):
        return (t_left, mats[GEODE])

    k = (t_left, tuple(robots[m] for m in [GEODE, OBSIDIAN, CLAY, ORE]), tuple(
        mats[m] for m in [GEODE, OBSIDIAN, CLAY, ORE]))
    if k in DP:
        return DP[k]

    # k2 = (k[1], k[2])
    # if k2 in best and best[k2] > t_left:
    #     return 0
    # best[k2] = t_left

    ans = (0, 0)

    if robots[OBSIDIAN] >= blues[GEODE][OBSIDIAN] and robots[ORE] >= blues[GEODE][ORE]:
        new_robots = deepcopy(robots)
        new_mats = deepcopy(mats)
        for m in blues[GEODE]:
            new_mats[m] -= blues[GEODE][m]
        for m in robots:
            new_mats[m] += robots[m]
        new_robots[GEODE] += 1
        ans = f3(t_left - 1, new_robots, new_mats, blues, DP, best)

        DP[k] = ans
        return ans

    new_robots = deepcopy(robots)
    new_mats = deepcopy(mats)
    for m in robots:
        new_mats[m] += robots[m]
    ans = f3(t_left - 1, new_robots, new_mats, blues, DP, best)

    if day19_can_build(mats, blues[GEODE]):
        new_robots = deepcopy(robots)
        new_mats = deepcopy(mats)
        for m in blues[GEODE]:
            new_mats[m] -= blues[GEODE][m]
        for m in robots:
            new_mats[m] += robots[m]
        new_robots[GEODE] += 1
        t2, g = f3(t_left - 1, new_robots, new_mats, blues, DP, best)
        if t2 > ans[0]:
            ans = (t2, g)
        elif t2 == ans[0] and g > ans[0]:
            ans = (t2, g)
        DP[k] = ans
        return ans

    if day19_can_build(mats, blues[OBSIDIAN]):
        if robots[OBSIDIAN] < blues[GEODE][OBSIDIAN]:
            new_robots = deepcopy(robots)
            new_mats = deepcopy(mats)
            for m in blues[OBSIDIAN]:
                new_mats[m] -= blues[OBSIDIAN][m]
            for m in robots:
                new_mats[m] += robots[m]
            new_robots[OBSIDIAN] += 1
            t2, g = f3(t_left - 1, new_robots, new_mats, blues, DP, best)
            if t2 > ans[0]:
                ans = (t2, g)
            elif t2 == ans[0] and g > ans[0]:
                ans = (t2, g)

    if day19_can_build(mats, blues[CLAY]):
        if robots[OBSIDIAN] < blues[GEODE][OBSIDIAN] and robots[CLAY] < blues[OBSIDIAN][CLAY]:
            new_robots = deepcopy(robots)
            new_mats = deepcopy(mats)
            for m in blues[CLAY]:
                new_mats[m] -= blues[CLAY][m]
            for m in robots:
                new_mats[m] += robots[m]
            new_robots[CLAY] += 1
            t2, g = f3(t_left - 1, new_robots, new_mats, blues, DP, best)
            if t2 > ans[0]:
                ans = (t2, g)
            elif t2 == ans[0] and g > ans[0]:
                ans = (t2, g)

    if day19_can_build(mats, blues[ORE]):
        if robots[ORE] < max(blues[GEODE][ORE], blues[OBSIDIAN][ORE], blues[CLAY][ORE], blues[ORE][ORE]):
            new_robots = deepcopy(robots)
            new_mats = deepcopy(mats)
            for m in blues[ORE]:
                new_mats[m] -= blues[ORE][m]
            for m in robots:
                new_mats[m] += robots[m]
            new_robots[ORE] += 1
            t2, g = f3(t_left - 1, new_robots, new_mats, blues, DP, best)
            if t2 > ans[0]:
                ans = (t2, g)
            elif t2 == ans[0] and g > ans[0]:
                ans = (t2, g)

    DP[k] = ans
    return ans
def f2(t_left, robots, mats, blues, DP, best):
    q = [((0, 0, 0, 0), t_left, robots, mats)]
    ans = 0
    seen = set()
    while q:
        c, t, r, ma = heappop(q)

        if t == 0:
            ans = max(ans, ma[GEODE])
            return ans

        # k = (t, r,ma)
        k = (tuple(r[m] for m in [GEODE, OBSIDIAN, CLAY, ORE]),
             tuple(ma[m] for m in [GEODE, OBSIDIAN, CLAY, ORE]))

        if k in seen:
            continue
        seen.add(k)

        if day19_can_build(ma, blues[GEODE]):
            new_robots = deepcopy(r)
            new_mats = deepcopy(ma)
            for m in blues[GEODE]:
                new_mats[m] -= blues[GEODE][m]
            for m in r:
                new_mats[m] += r[m]
            new_robots[GEODE] += 1
            c = day19_cost(blues, new_mats, new_robots, t_left, 24)
            heappush(q, (c, t_left - 1, new_robots, new_mats))
            continue

        new_robots = deepcopy(r)
        new_mats = deepcopy(ma)
        for m in r:
            new_mats[m] += r[m]
        c = day19_cost(blues, new_mats, new_robots, t_left, 24)
        heappush(q, (c, t_left - 1, new_robots, new_mats))

        if day19_can_build(ma, blues[OBSIDIAN]):
            if r[OBSIDIAN] < blues[GEODE][OBSIDIAN]:
                new_robots = deepcopy(r)
                new_mats = deepcopy(ma)
                for m in blues[OBSIDIAN]:
                    new_mats[m] -= blues[OBSIDIAN][m]
                for m in r:
                    new_mats[m] += r[m]
                new_robots[OBSIDIAN] += 1
                c = day19_cost(blues, new_mats, new_robots, t_left, 24)
                heappush(q, (c, t_left - 1, new_robots, new_mats))

        if day19_can_build(ma, blues[CLAY]):
            if r[OBSIDIAN] < blues[GEODE][OBSIDIAN] and r[CLAY] < blues[OBSIDIAN][CLAY]:
                new_robots = deepcopy(r)
                new_mats = deepcopy(ma)
                for m in blues[CLAY]:
                    new_mats[m] -= blues[CLAY][m]
                for m in r:
                    new_mats[m] += r[m]
                new_robots[CLAY] += 1
                c = day19_cost(blues, new_mats, new_robots, t_left, 24)
                heappush(q, (c, t_left - 1, new_robots, new_mats))

        if day19_can_build(ma, blues[ORE]):
            if r[ORE] < max(blues[GEODE][ORE], blues[OBSIDIAN][ORE], blues[CLAY][ORE], blues[ORE][ORE]):
                new_robots = deepcopy(r)
                new_mats = deepcopy(ma)
                for m in blues[ORE]:
                    new_mats[m] -= blues[ORE][m]
                for m in r:
                    new_mats[m] += r[m]
                new_robots[ORE] += 1
                c = day19_cost(blues, new_mats, new_robots, t_left, 24)
                heappush(q, (c, t_left - 1, new_robots, new_mats))
    return ans

    if t_left == 0:
        return mats[GEODE]

    k = (t_left, tuple(robots[m] for m in [GEODE, OBSIDIAN, CLAY, ORE]), tuple(
        mats[m] for m in [GEODE, OBSIDIAN, CLAY, ORE]))
    if k in DP:
        return DP[k]

    # k2 = (k[1], k[2])
    # if k2 in best and best[k2] > t_left:
    #     return 0
    # best[k2] = t_left

    if r[OBSIDIAN] >= blues[GEODE][OBSIDIAN] and r[ORE] >= blues[GEODE][ORE]:
        new_robots = deepcopy(r)
        new_mats = deepcopy(m)
        for m in blues[GEODE]:
            new_mats[m] -= blues[GEODE][m]
        for m in robots:
            new_mats[m] += robots[m]
        new_robots[GEODE] += 1
        ans = f(t_left - 1, new_robots, new_mats, blues, DP, best)

        DP[k] = ans
        return ans

    new_robots = deepcopy(robots)
    new_mats = deepcopy(mats)
    for m in robots:
        new_mats[m] += robots[m]
    ans = max(ans, f(t_left - 1, new_robots, new_mats, blues, DP, best))

    if day19_can_build(mats, blues[GEODE]):
        new_robots = deepcopy(robots)
        new_mats = deepcopy(mats)
        for m in blues[GEODE]:
            new_mats[m] -= blues[GEODE][m]
        for m in robots:
            new_mats[m] += robots[m]
        new_robots[GEODE] += 1
        ans = max(ans, f(t_left - 1, new_robots, new_mats, blues, DP, best))

        DP[k] = ans
        return ans

    if day19_can_build(mats, blues[OBSIDIAN]):
        if robots[OBSIDIAN] < blues[GEODE][OBSIDIAN]:
            new_robots = deepcopy(robots)
            new_mats = deepcopy(mats)
            for m in blues[OBSIDIAN]:
                new_mats[m] -= blues[OBSIDIAN][m]
            for m in robots:
                new_mats[m] += robots[m]
            new_robots[OBSIDIAN] += 1
            ans = max(ans, f(t_left - 1, new_robots,
                             new_mats, blues, DP, best))

    if day19_can_build(mats, blues[CLAY]):
        if robots[OBSIDIAN] < blues[GEODE][OBSIDIAN] and robots[CLAY] < blues[OBSIDIAN][CLAY]:
            new_robots = deepcopy(robots)
            new_mats = deepcopy(mats)
            for m in blues[CLAY]:
                new_mats[m] -= blues[CLAY][m]
            for m in robots:
                new_mats[m] += robots[m]
            new_robots[CLAY] += 1
            ans = max(ans, f(t_left - 1, new_robots,
                             new_mats, blues, DP, best))

    if day19_can_build(mats, blues[ORE]):
        if robots[ORE] < max(blues[GEODE][ORE], blues[OBSIDIAN][ORE], blues[CLAY][ORE], blues[ORE][ORE]):
            new_robots = deepcopy(robots)
            new_mats = deepcopy(mats)
            for m in blues[ORE]:
                new_mats[m] -= blues[ORE][m]
            for m in robots:
                new_mats[m] += robots[m]
            new_robots[ORE] += 1
            ans = max(ans, f(t_left - 1, new_robots,
                             new_mats, blues, DP, best))

    DP[k] = ans
    return ans

EXPECTED_1 = 33
EXPECTED_2 = None
def day19_1(data):
    # return ""
    _x_ = day19_parse(data)
    ans = 0
    tm = 24
    ans = 0
    for i, b in _x_:
        DP = {}
        best = {}
        r_s = defaultdict(int)
        r_s["ore"] = 1
        res = f(tm, r_s, defaultdict(int), b, DP, best)
        # res = day19_compute(b, tm)
        ans += i * res

    # 851
    return ans
    # _x_ = _x_[0:1]
    _x_ = _x_[1:2]
    DP = {}
    r_s = defaultdict(int)
    r_s["ore"] = 1
    return f(tm, r_s, defaultdict(int), _x_[0][1], DP)

    # return day19_solve2(_x_[0][1], tm)

    # for i, blues in _x_:
    #     print(i)
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
    # i_robots = defaultdict(int)
    # i_robots[ORE] = 1
    # ans = 0
    # for i, blues in _x_:
    #     ans += i*day19_recurse(blues, tm, 0, defaultdict(int), i_robots)
    # return ans

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
        ans += total * i
    return ans

def day19_2(data):
    _x_ = day19_parse(data)
    _x_ = _x_[:3]
    ans = 0
    tm = 32
    ans = 1
    for i, b in _x_:
        DP = {}
        best = {}
        r_s = defaultdict(int)
        r_s["ore"] = 1
        res = f(tm, r_s, defaultdict(int), b, DP, best)
        ans *= res
    return ans


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
