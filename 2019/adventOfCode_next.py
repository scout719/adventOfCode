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

def day19_parse_input(data):
    return [int(d) for d in data[0].split(",")]

def day19_1(data):
    #data = read_input(2019, 1901)
    data = day19_parse_input(data)
    grid = [[0 for _ in range(50)] for _ in range(50)]
    count =0
    def g_i():
        #print(pos)
        return pos.pop(0)
    
    for x in range(50):
        for y in range(50):
            pos = [x,y]
            
            grid[y][x] = int_run_19(data, [], g_i)[-1]
            count += grid[y][x]
    
    for r , row in enumerate(grid):
        print()
        for c, p in enumerate(row):
            if p == 1:
                print(WHITE_SQUARE, end="")
            else:
                print(".", end="")
    
    return count

def checkx(data, x, y):
    def g_i():
        return pos.pop(0)
    q = [(x,y, -1), (x,y,1)]
    count = 1
    while q:
        x,y,d = q.pop(0)
        pos = [x+d,y]
        v = int_run_19(data, [], g_i)[-1]
        if v == 1:
           count += 1
           q.append((x+d, y, d))
    return count 
def checky(data, x, y):
    def g_i():
        return pos.pop(0)
    q = [(x,y, -1), (x,y,1)]
    count = 1
    while q:
        x,y,d = q.pop(0)
        pos = [x+d,y]
        v = int_run_19(data, [], g_i)[-1]
        if v == 1:
           count += 1
           q.append((x+d, y, d))
    return count 

def c(data, x,y):
    def g_i():
        return pos.pop(0)
    xx,yy = x,y
    pos = [x,y]
    while int_run_19(data, [], g_i)[-1] == 1:
        x +=1
        pos =[x,y]
    width = x - xx
    xx = xx + (width//2)
    pos = [xx,y]
    while int_run_19(data, [], g_i)[-1] == 1:
        y +=1
        pos =[xx,y]
    height = y - yy
    return height, width//2
    

def day19_2(data):
    #return
    #data = read_input(2019, 1901)
    data = day19_parse_input(data)
    count =0
    def g_i():
        return pos.pop(0)
    
    q = [(0,0)]
    while q:
        x, y = q.pop(0)
        pos=[x,y]
        v = int_run_19(data, [], g_i)[-1]
        if v == 1:
            dims = c(data, x,y)
            print(y, dims)
            x=x
            if y == 0:
                y += 640
            y+=1
            pos = [x,y]
            while int_run_19(data, [], g_i)[-1] == 0:
                x +=1
                pos =[x,y]
            q.append((x,y))
           
            
    
    return count

# IntCode logic:
def int_run_19(insts, inputs, calculate_input=None):
    insts = [insts[i] if i < len(insts) else 0 for i in range(10000)]
    pc = 0
    rel_base = 0
    outputs = []
    while not outputs or insts[pc] != 99:
        op = insts[pc]
        (pc, insts, rel_base) = ic_execute(
            op, pc, insts, inputs, outputs, rel_base, calculate_input)
    return outputs

""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, globals(), 2019)