# -*- coding: utf-8 -*-
# pylint: disable=import-error
# pylint: disable=unused-import
# pylint: disable=wildcard-import
# pylint: disable=wrong-import-position
# pylint: disable=consider-using-enumerate
import functools
import math
import os
from os.path import join
import sys
import time
from copy import deepcopy
from collections import defaultdict
from heapq import heappop, heappush

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
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

""" DAY 23 """

def day23_parse(data):
    return data

class Node:
    i = 0
    n = None
    p = None

    def __init___(self, i):
        """
        docstring
        """
        self.i = i

    def next(self, n):
        self.n = n

    def prev(self, p):
        self.p = p


def day23_round(cups, curr, min_, max_):
    # print(cups)
    curr_c = cups[curr]
    sel_cups = []
    for i in range(1, 4):
        sel_cups.append(cups[(curr + i) % len(cups)])
    cups = [x for x in cups if x not in sel_cups]

    dest_cup = curr_c - 1
    while dest_cup not in cups:
        dest_cup -= 1
        if dest_cup < min_:
            dest_cup = max_
    # print(cups, curr_c, sel_cups, dest_cup)
    new_cups = []
    for i, c in enumerate(cups):
        if c not in sel_cups:
            new_cups.append(c)
            if c == dest_cup:
                for c2 in sel_cups:
                    new_cups.append(c2)
    cups = new_cups
    for i, c in enumerate(cups):
        if c == curr_c:
            curr = (i + 1) % len(cups)
            break
    return cups, curr

def day23_round2(start: Node, s, curr, min_, max_, mem):
    after_sel = start
    selected = []
    for _ in range(4):
        after_sel = after_sel.n
        selected.append(after_sel.i)
    selected = selected[:-1]

    start_sel = start.n
    end_sel = after_sel.p

    start.next(after_sel)
    after_sel.prev(start)

    assert start.n != start
    assert after_sel.p != after_sel

    dest_cup = after_sel
    dest_cup_i = start.i - 1
    if dest_cup_i < min_:
        dest_cup_i = max_
    while dest_cup_i in selected:
        dest_cup_i -= 1
        if dest_cup_i < min_:
            dest_cup_i = max_

    dest_cup = mem[dest_cup_i]

    end_sel.next(dest_cup.n)
    dest_cup.n.prev(end_sel)

    start_sel.prev(dest_cup)
    dest_cup.next(start_sel)

    assert after_sel.p != after_sel

    return start.n


def day23_1(data):
    # data = read_input(2020, 2301)
    cups = [int(x) for x in data[0]]
    min_ = min(cups)
    max_ = max(cups)

    curr = 0
    for _ in range(100):
        cups, curr = day23_round(cups, curr, min_, max_)

    label = min_
    delta = cups.index(label)
    return "".join([str(cups[(i + delta) % len(cups)]) for i in range(len(cups))]).replace("1", "")

def day23_print(start):
    seen = set()
    l = []
    while start.i not in seen:
        seen.add(start.i)
        l.append(str(start.i))
        start = start.n
    print(", ".join(l))

def day23_2(data):
    # data = read_input(2020, 2301)
    cups = [int(x) for x in data[0]]
    rounds = 10000000
    n_cups = 1000000
    # rounds = 100
    # n_cups = 9
    min_ = min(cups)
    max_ = max(cups)
    for i in range(max_ + 1, n_cups + 1):
        cups.append(i)
    assert len(cups) == n_cups, len(cups)

    max_ = n_cups

    s = Node()
    s.i = cups[0]
    start = s
    mem = {}
    mem[cups[0]] = start
    for i in cups[1:]:
        curr = Node()
        curr.i = i
        mem[i] = curr
        s.next(curr)
        curr.prev(s)
        s = curr
    start.prev(s)
    s.next(start)

    curr = 0
    s = start
    for _ in range(rounds):
        start = day23_round2(start, s, curr, min_, max_, mem)

    return mem[1].n.n.i, mem[1].n.i * mem[1].n.n.i


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, globals(), 2020)
