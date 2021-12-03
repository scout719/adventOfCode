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


""" DAY 1 """

def day1_parse(data):
    return [int(x) for x in data]
    # return data

def day1_1(data):
    # data = read_input(2021, 101)
    data = day1_parse(data)
    greater = 0
    for i in range(len(data)):
        if i == 0:
            continue
        if data[i] > data[i - 1]:
            greater += 1
    return greater


def day1_2(data):
    # data = read_input(2021, 101)
    data = day1_parse(data)
    greater = 0
    for i in range(len(data)):
        if i in (0, 1, 2):
            continue
        prev = data[i - 3] + data[i - 2] + data[i - 1]
        curr = data[i - 2] + data[i - 1] + data[i]
        if curr > prev:
            greater += 1
    return greater


""" DAY 2 """

def day2_parse(data):
    return [s.split() for s in data]

def day2_1(data):
    # data = read_input(2021, 201)
    data = day2_parse(data)
    pos = 0
    depth = 0
    for comm, val in data:
        if comm == "forward":
            pos += int(val)
        elif comm == "up":
            depth -= int(val)
        elif comm == "down":
            depth += int(val)
    return depth * pos

def day2_2(data):
    # data = read_input(2021, 201)
    data = day2_parse(data)
    pos = 0
    depth = 0
    aim = 0
    for comm, val in data:
        if comm == "forward":
            pos += int(val)
            depth += aim * int(val)
        elif comm == "up":
            aim -= int(val)
        elif comm == "down":
            aim += int(val)
    return depth * pos


""" DAY 3 """

def day3_parse(data):
    return data

def day3_freq(data, bit):
    n_0 = 0
    n_1 = 0
    for j in range(len(data)):
        curr = data[j][bit]
        if curr == "0":
            n_0 += 1
        else:
            n_1 += 1
    if n_0 > n_1:
        return ("0", "1")
    else:
        return ("1", "0")


def day3_1(data):
    # data = read_input(2021, 301)
    data = day3_parse(data)
    n_bits = len(data[0])
    gamma = ""
    epsilon = ""
    for i in range(n_bits):
        most, least = day3_freq(data, i)
        gamma += most
        epsilon += least

    gamma = int(gamma, 2)
    epsilon = int(epsilon, 2)
    return gamma * epsilon


def day3_2(data):
    # data = read_input(2021, 301)
    data = day3_parse(data)
    n_bits = len(data[0])
    data_copy = ["" + y for y in data]
    for i in range(n_bits):
        most, _ = day3_freq(data, i)
        data = [v for v in data if v[i] == most]
        if len(data) == 1:
            break

    oxygen = int(data[0], 2)
    data = data_copy

    for i in range(n_bits):
        _, least = day3_freq(data, i)
        data = [v for v in data if v[i] == least]
        if len(data) == 1:
            break

    co2 = int(data[0], 2)
    return co2 * oxygen


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, globals(), 2021)
