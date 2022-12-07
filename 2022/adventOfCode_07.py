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
from common.utils import main, day_with_validation  # NOQA: E402
# pylint: enable=import-error
# pylint: enable=wrong-import-position

YEAR = 2022
DAY = 7
EXPECTED_1 = 95437
EXPECTED_2 = 24933642


""" DAY 7 """

def day7_parse(data):
    filesystem = defaultdict(set)
    cwd = ""
    curr_line = 0
    while curr_line < len(data):
        line = data[curr_line]
        assert line[0] == "$"

        # $ <cmd> <args>
        parts = line.split(" ")[1:]
        cmd = parts[0]
        if cmd == "cd":
            target = parts[1]
            if target == "..":
                cwd = "/".join(cwd.split("/")[:-2]) + "/"
            else:
                # avoid the // at the start
                cwd += (target + "/").replace("//", "/")
            curr_line += 1
        elif cmd == "ls":
            curr_line += 1
            while curr_line < len(data) and not data[curr_line].startswith("$"):
                line = data[curr_line]
                parts = line.split(" ")
                if parts[0] == "dir":
                    filesystem[cwd].add((parts[1], True, 0))
                else:
                    size = int(parts[0])
                    f = parts[1]
                    filesystem[cwd].add((f, False, size))
                curr_line += 1

    return filesystem

def day7_directory_size(filesystem, directory, DP):
    if directory in DP:
        return DP[directory]
    total_size = 0
    for child, is_dir, size in filesystem[directory]:
        if is_dir:
            total_size += day7_directory_size(filesystem,
                                              directory + child + "/", DP)
        else:
            total_size += size
    DP[directory] = total_size
    return total_size

def day7_1(data):
    filesystem = day7_parse(data)

    DP = {}
    day7_directory_size(filesystem, "/", DP)
    total = 0
    directories = ["/"]
    while directories:
        directory = directories.pop()
        if DP[directory] <= 100000:
            total += DP[directory]
        for child, is_dir, _ in filesystem[directory]:
            if is_dir:
                directories.append(directory + child + "/")

    return total

def day7_2(data):
    data = day7_parse(data)
    DP = {}
    day7_directory_size(data, "/", DP)
    unused_space = 70000000 - DP["/"]
    min_to_free = 30000000 - unused_space
    candidates = []
    for size in DP.values():
        if size >= min_to_free:
            candidates.append(size)
    return min(candidates)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
