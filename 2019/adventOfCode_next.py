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

def day16_parse_input(data):
    return [d for d in data[0]]

import itertools
import math
def day16_1(data):
    #data = read_input(2019, 1601)
    data = day16_parse_input(data)
    #data = data[offset:]
    data = [int(d) for d in data]
    pattern = [0,1,0,-1]
    #print(data)
    mem = {}
    l = len(data)
    out=[data, [0 for _ in range(l)]]
    data_idx = 0
    out_idx = 1
    half = l//2
    for p in range(100):
        # print(p)
        #k = ''.join(data)
        #print(k)
        #if k in mem:
            #data = list(mem[k])
            #continue
        o_c = 0
        #last_half = sum(data, l//2)


        while o_c < l:
            out[out_idx][o_c] = 0
            #print(o_c, data)
            #c_pat = [[d]*(o_c+1) for d in pattern]
            #c_pat=list(itertools.chain.from_iterable(c_pat))
            #c_pat = c_pat*max((len(data))//len(c_pat),1)
            #print(c_pat)
            # if o_c % 1000 == 0:
            #     print(o_c, l)

            # if o_c >= l //2:
            #     out[o_c] = sum(data, o_c)
            #     o_c += 1
            #     continue
            value = 0 
            i = o_c
            while i < l:
                if o_c > half:
                    idx = 1
                else:
                    idx = ((i + 1)//(o_c + 1))%4
                # if i % 1000000 == 0:
                #     print(i)
                #print(i)
                if idx == 1:
                    c = out[data_idx][i]
                    value += c
                elif idx % 2 == 0:
                    i += o_c + 1
                    continue
                elif idx == 3:
                    c = out[data_idx][i]
                    value += -c
                i += 1
            out[out_idx][o_c] = abs(value)%10
            o_c += 1


        #mem[k]=out
        # data = out[:]
        data_idx = (data_idx + 1)%2
        out_idx = (out_idx + 1)%2
    return ''.join([str(d) for d in out[data_idx][:8]])

def day16_2(data):
    #data = read_input(2019, 1601)
    data = day16_parse_input(data)
    offset = int(''.join(data[0:7]))
    print(offset)
    data = data*10000
    #data = data[offset:]
    data = [int(d) for d in data]
    pattern = [0,1,0,-1]
    #print(data)
    mem = {}
    l = len(data)
    out=[data, [0 for _ in range(l)]]
    data_idx = 0
    out_idx = 1
    half = l//2
    for p in range(100):
        # print(p)
        #k = ''.join(data)
        #print(k)
        #if k in mem:
            #data = list(mem[k])
            #continue
        o_c = offset
        #last_half = sum(data, l//2)

        s = sum(out[data_idx][o_c:])
        out[out_idx][o_c] = abs(s) % 10
        i = o_c+1
        while i < l:
            s = s - out[data_idx][i-1]
            out[out_idx][i] = abs(s) % 10
            i += 1

        # while o_c < l:
        #     out[out_idx][o_c] = 0
        #     #print(o_c, data)
        #     #c_pat = [[d]*(o_c+1) for d in pattern]
        #     #c_pat=list(itertools.chain.from_iterable(c_pat))
        #     #c_pat = c_pat*max((len(data))//len(c_pat),1)
        #     #print(c_pat)
        #     # if o_c % 1000 == 0:
        #     #     print(o_c, l)

        #     # if o_c >= l //2:
        #     #     out[o_c] = sum(data, o_c)
        #     #     o_c += 1
        #     #     continue
        #     value = 0 
        #     i = o_c
        #     while i < l:
        #         if o_c > half:
        #             idx = 1
        #         else:
        #             idx = ((i + 1)//(o_c + 1))%4
        #         # if i % 1000000 == 0:
        #         #     print(i)
        #         #print(i)
        #         if idx == 1:
        #             c = out[data_idx][i]
        #             value += c
        #         elif idx % 2 == 0:
        #             i += o_c + 1
        #             continue
        #         elif idx == 3:
        #             c = out[data_idx][i]
        #             value += -c
        #         i += 1
        #     out[out_idx][o_c] = abs(value)%10
        #     o_c += 1


        #mem[k]=out
        # data = out[:]
        data_idx = (data_idx + 1)%2
        out_idx = (out_idx + 1)%2
    return ''.join([str(d) for d in out[data_idx][offset:offset+8]])

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