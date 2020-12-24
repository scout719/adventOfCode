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

""" DAY 24 """

def day24_parse(data):
    tiles = []
    for line in data:
        curr_dir = ""
        curr_tile = []
        for c in list(line):
            curr_dir += c
            if curr_dir in ["e", "se", "sw", "w", "nw", "ne"]:
                curr_tile.append(curr_dir)
                curr_dir = ""

        tiles.append(curr_tile)

    return tiles

def day24_move(dir_):
    mov = {
        "e": (0 + 1, 0),
        "se": (0 + 0.5, 0 + 1),
        "sw": (0 - 0.5, 0 + 1),
        "w": (0 - 1, 0),
        "nw": (0 - 0.5, 0 - 1),
        "ne": (0 + 0.5, 0 - 1)
    }
    return mov[dir_]

def day24_1(data):
    # data = read_input(2020, 2401)
    tiles = day24_parse(data)

    tiles_pos = {}
    for tile in tiles:
        x, y = 0, 0
        for dir_ in tile:
            dx, dy = day24_move(dir_)
            x, y = x + dx, y + dy
            # print(x, y, dir_)
        pos = (x, y)
        # print(tile, pos)
        if pos not in tiles_pos:
            tiles_pos[pos] = True
        else:
            tiles_pos[pos] = not tiles_pos[pos]

    return sum([1 for x in tiles_pos.values() if x])

# def day24_print(tiles_pos):


def day24_2(data):
    # data = read_input(2020, 2401)
    tiles = day24_parse(data)

    tiles_pos = {}
    for tile in tiles:
        x, y = 0, 0
        for dir_ in tile:
            dx, dy = day24_move(dir_)
            x, y = x + dx, y + dy
            # print(x, y, dir_)
        pos = (x, y)
        # print(tile, pos)
        if pos not in tiles_pos:
            tiles_pos[pos] = True
        else:
            tiles_pos[pos] = not tiles_pos[pos]
    min_x = min([x for x, y in tiles_pos.keys()])
    max_x = max([x for x, y in tiles_pos.keys()])
    min_y = min([y for x, y in tiles_pos.keys()])
    max_y = max([y for x, y in tiles_pos.keys()])
    print(min_x, max_x, min_y, max_y)
    print(tiles_pos)
    for x in range(int(min_x - 1), int(max_x + 2)):
        for y in range(min_y - 1, max_y + 2):
            if y % 2 != 0:
                dx = 0.5
            else:
                dx = 0
            pos = x + dx, y
            if pos not in tiles_pos:
                tiles_pos[pos] = False
    print(tiles_pos)

    for _ in range(100):
        n_tiles_pos = {}
        edges = set()
        for t in tiles_pos:
            x, y = t
            count = 0
            for dir_ in ["e", "se", "sw", "w", "nw", "ne"]:
                dx, dy = day24_move(dir_)
                nx, ny = x + dx, y + dy
                if (nx, ny) in tiles_pos:
                    if tiles_pos[(nx, ny)]:
                        count += 1
                else:
                    edges.add((nx, ny))
            if tiles_pos[t] and (count == 0) or (count > 2):
                n_tiles_pos[t] = False
            elif not tiles_pos[t] and (count == 2):
                n_tiles_pos[t] = True
            else:
                n_tiles_pos[t] = tiles_pos[t]
            # print(t,tiles_pos[t], count, n_tiles_pos[t])
        for x, y in edges:
            n_tiles_pos[(x, y)] = False

        tiles_pos = n_tiles_pos
        print(sum([1 for x in tiles_pos.values() if x]))

    return sum([1 for x in tiles_pos.values() if x])
    # reutrn


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, globals(), 2020)
