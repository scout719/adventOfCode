# -*- coding: utf-8 -*-
import functools
import math
import os
import sys
import time
from collections import Counter, defaultdict, deque
from copy import deepcopy
from heapq import heappop, heappush, heapify
from os.path import join
from typing import Callable, ChainMap, Dict, Iterator, List, Optional, Union

from z3 import If, Int, Solver, Sum, Abs

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable-next=wrong-import-position
from common.utils import day_with_validation, main  # NOQA: E402

YEAR = 2022
DAY = 16
EXPECTED_1 = 1651
EXPECTED_2 = 1707


""" DAY 16 """

def day16_parse(data):
    valves = {}
    for line in data:
        # Valve AA has flow rate=0; tunnels lead to valves DD, II, BB

        v = line.split("alve ")[1].split(" ")[0]
        r = int(line.split("rate=")[1].split(";")[0])
        if "valves" in line:
            vs = line.split("valves ")[1].split(", ")
        else:
            vs = [line.split("valve ")[1]]

        valves[v] = (r, vs)
    return valves

def day16_time_to_valve(s, e, valves):
    q = [(0, s)]
    visited = set()
    while q:
        t, curr = heappop(q)
        if curr == e:
            return t
        visited.add(curr)
        for vs in valves[curr][1]:
            if vs in visited:
                continue
            q.append((t + 1, vs))
    return None

def day16_get_cost(t, open_, valves, max_t):
    c = 0
    vs_n = list(valves.keys())
    for vs in vs_n:
        if vs not in open_:
            c += (max_t - (t)) * valves[vs][0]
    return c

def day16_1(data):
    valves = day16_parse(data)
    # cost, pressure, t, curr_valve, open
    max_t = 30
    q = [(day16_get_cost(0, [], valves, max_t), 0, 0, "AA", [])]

    vs_n = [vs for vs in valves.keys() if valves[vs][0] > 0]
    DP = {}
    while q:
        cost, pr, t, curr, open_ = heappop(q)
        if t == 30 or len(open_) == len(vs_n):
            return pr
        for vs in vs_n:
            if vs in open_:
                continue
            if (curr, vs) in DP:
                time_to_valve = DP[(curr, vs)]
            else:
                time_to_valve = day16_time_to_valve(curr, vs, valves)
                DP[(curr, vs)] = time_to_valve
            if time_to_valve is not None:
                open2 = open_ + [vs]
                t2 = t + time_to_valve + 1
                if t2 > 30:
                    t2 = 30
                pr2 = pr + (30 - t2) * valves[vs][0]
                heappush(q, (-pr2 - day16_get_cost(t2, open2, valves,
                         max_t), pr2, t2, vs, open2))
    # 856
    # 2102
    assert False

def day16_time_to_valve2(s, e, valves):
    q = [(0, s, [])]
    visited = set()
    while q:
        t, curr, path = heappop(q)
        if curr == e:
            return t, path
        if curr in visited:
            continue
        visited.add(curr)
        for vs in valves[curr][1]:
            # if vs in visited:
                # continue
            q.append((t + 1, vs, path + [vs]))
    return None, []

def day16_get_release(open_, valves):
    ps = 0
    for vs in open_:
        ps += valves[vs][0]
    return ps

def day16_2(data):
    valves = day16_parse(data)
    # cost, pressure, t, curr_valve, open
    max_t = 26
    q = [(day16_get_cost(1, [], valves, max_t), 0, 0, ("AA", [], "AA", []), set())]

    vs_n = [vs for vs in valves.keys() if valves[vs][0] > 0]
    DP = {}
    t_ = 0
    while q:
        _, pr, t, (curr, path, curr_e, path_e), open_ = heappop(q)

        if t == max_t:# or len(open_) == len(vs_n):
            # 2170
            return pr
        
        # 🔨
        if len(q) > 200000:
            new_q = sorted(q)[:170000]
            heapify(new_q)
            q = new_q
        
        pr += day16_get_release(open_, valves)
        next_me = []
        next_e = []
        if path:
            if len(path) == 1:
                assert path[0] == curr, (path[0], curr)
                open2 = set(list(open_) + [path[0]])
                curr2 = curr
            else:
                open2 = set(open_)
                curr2 = path[1]
            path2 = path[1:]
            next_me = [(curr2, path2, open2)]
            # print(next_me, curr, path, open2, open_, open2.difference(open_))
        else:
            for vs in vs_n:
                if vs in open_:
                    continue
                if path_e and vs == path_e[-1]:
                    continue
                if (curr, vs) in DP:
                    time_to_valve, path2 = DP[(curr, vs)]
                else:
                    time_to_valve, path2 = day16_time_to_valve2(
                        curr, vs, valves)
                    DP[(curr, vs)] = (time_to_valve, path2)
                if time_to_valve is not None:
                    next_me.append((path2[0], path2, open_))
            if not next_me:
                # assert len(open_) == len(vs_n)
                next_me.append((curr, path, open_))
        if path_e:
            if len(path_e) == 1:
                assert path_e[0] == curr_e
                open_e2 = set(list(open_) + [path_e[0]])
                curr_e2 = curr_e
            else:
                open_e2 = set(open_)
                curr_e2 = path_e[1]
            path_e2 = path_e[1:]
            next_e = [(curr_e2, path_e2, open_e2)]
        else:
            for vs in vs_n:
                if vs in open_:
                    continue
                if path and vs == path[-1]:
                    continue
                if (curr_e, vs) in DP:
                    # print(curr_e, vs, DP[(curr_e, vs)])
                    time_to_valve_e, path_e2 = DP[(curr_e, vs)]
                else:
                    time_to_valve_e, path_e2 = day16_time_to_valve2(
                        curr_e, vs, valves)
                    DP[(curr_e, vs)] = (time_to_valve_e, path_e2)
                if time_to_valve_e is not None:
                    next_e.append((path_e2[0], path_e2, open_))
            if not next_e:
                # assert len(open_) == len(vs_n)
                next_e.append((curr_e, path_e, open_))

        for curr2, path2, open2 in next_me:
            for curr_e2, path_e2, open_e2 in next_e:
                if path2 and path_e2 and path_e2[-1] == path2[-1]:
                    continue
                n_open = open2.union(open_e2)
                pr2 = -pr
                for vs in n_open:
                    pr2 -= (max_t-(t+1))*valves[vs][0]
                heappush(q, (pr2 - day16_get_cost(t+2, n_open, valves, max_t),
                        pr, t + 1, (curr2, path2, curr_e2, path_e2), n_open))

    assert False


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
