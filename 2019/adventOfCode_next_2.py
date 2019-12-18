# -*- coding: utf-8 -*-
# pylint: disable=import-error
# pylint: disable=wrong-import-position
from _heapq import *
from _collections import defaultdict
import time
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
print(FILE_DIR)
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
sys.path.insert(0, FILE_DIR + "/../../")
from common.utils import read_input, main, clear  # NOQA: E402
from icComputer import ic_execute  # NOQA: E402
# pylint: enable=import-error
# pylint: enable=wrong-import-position

WHITE_SQUARE = "█"
WHITE_CIRCLE = "•"

def day18_parse_input(data):
    return [str(d) for d in data]

import itertools
import math

def n_pos(r, c, grid, seen, count):
    D = [(0,1),(1,0),(-1,0),(0,-1)]
    m=[]
    for d in range(0, 4):
        rrr, ccc = r + D[d][0], c + D[d][1]
        p = grid[rrr][ccc]
        if not (rrr, ccc) in seen:
            if p == '.':
                m += n_pos(rrr,ccc, grid, seen + [(r, c)], count +1)
            elif p != '#':
                m += [(rrr,ccc, count + 1)]
    return m
            
def day18_1(data):
    data = read_input(2019, 1802)
    data = day18_parse_input(data)
    keys = {}
    grid = []
    for r, row in enumerate(data):
        grid.append([])
        for c, p in enumerate(row):
            grid[r].append(p)
            if ord('a') <= ord(p) <= ord('z'):
                keys[p] = (r, c)
            elif p == '@':
                start = r,c
    
    seen = set()
    q = [(0, 0, start, [])]
    D = [(0,1),(1,0),(-1,0),(0,-1)]
    
    while q:
        ks_l, steps, pos, ks = heappop(q)
        seen.add((pos, tuple(sorted(ks))))
        rr, cc = pos
        if len(keys.keys()) == len(ks):
            return steps
        for rrr, ccc, s in n_pos(rr,cc,grid,[],0):
           if ((rrr,ccc), tuple(sorted(ks))) in seen:
               continue
           p = grid[rrr][ccc]
           #print(pos, ks, steps)
           #print(len(ks), len(keys.keys()))
           if ord('a') <= ord(p) <= ord('z'):
               heappush(q, (ks_l-1, steps+s, (rrr,ccc), ks + [p]))
           elif ord('A') <= ord(p) <= ord('Z'):
               if p.lower() in ks:
                   heappush(q, (ks_l, steps+s, (rrr,ccc), ks))
           else:
               heappush(q, (ks_l, steps+s, (rrr,ccc), ks))
    return None

# IntCode logic:
# def int_run(insts, inputs):
#     def calculate_input():
#         return 0
#     pc = 0
#     rel_base = 0
#     outputs = []
#     while insts[pc] != 99:
#         op = insts[pc]
#         (pc, insts, rel_base) = day2_execute(
#             op, pc, insts, inputs, outputs, rel_base, calculate_input)
#     return outputs

""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, globals(), 2019)