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

from z3 import If, Int, Solver, Sum, Abs

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable-next=wrong-import-position
from common.utils import day_with_validation, main

YEAR = 2022
DAY = 16
EXPECTED_1 = 1651
EXPECTED_2 = None


""" DAY 16 """

def day16_parse(data):
    valves = {}
    for line in data:
        # Valve AA has flow rate=0; tunnels lead to valves DD, II, BB

        v = line.split("alve ")[1].split(" ")[0]
        f = int(line.split("rate=")[1].split(";")[0])
        if "valves" in line:
            vs = line.split("valves ")[1].split(", ")
        else:
            vs = [line.split("valve ")[1]]

        valves[v] = (f, vs)
    return valves

def day16_short(s, e, valves):
    q = [(s, [])]
    visited = set()
    while q:
        curr, path = q.pop()
        if curr == e:
            return path+[e]
        visited.add(curr
                    )
        for vs in valves[curr][1]:
            if vs in visited:
                continue
            path2 = deepcopy(path)
            path2.append(curr)
            q.append((vs, path2))
    return None

def day16_1(data):
    valves = day16_parse(data)
    q = [(0, "AA", 0, 1, [], ["AA"])]
    flow = []
    print(valves)
    vs_n = list(valves.keys())
    print(vs_n)
    visited = set()
    while q:
        _, curr, pr, t, vis, op = q.pop()
        # print(curr, pr, t, vis)

        # if op != ["AA"]:
        #     k = tuple(op)
        #     if k in visited:
        #         continue
        #     visited.add(k)

        op2 = deepcopy(op)
        if curr not in op:
            op2.append(curr)
            pr += (30 - t - 1) * valves[curr][0]
            t += 2
        else:
            t += 1

        print(len(op2))
        if len(op2) == len(vs_n):
            return pr
            flow.append((pr, vis))
            continue

        for vs in vs_n:
            if vs in op or vs == curr:
                continue
            path = day16_short(curr, vs, valves)
            # print(curr, vs, path)
            if path is not None:
                vis2 = deepcopy(vis)
                vis2.append(curr)
                op3 = deepcopy(op2)
                q.append((len(vis2), path[1], pr, t, vis2, op3))

    print(sorted(flow, reverse=True))
    return max(pr for pr, _ in flow)

def day16_2(data):
    x = day16_parse(data)
    return ""


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
