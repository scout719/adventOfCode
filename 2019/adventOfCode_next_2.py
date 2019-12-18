# -*- coding: utf-8 -*-
# pylint: disable=import-error
# pylint: disable=wrong-import-position
from heapq import *
from _collections import defaultdict
from functools import *
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

def n_pos(r, c, grid, seen, count, ks):
    D = [(0,1),(1,0),(-1,0),(0,-1)]
    m=[]
    for d in range(0, 4):
        rrr, ccc = r + D[d][0], c + D[d][1]
        p = grid[rrr][ccc]
        if not (rrr, ccc) in seen:
            if p == '.' or p == "@" or p in ks or p.lower() in ks:
                m += n_pos(rrr,ccc, grid, seen + [(r, c)], count +1, ks)
            elif ord('a') <= ord(p) <= ord('z'):
                m += [(rrr,ccc, count + 1)]
    return m
            

@total_ordering
class Key:
    def __init__(self, steps, keys, doors, grid, pos):
        self.steps = steps
        self.keys = sorted(keys)
        self.doors = sorted(doors)
        self.grid = grid
        self.pos = pos

    def _is_valid_operand(self, other):
        return (hasattr(other, "steps") and
                hasattr(other, "keys") and
                hasattr(other, "doors"))
    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return ((self.steps, self.keys, self.doors) ==
                (other.steps, other.keys, other.doors))
    def __lt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        
        if self.steps != other.steps:
            return self.steps < other.steps
        else:
            return self.steps == other.steps
            return len((self.keys)) > len((other.keys))
            #return len((self.doors)) < len((other.doors)) and len((self.keys)) > len((other.keys))
            self_count = sum([0 if d.lower() in self.keys else 1 for d in self.doors])
            other_count = sum([0 if d.lower() in other.keys else 1 for d in other.doors])
            if self_count != other_count:
                return self_count < other_count
            else:
                return len((self.doors)) < len((other.doors)) and len((self.keys)) > len((other.keys))

from timeit import default_timer as timer
def day18__1(data):
    data = read_input(2019, 1802)
    data = day18_parse_input(data)
    keys = {}
    grid = []
    doors = set()
    for r, row in enumerate(data):
        grid.append([])
        for c, p in enumerate(row):
            grid[r].append(p)
            if ord('a') <= ord(p) <= ord('z'):
                keys[p] = (r, c)
            elif ord('A') <= ord(p) <= ord('Z'):
                doors.add(p)
            elif p == '@':
                start = r,c
    
    seen = {}
    seen_path = {}
    q = [(Key(0, set(), doors, grid, start), start, [], [], doors)]
    D = [(0,1),(1,0),(-1,0),(0,-1)]
    
    res = []
    min_res = None
    paths = set()
    start_t = timer()
    while q:
        key, pos, ks, path, doors = heappop(q)
        steps = key.steps
        if path:
            seen_path[tuple(path)] = steps
        seen[(pos, tuple(sorted(ks)))] = steps
        rr, cc = pos
        if len(keys.keys()) == len(ks):
            #if tuple(path) in paths:
                #assert False
            #paths.add(tuple(path))
            end = timer()
            if min_res is None:
                min_res = steps
                print("                                                                           ", end="\r")
                print("New Min {0} ({1:.3f} secs)".format(min_res, end - start_t))
            elif steps < min_res:
                min_res = steps
                print("                                                                           ", end="\r")
                print("New Min {0} ({1:.3f} secs)".format(min_res, end - start_t))
            if (math.floor(end - start_t)) % 10 == 0:
                print("({1:.3f} secs)".format(min_res, end - start_t), end="\r")
        for rrr, ccc, s in n_pos(rr,cc,grid,[],0, ks):
            #print(rr,cc, rrr,ccc)
            if ((rrr,ccc), tuple(sorted(ks))) in seen and seen[((rrr,ccc), tuple(sorted(ks)))] < steps+s:
                #print(pos, ks, steps+s, seen)
                continue
            p = grid[rrr][ccc]
            # print(len(ks), len(keys.keys()))
            if ord('a') <= ord(p) <= ord('z'):
                path2 = tuple(path + [p])
                if not path2 in seen_path or seen_path[path2] > steps:
                    heappush(q, (Key(steps+s, list(set(ks + [p])), doors, grid, (rrr,ccc)), (rrr,ccc), list(set(ks + [p])), path + [p], doors))
            elif ord('A') <= ord(p) <= ord('Z'):
                if p.lower() in ks:
                    path2 = tuple(path + [p])
                    if not path2 in seen_path or seen_path[path2] > steps:
                        heappush(q, (Key(steps+s, ks, doors-set(p), grid, (rrr,ccc)), (rrr,ccc), ks, path + [p], doors-set(p)))
            else:
                heappush(q, (Key(steps+s, ks, doors, grid, (rrr,ccc)), (rrr,ccc), ks, path, doors))
        #print(q)
    return min(res)

@total_ordering
class Node:
    def __hash__(self):
        return ord(self.door)

    def __init__(self, r,c,v):
        self.connections = set()
        self.door = v
        self.is_door = ord('A') <= ord(v) <= ord('Z')
        self.r = r
        self.c = c

    def __eq__(self, other):
        return self.door == other.door

    def __lt__(self, other):
        return self.door < other.door
    
    def connect(self, other, steps):
        self.connections.add((other, steps))
        other.connections.add((self, steps))

    def __repr__(self):
        return f"{self.door} - ({self.r},{self.c}) {[(other.door, steps) for other, steps in self.connections]}"
        return super().__repr__()

def adjacent_doors(door: Node, grid) -> [str]:
    q = [((door.r, door.c), 0)]
    seen = set()
    doors = []
    D = [(0,1),(1,0),(-1,0),(0,-1)]
    while q:
        pos, steps = q.pop(0)
        seen.add(pos)
        r,c = pos
        for d in range(4):
            rr,cc = r+D[d][0], c+D[d][1]
            p = grid[rr][cc]
            if p != "#" and not (rr,cc) in seen:
                if p == ".":
                    q.append(((rr,cc), steps+1))
                else:
                    doors.append(((rr,cc), p, steps))
                    continue
                # if ord('A') <= ord(p) <= ord('Z') or ord(p) == "@":
                #     continue
                # n_keys = keys
                # if ord('a') <= ord(p) <= ord('z'):
                #     n_keys.append(p)
    
    return doors

def day18_1(data):
    data = read_input(2019, 1801)
    data = day18_parse_input(data)
    total_keys = {}
    grid = []
    doors = set()
    for r, row in enumerate(data):
        grid.append([])
        for c, p in enumerate(row):
            grid[r].append(p)
            if ord('a') <= ord(p) <= ord('z'):
                total_keys[p] = (r, c)
            elif ord('A') <= ord(p) <= ord('Z'):
                doors.add(p)
            elif p == '@':
                start = r,c
    
    # doors = {"@": Node(start[0], start[1], "@")}
    # q = [doors["@"]]
    # while q:
    #     door = q.pop(0)
    #     n_doors = adjacent_doors(door, grid)
    #     for (rr,cc), d, steps in n_doors:
    #         if not d in doors:
    #             doors[d] = Node(rr,cc, d)
    #             q.append(doors[d])
    #         door.connect(doors[d], steps)
    # print(doors)

    # hq = [(0, set(), doors["@"])]
    # seen = {}
    # while hq:
    #     total, keys, door = heappop(hq)
    #     if door.door in seen:
    #         combs = seen[door.door]
    #         cont = False
    #         for s, k in combs:
    #             if s < steps and all([kk in k for kk in keys]):
    #                 cont = True
    #                 break
    #         if cont:
    #             continue
    #     else:
    #         seen[door.door] = []
        
    #     if len(keys) == len(total_keys):
    #         return total
    #     seen[door.door].append((steps, keys))
        
    #     for d, steps in door.connections:
    #         if d.is_door:
    #             if d.door.lower() in keys:
    #                 print(d.door)
    #                 heappush(hq, (total+steps, keys, d))
    #         else:
    #             heappush(hq, (total+steps, set(list(keys) + [d.door]), d))


    # return
    seen = {}
    seen_path = {}
    q = [(0, 0, start, [])]
    D = [(0,1),(1,0),(-1,0),(0,-1)]
    
    res = []
    min_res = None
    paths = set()
    start_t = timer()
    while q:
        steps, ks_l, pos, ks = heappop(q)
        paths.add(tuple(ks))
        rr, cc = pos
        # print(steps, ks)
        if len(total_keys.keys()) == len(ks):
            #if tuple(path) in paths:
                #assert False
            #paths.add(tuple(path))
            end = timer()
            if min_res is None:
                min_res = steps
                return min_res
                print("                                                                           ", end="\r")
                print("New Min {0} ({1:.3f} secs)".format(min_res, end - start_t))
            elif steps < min_res:
                min_res = steps
                print("                                                                           ", end="\r")
                print("New Min {0} ({1:.3f} secs)".format(min_res, end - start_t))
            if (math.floor(end - start_t)) % 10 == 0:
                print("({1:.3f} secs)".format(min_res, end - start_t), end="\r")
        for rrr, ccc, s in n_pos(rr,cc,grid,[],0, ks):
            #print(rr,cc, rrr,ccc)
            # if ((rrr,ccc), tuple(sorted(ks))) in seen and seen[((rrr,ccc), tuple(sorted(ks)))] < steps+s:
            #     #print(pos, ks, steps+s, seen)
            #     continue
            p = grid[rrr][ccc]
            n_ks = ks + [p]
            if tuple(n_ks) in paths:
                continue
            heappush(q, (steps + s, -len(n_pos(rrr,ccc,grid,[],0, n_ks)), (rrr,ccc), n_ks))
            # print(len(ks), len(keys.keys()))
        #print(q)
    return min_res

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


    
    # seen = {}
    # seen_path = {}
    # q = [(Key(0, set(), doors, grid, start), start, [], [], doors)]
    # D = [(0,1),(1,0),(-1,0),(0,-1)]
    
    # res = []
    # min_res = None
    # paths = set()
    # start_t = timer()
    # while q:
    #     key, pos, ks, path, doors = heappop(q)
    #     steps = key.steps
    #     print(steps, path, doors)
    #     if path:
    #         seen_path[tuple(path)] = steps
    #     seen[(pos, tuple(sorted(ks)))] = steps
    #     rr, cc = pos
    #     if len(total_keys.keys()) == len(ks):
    #         #if tuple(path) in paths:
    #             #assert False
    #         #paths.add(tuple(path))
    #         end = timer()
    #         if min_res is None:
    #             min_res = steps
    #             print("                                                                           ", end="\r")
    #             print("New Min {0} ({1:.3f} secs)".format(min_res, end - start_t))
    #         elif steps < min_res:
    #             min_res = steps
    #             print("                                                                           ", end="\r")
    #             print("New Min {0} ({1:.3f} secs)".format(min_res, end - start_t))
    #         if (math.floor(end - start_t)) % 10 == 0:
    #             print("({1:.3f} secs)".format(min_res, end - start_t), end="\r")
    #     for rrr, ccc, s in n_pos(rr,cc,grid,[],0, ks):
    #         #print(rr,cc, rrr,ccc)
    #         if ((rrr,ccc), tuple(sorted(ks))) in seen and seen[((rrr,ccc), tuple(sorted(ks)))] < steps+s:
    #             #print(pos, ks, steps+s, seen)
    #             continue
    #         p = grid[rrr][ccc]
    #         # print(len(ks), len(keys.keys()))
    #         if ord('a') <= ord(p) <= ord('z'):
    #             path2 = tuple(path + [p])
    #             if not path2 in seen_path or seen_path[path2] > steps:
    #                 heappush(q, (Key(steps+s, list(set(ks + [p])), doors, grid, (rrr,ccc)), (rrr,ccc), list(set(ks + [p])), path + [p], doors))
    #         elif ord('A') <= ord(p) <= ord('Z'):
    #             if p.lower() in ks:
    #                 path2 = tuple(path + [p])
    #                 if not path2 in seen_path or seen_path[path2] > steps:
    #                     heappush(q, (Key(steps+s, ks, doors-set(p), grid, (rrr,ccc)), (rrr,ccc), ks, path + [p], doors-set(p)))
    #         else:
    #             heappush(q, (Key(steps+s, ks, doors, grid, (rrr,ccc)), (rrr,ccc), ks, path, doors))
    #     #print(q)
    # return min_res