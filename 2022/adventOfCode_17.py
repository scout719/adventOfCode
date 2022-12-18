# -*- coding: utf-8 -*-
# pylint: disable=import-error
# pylint: disable=unused-import
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
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
from common.utils import main, day_with_validation, WHITE_SQUARE  # NOQA: E402
# pylint: enable=import-error
# pylint: enable=wrong-import-position

YEAR = 2022
DAY = 17
EXPECTED_1 = 3068
EXPECTED_2 = 1514285714288

""" DAY 17 """


def day17_parse(data):
    return list(data[0])

def day17_rockt(t):
    shapes = [
        [(0,0), (0, 1), (0,2), (0, 3)],
        [(0,1), (1,0), (1,1), (1,2), (2,1)],
        [(0,0), (0,1), (0,2), (1,2), (2,2)],
        [(0,0), [1,0], (2,0), (3,0)],
        [[0,0], (0,1), (1,0),(1,1)]
    ]

    return shapes[t%5]

def day17_print(G):
    max_r = max(r for r,_ in G) if G else 3
    min_r = 0
    for r in range(max_r, -1, -1):
        line = "|"
        for c in range(0, 7):
            if (r,c) in G:
                line += WHITE_SQUARE
            else:
                line += " "
        line += "|"
        print(line)
    print("-"*9)
    print()

    
def day17_1(data):
    data = day17_parse(data)
    rocks = []
    G = set()
    i = 0
    for t in range(2022):
        # day17_print(G)
        # for r2 in rocks:
        #     max_r = max(max_r, max(rr for rr,cc in r2))
        max_r = max(r for r,c in G) if G else -1
        shape = day17_rockt(t)
        # print("shape")
        # day17_print_s([shape])
        shape = [(max_r + 3 + 1 + rr, cc + 2) for rr,cc in shape]
        moving = True
        while moving:
            # if t > 4:
            # lse
            # print(i)
            m = data[i%len(data)]
            # day17_print(rocks + [shape])
            # print(m)
            i+=1
            dc = 0
            if m == "<":
                dc = -1
            else:
                assert m == ">"
                dc = 1
                
            can_move = True
            for rr,cc in shape:
                if not(0<=cc+dc<7):
                    can_move = False
                    break
                if (rr, cc+dc) in G:
                    can_move = False
                    break
            if can_move:
                shape = [(rr, cc + dc) for rr,cc in shape]
            # print(m)
            # day17_print(rocks + [shape])

            can_drop = True
            for rr,cc in shape:
                if (rr-1, cc) in G or rr-1 < 0:
                    can_drop = False
                    break
            # for rr,cc in shape:
            #     if rr-1 < 0:
            #         can_drop &= False
            #     for other in rocks:
            #         for rrr,ccc in other:
            #             if rrr == rr-1 and ccc == cc:
            #                 can_drop &= False
            # print(shape)

            if can_drop:
                shape = [(rr-1, cc) for rr,cc in shape]
            else:
                for r,c in shape:
                    G.add((r,c))
                moving = False
    return max(r for r,_ in G)+1
            

    return ""

def day17_2(data):
    data = day17_parse(data)
    rocks = []
    G = set()
    i = 0
    for t in range(1000000000000):
        # day17_print(G)
        # for r2 in rocks:
        #     max_r = max(max_r, max(rr for rr,cc in r2))
        max_r = max(r for r,c in G) if G else -1

        for dr in range(20):
            complete = True
            for c in range(7):
                if (max_r-dr,c) not in G:
                    complete = False
                    break
            if complete:
                print(t, i)
                print(t, i)

        shape = day17_rockt(t)
        # print("shape")
        # day17_print_s([shape])
        shape = [(max_r + 3 + 1 + rr, cc + 2) for rr,cc in shape]
        moving = True
        while moving:
            # if t > 4:
            # lse
            # print(i)
            m = data[i%len(data)]
            # day17_print(rocks + [shape])
            # print(m)
            i+=1
            dc = 0
            if m == "<":
                dc = -1
            else:
                assert m == ">"
                dc = 1
                
            can_move = True
            for rr,cc in shape:
                if not(0<=cc+dc<7):
                    can_move = False
                    break
                if (rr, cc+dc) in G:
                    can_move = False
                    break
            if can_move:
                shape = [(rr, cc + dc) for rr,cc in shape]
            # print(m)
            # day17_print(rocks + [shape])

            can_drop = True
            for rr,cc in shape:
                if (rr-1, cc) in G or rr-1 < 0:
                    can_drop = False
                    break
            # for rr,cc in shape:
            #     if rr-1 < 0:
            #         can_drop &= False
            #     for other in rocks:
            #         for rrr,ccc in other:
            #             if rrr == rr-1 and ccc == cc:
            #                 can_drop &= False
            # print(shape)

            if can_drop:
                shape = [(rr-1, cc) for rr,cc in shape]
            else:
                for r,c in shape:
                    G.add((r,c))
                moving = False
    return max(r for r,_ in G)+1
    
    return ""


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
