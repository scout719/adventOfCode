# -*- coding: utf-8 -*-
# pylint: disable=import-error
# pylint: disable=unused-import
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# pylint: disable=wrong-import-position
# pylint: disable=consider-using-enumerate
from typing import Callable, Dict, Iterator, Union, Optional, List, ChainMap
import functools
import math
import os
from os.path import join
import sys
import time
from copy import deepcopy
from collections import Counter, defaultdict, deque
from heapq import heappop, heappush

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import *  # NOQA: E402
# pylint: enable=import-error
# pylint: enable=wrong-import-position

YEAR = 2022
DAY = 7
EXPECTED_1 = 95437
EXPECTED_2 = 24933642


""" DAY 7 """

def day7_parse(data):
    m = defaultdict(set)
    curr = ""
    i = 0
    while i < len(data):
        line = data[i]
        if line.startswith("$ "):
            parts = line.split("$ ")[1].split(" ")
            cmd = parts[0]
            if cmd == "cd":
                n = parts[1]
                if n == "..":
                    curr = "/".join(curr.split("/")[:-2]) + "/"
                else:
                    if curr:
                        curr += n + "/"
                    else:
                        curr = n
                i += 1
            elif cmd == "ls":
                i += 1
                while i < len(data) and not (data[i].startswith("$ ")):
                    line = data[i]
                    parts = line.split(" ")
                    if parts[0] == "dir":
                        m[curr].add((parts[1], True, 0))
                    else:
                        size = int(parts[0])
                        f = parts[1]
                        m[curr].add((f, False, size))
                    i += 1

    return m

def day7_total(m, d, mem):
    if d in mem:
        return mem[d]
    t = 0
    for c, is_dir, size in m[d]:
        if is_dir:
            t += day7_total(m, d + c + "/", mem)
        else:
            t += size
    mem[d] = t
    return t

def day7_1(data):
    data = day7_parse(data)

    mem = {}
    day7_total(data, "/", mem)
    ans = 0
    q = ["/"]
    while q:
        curr = q.pop()
        if mem[curr] <= 100000:
            ans += mem[curr]
        for c, is_dir, _ in data[curr]:
            if is_dir:
                q.append(curr + c + "/")

    return ans

def day7_2(data):
    data = day7_parse(data)
    mem = {}
    day7_total(data, "/", mem)
    unused = 70000000 - mem["/"]
    target = 30000000 - unused
    t = list()
    for v in mem.values():
        if v >= target:
            t.append(v)
    return min(t)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
