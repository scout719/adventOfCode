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

def day17_parse_input(data):
    return [int(d) for d in data[0].split(",")]

def day17_is_scaff(x,y,grid):
    return y >= 0 and y < len(grid) and \
            x >= 0 and x < len(grid[y]) and \
            grid[y][x] != " "

def day17_get_grid(insts):
    output = int_run(insts, [])
    view = ""
    grid = [[]]
    for c in output:
        if c == 35:
            view += WHITE_SQUARE
            grid[-1].append(WHITE_SQUARE)
        elif c== 46:
            view += " "
            grid[-1].append(" ")
        elif c == 10:
            view += "\n"
            grid.append([])
        else:
            view += f"{bcolors.FAIL}{bcolors.BOLD}{chr(c)}{bcolors.ENDC}"
            grid[-1].append(chr(c))
    
    # print(view)
    return grid

def day17_1(data):
    #data = read_input(2019, 1701)
    data = day17_parse_input(data)
    output = int_run(data, [])
    view = ""
    grid = day17_get_grid(data)

    inters = 0
    for y, row in enumerate(grid):
        for x, pos in enumerate(row):
            if pos != " ":
                adjacents = [(x-1, y), (x+1, y), (x,y-1), (x, y+1)]
                if all([day17_is_scaff(a,b, grid) for a,b in adjacents]):
                    inters += x*y
    
    return inters

def day17_2(data):
    #data = read_input(2019, 1701)
    data = day17_parse_input(data)
    data_backup = data[:]
    output = int_run(data, [])
    view = ""
    grid = day17_get_grid(data)

    robot_pos = (0,0)
    for y, row in enumerate(grid):
        for x, pos in enumerate(row):
            if grid[y][x] != ' ' and grid[y][x] != WHITE_SQUARE:
                robot_pos = (x,y)
                break
        if robot_pos != (0,0):
            break
     
    seen = set()
    x,y = robot_pos
    path2 = []
    d = [(-1,0), (0,-1), (1,0), (0,1)]
    curr_d = 1
    d_s = ["L", "R"]
    moves = 0
    while True:
        new_x, new_y = [sum(i) for i in zip(*[(x,y),d[curr_d]])]
        if day17_is_scaff(new_x, new_y, grid):
            moves += 1
            x,y = new_x, new_y
        else:
            d_l = (curr_d - 1) % 4
            d_r = (curr_d + 1) % 4
            new_x_l, new_y_l = [sum(i) for i in zip(*[(x,y),d[d_l]])]
            new_x_r, new_y_r = [sum(i) for i in zip(*[(x,y),d[d_r]])]
            if day17_is_scaff(new_x_l, new_y_l, grid):
                if moves != 0:
                    path2.append(moves)
                path2.append("L")
                moves = 0
                curr_d = d_l
            elif day17_is_scaff(new_x_r, new_y_r, grid):
                if moves != 0:
                    path2.append(moves)
                path2.append("R")
                moves = 0
                curr_d = d_r
            else:
                if moves != 0:
                    path2.append(moves)
                break

    #[A  B B A  B C C B A]
    data = data_backup
    data[0] = 2
    # [A, B, B, A, C, B, C, C, B, A]
    # A R,10,R,8,L,10,L,10
    # B R,8,L,6,L,6
    # C L,10,R,10,L,6
    main = [ord(c) for c in "A|,|B|,|B|,|A|,|C|,|B|,|C|,|C|,|B|,|A".split("|")] + [10]
    A = f"{ord('R')}|{ord(',')}|{ord('1')}|{ord('0')}|{ord(',')}|{ord('R')}|{ord(',')}|{ord('8')}|{ord(',')}|{ord('L')}|{ord(',')}|{ord('1')}|{ord('0')}|{ord(',')}|{ord('L')}|{ord(',')}|{ord('1')}|{ord('0')}|10".split("|")
    B = f"{ord('R')}|{ord(',')}|{ord('8')}|{ord(',')}|{ord('L')}|{ord(',')}|{ord('6')}|{ord(',')}|{ord('L')}|{ord(',')}|{ord('6')}|10".split("|")
    C = f"{ord('L')}|{ord(',')}|{ord('1')}|{ord('0')}|{ord(',')}|{ord('R')}|{ord(',')}|{ord('1')}|{ord('0')}|{ord(',')}|{ord('L')}|{ord(',')}|{ord('6')}|10".split("|")
    response = f"{ord('n')}|10".split("|")
    main = [int(d) for d in main]
    A = [int(d) for d in A]
    B = [int(d) for d in B]
    C = [int(d) for d in C]
    response = [int(d) for d in response]
    def calc():
        c = ""
        if len(main) > 0:
            c = main.pop(0)
        elif len(A) > 0:
            c = A.pop(0)
        elif len(B) > 0:
            c = B.pop(0)
        elif len(C) > 0:
            c = C.pop(0)
        else:
            c = response.pop(0)
        return c
    output = int_run(data, [], calc)
    return output[-1]

# IntCode logic:
def int_run(insts, inputs, calculate_input=None):
    insts = [insts[i] if i < len(insts) else 0 for i in range(10000)]
    pc = 0
    rel_base = 0
    outputs = []
    while insts[pc] != 99:
        op = insts[pc]
        (pc, insts, rel_base) = ic_execute(
            op, pc, insts, inputs, outputs, rel_base, calculate_input)
    return outputs

""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, globals(), 2019)