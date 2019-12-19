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

def all_dist2(k, r,c, grid):
    D = [(0,1),(1,0),(-1,0),(0,-1)]
    m=[]
    q = [(r,c, 0)]
    seen = {(r,c):0}
    dists = {}
    while q:
        rr,cc,count = heappop(q)

        for d in range(0, 4):
            rrr, ccc = rr + D[d][0], cc + D[d][1]
            if not (rrr, ccc) in seen or seen[(rrr,ccc)] > count+1:
                seen[(rrr,ccc)] = count+1
                p = grid[rrr][ccc]
                if p == '.' or p == "@":
                    heappush(q, (rrr,ccc, count+1))
                # elif ord('A') <= ord(p) <= ord('Z'):
                    # q.append((rrr,ccc, count+1, doors + [p.lower()]))
                elif p != "#":
                    dists[p] = (rrr,ccc, count + 1)
                    # m.append((rrr,ccc, count + 1))
    return dists

def n_pos2(p, grid, dists, ks):
    D = [(0,1),(1,0),(-1,0),(0,-1)]
    m=[]
    q = [(p, 0)]
    seen = set([p])
    while q:
        pp, steps = q.pop()
        for ppp in dists[pp]:
            if not ppp in seen:
                seen.add(ppp)
                r,c, s = dists[pp][ppp]
                if ord('A') <= ord(ppp) <= ord('Z') and ppp.lower() in ks:
                    q.append((ppp, steps +s))
                elif ord('a') <= ord(ppp) <= ord('z'):
                    if ppp in ks:
                        q.append((ppp, steps +s))
                    else:
                        m.append((ppp, steps + s))
    return m
from timeit import default_timer as timer

def day18_1(data):
    # data = read_input(2019, 1801)   
    data = day18_parse_input(data)
    total_keys = {}
    grid = []
    doors = {}
    for r, row in enumerate(data):
        grid.append([])
        for c, p in enumerate(row):
            grid[r].append(p)
            if ord('a') <= ord(p) <= ord('z'):
                total_keys[p] = (r, c)
            elif ord('A') <= ord(p) <= ord('Z'):
                doors[p] = (r,c)
            elif p == '@':
                total_keys[p] = (r, c)
                start = r,c
    
    dists = {}
    for key in total_keys:
        r,c = total_keys[key]
        dists[key] = all_dist2(key,r,c,  grid)
    for door in doors:
        r,c = doors[door]
        dists[door] = all_dist2(door,r,c,  grid)

    q = [(0, "@", [])]
    
    min_res = None
    seen3 = {}
    total_keys_n = len(total_keys.keys())-1 # remove @
    while q:
        steps, key, ks = heappop(q)
        # print(steps, ks)
        # paths.add(tuple(ks))
        # k  =tuple([steps, key] + sorted(ks))
        # seen2.add(k)
        # k  =tuple([key] + sorted(ks))
        # if k in seen3 and seen3[k] < steps:
        #     continue

        #k  =(tuple(sorted(ks)), steps)
        # print(steps, ks, pos)
        if total_keys_n == len(ks):
            #if tuple(path) in paths:
                #assert False
            #paths.add(tuple(path))
            return steps
        
        for other_key, s in n_pos2(key, grid, dists, ks):

            #m.append((other_key,steps))
            #print(rr,cc, rrr,ccc)
            # if ((rrr,ccc), tuple(sorted(ks))) in seen and seen[((rrr,ccc), tuple(sorted(ks)))] < steps+s:
            #     #print(pos, ks, steps+s, seen)
            #     continue
            n_ks = ks + [other_key]
            # if tuple(n_ks) in paths:
            #     continue
            # heappush(q, (steps + s, -len(n_pos(rrr,ccc,grid,[],0, n_ks)), (rrr,ccc), n_ks))
            k  =tuple([other_key] + sorted(n_ks))
            if k in seen3 and seen3[k] < steps+s:
                continue
            seen3[k] = steps+s
            heappush(q, (steps + s, other_key, n_ks))
            #print(len(ks), len(total_keys.keys()))
        #print(q)
    return min_res

# def day18_2(data):
#     # data = read_input(2019, 1801)   
#     data = day18_parse_input(data)
#     total_keys = {}
#     grid = []
#     doors = {}
#     for r, row in enumerate(data):
#         grid.append([])
#         for c, p in enumerate(row):
#             grid[r].append(p)
#             if ord('a') <= ord(p) <= ord('z'):
#                 total_keys[p] = (r, c)
#             elif ord('A') <= ord(p) <= ord('Z'):
#                 doors[p] = (r,c)
#             elif p == '@':
#                 start = r,c
#     D = [-1,0,1]
#     count = 1
#     robots = []
#     for i in range(3):
#         for j in range(3):
#             rr,cc = start[0] + D[i], start[1] + D[j]
#             if abs(i) + abs(j) == 2:
#                 grid[rr][cc] = str(count)
#                 total_keys[str(count)] = (rr,cc)
#                 robots.append((rr,cc))
#                 count += 1
#             else:
#                 grid[rr][cc] = "#"
#     dists = {}
#     for key in total_keys:
#         r,c = total_keys[key]
#         dists[key] = all_dist2(key,r,c,  grid)
#     for door in doors:
#         r,c = doors[door]
#         dists[door] = all_dist2(door,r,c,  grid)
    
#     for key in total_keys:
#         r,c = total_keys[key]
#         if r <=  robots[0][0] and  r <=  robots[0][0]


#     q = [(0, "@", [])]
    
#     min_res = None
#     seen3 = {}
#     total_keys_n = len(total_keys.keys())-1 # remove @
#     while q:
#         steps, key, ks = heappop(q)
#         # print(steps, ks)
#         # paths.add(tuple(ks))
#         # k  =tuple([steps, key] + sorted(ks))
#         # seen2.add(k)
#         # k  =tuple([key] + sorted(ks))
#         # if k in seen3 and seen3[k] < steps:
#         #     continue

#         #k  =(tuple(sorted(ks)), steps)
#         # print(steps, ks, pos)
#         if total_keys_n == len(ks):
#             #if tuple(path) in paths:
#                 #assert False
#             #paths.add(tuple(path))
#             return steps
        
#         for other_key, s in n_pos2(key, grid, dists, ks):

#             #m.append((other_key,steps))
#             #print(rr,cc, rrr,ccc)
#             # if ((rrr,ccc), tuple(sorted(ks))) in seen and seen[((rrr,ccc), tuple(sorted(ks)))] < steps+s:
#             #     #print(pos, ks, steps+s, seen)
#             #     continue
#             n_ks = ks + [other_key]
#             # if tuple(n_ks) in paths:
#             #     continue
#             # heappush(q, (steps + s, -len(n_pos(rrr,ccc,grid,[],0, n_ks)), (rrr,ccc), n_ks))
#             k  =tuple([other_key] + sorted(n_ks))
#             if k in seen3 and seen3[k] < steps+s:
#                 continue
#             seen3[k] = steps+s
#             heappush(q, (steps + s, other_key, n_ks))
#             #print(len(ks), len(total_keys.keys()))
#         #print(q)
#     return min_res

def day18__1(data):
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
                #total_keys[p] = (r, c)
                start = r,c
    
    # dists = {} key] = all_dist(key, total_keys, grid)

    seen = {}
    seen_path = {}
    q = [(0, 0, start, set())]
    D = [(0,1),(1,0),(-1,0),(0,-1)]
    
    res = []
    min_res = None
    paths = set()
    start_t = timer()
    seen2 = set()
    i = 0
    total_keys_n = len(total_keys.keys())
    while q:
        i += 1
        steps, ks_l, pos, ks = heappop(q)
        # paths.add(tuple(ks))
        k  =tuple([steps] + sorted(ks) + list(pos))
        seen2.add(k)
        rr, cc = pos

        if i% 10000 == 0:
            end = timer()
            print("                                                                           ", end="\r")
            print("{0} {1} {2} ({3:.3f} secs)".format(len(ks),total_keys_n, len(q), end - start_t), end="\r")
            print(len(ks),total_keys_n, len(q))

        #k  =(tuple(sorted(ks)), steps)
        # print(steps, ks, pos)
        if total_keys_n == len(ks):
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
            n_ks = ks.union([p])
            # if tuple(n_ks) in paths:
            #     continue
            # heappush(q, (steps + s, -len(n_pos(rrr,ccc,grid,[],0, n_ks)), (rrr,ccc), n_ks))
            
            k  =tuple([steps+s] + sorted(n_ks) + [rrr,ccc])
            if k in seen2:
                continue
            seen2.add(k)
            heappush(q, (steps + s, 0, (rrr,ccc), n_ks))
            #print(len(ks), len(total_keys.keys()))
        #print(q)
    return min_res

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