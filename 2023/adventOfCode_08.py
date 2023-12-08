# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
import os
import sys
from collections import defaultdict
import time
from typing import List, Mapping

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import day_with_validation  # NOQA: E402
from common.utils import main  # NOQA: E402

YEAR = 2023
DAY = 8
EXPECTED_1 = None
EXPECTED_2 = 6


""" DAY 8 """

def day8_parse(data: List[str]):
    inst = data[0]
    M: Mapping[str, List[str]] = {}
    for line in data[2:]:
        orig, dest = line.split(" = ")
        dest = dest.replace("(", "")
        dest = dest.replace(")", "")
        dest = dest.split(", ")
        M[orig] = dest
    return inst, M

def day8_1(data: List[str]):
    inst, M = day8_parse(data)
    st = "AAA"
    q = []
    curr_i = 0
    count = 0
    while st != "ZZZ":
        if count % 1000 == 0:
            print(count)
        count += 1
        curr_dir = inst[curr_i]
        curr_i = (curr_i + 1) % len(inst)
        if curr_dir == "L":
            st = M[st][0]
        else:
            assert curr_dir == "R"
            st = M[st][1]

    return count

def day8_2(data: List[str]):
    inst, M = day8_parse(data)
    st: List[str] = []
    for k in M.keys():
        if k.endswith("A"):
            st.append(k)
    curr_i = 0
    count = 0
    st_l = len(st)
    print(st_l)
    rem = {s for s in st if not s.endswith("Z")}
    while True:
        if len(rem) == 0:
            return count

        # if count % 1000 == 0:
        #     print(count)
        # if len(rem) < st_l:
        #     print(rem)
        count += 1
        curr_dir = inst[curr_i]
        curr_i = (curr_i + 1) % len(inst)
        for i,s in enumerate(st):
            s = st[i]
            if st[i] in rem:
                rem.remove(st[i])
            if curr_dir == "L":
                st[i] = M[s][0]
            else:
                assert curr_dir == "R"
                st[i] = M[s][1]

            if not st[i].endswith("Z"):
                rem.add(st[i])

    return count


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
