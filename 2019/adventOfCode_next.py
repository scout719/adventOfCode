# -*- coding: utf-8 -*-
# pylint: disable=import-error
# pylint: disable=wrong-import-position
# from _heapq import *
# from _collections import defaultdict
# import time
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

def day20_parse_input(data):
    return [d for d in data]

from collections import defaultdict
from heapq import *
def day20_1(data):
    #data = read_input(2019, 2001)
    data = day20_parse_input(data)
    
    grid = []
    for r, row in enumerate(data):
        grid.append([])
        for c, tile in enumerate(row):
            grid[-1].append(tile)
    
    R = len(grid)
    C = len(grid[0])
    x = 3
    while grid[R//2][x] == "." or grid[R//2][x] == "#":
        x +=1
    left = [(2,2), (x-1,R-3)]
    while grid[R//2][x] != "." and grid[R//2][x] != "#":
        x +=1
    right = [(x,2), (C-3,R-3)]
    y = 3
    while grid[y][C//2] == "." or grid[y][C//2] == "#":
        y +=1
    top = [(2,2), (C-3,y-1)]
    while grid[y][C//2] != "." and grid[y][C//2] != "#":
        y +=1
    bottom = [(2,y), (C-3,R-3)]
    
    ileftc = left[1][0]
    irightc = right[0][0]
    itopr = top[1][1]
    ibottomr = bottom[0][1]
    
    portals = defaultdict(lambda: [])
    for r, row in enumerate(grid):
        for c, t in enumerate(row):
            if t == ".":
                if r == 2:
                    p = grid[r-2][c] + grid[r-1][c]
                    portals[p].append((r,c))
                if r == R-3:
                    p = grid[R-2][c] + grid[R-1][c]
                    portals[p].append((r,c))
                if c == 2:
                    p = grid[r][c-2] + grid[r][c-1]
                    portals[p].append((r,c))
                if c == C-3:
                    p = grid[r][C-2] + grid[r][C-1]
                    portals[p].append((r,c))
                if r == itopr:
                    p = grid[itopr+1][c] + grid[itopr+2][c]
                    portals[p].append((r,c))
                if r == ibottomr:
                    p = grid[ibottomr-2][c] + grid[ibottomr-1][c]
                    portals[p].append((r,c))
                if c == ileftc:
                    p = grid[r][ileftc+1] + grid[r][ileftc+2]
                    portals[p].append((r,c))
                if c == irightc:
                    p = grid[r][irightc-2] + grid[r][irightc-1]
                    portals[p].append((r,c))
    
    rportals = {}
    for key in portals:
        if key != "AA" and key != "ZZ":
            rportals[portals[key][0]] = key
            rportals[portals[key][1]] = key
                
    #del portals["##"]
    #del portals["  "]
    del portals[".."]
    del portals[".#"]
    del portals["#."]
    
    q = [(0, portals["AA"][0])]
    seen = {}
    D=[(0,1), (-1, 0), (0, -1), (1,0)]
    while q:
        steps, pos = heappop(q)
        if pos in seen and seen[pos] < steps:
            continue
        r,c = pos
        print(steps, pos)
        if portals["ZZ"][0] == pos:
            return steps
        seen[pos]=steps
        for d in range(4):
            rr, cc = r+D[d][1], c+D[d][0]
            #if not (steps+1, (rr,cc)) in seen:
                
            if grid[rr][cc] == ".":
                heappush(q, (steps+1, (rr,cc)))
        if pos in rportals:
            p = rportals[pos]
            for rr,cc in portals[p]:
                if (rr,cc) != pos:# and not (steps+1, (rr,cc)) in seen:
                    heappush(q, (steps+1, (rr,cc)))
                    
        
    print(portals["ZZ"])
    return None
    

def day20__2(data):
    #data = read_input(2019, 2001)
    data = day20_parse_input(data)
    return data

# IntCode logic:
# def int_run_20(insts, inputs, calculate_input=None):
#     insts = [insts[i] if i < len(insts) else 0 for i in range(10000)]
#     pc = 0
#     rel_base = 0
#     outputs = []
#     while not outputs or insts[pc] != 99:
#         op = insts[pc]
#         (pc, insts, rel_base) = ic_execute(
#             op, pc, insts, inputs, outputs, rel_base, calculate_input)
#     return outputs

""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, globals(), 2019)