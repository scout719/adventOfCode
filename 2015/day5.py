# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
import os
import sys
from collections import defaultdict

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
# pylint: enable=wrong-import-position

def day5_solve1(s_list):
    l = []
    for s in s_list:
        m = defaultdict(lambda: 0)
        for c in s:
            m[c] += 1
        valid = sum([m[v] for v in "aeiou"]) >= 3
        valid &= any([l * 2 in s for l in "abcdefghijklmnopqrstuvwxyz"])
        valid &= all([not ss in s for ss in ["ab", "cd", "pq", "xy"]])

        if valid:
            l.append(s)
    return l

def day5_solve2(s_list):
    l = []
    for s in s_list:
        count = 0

        for i in range(len(s) - 1):
            sub_str = s[i] + s[i + 1]
            for j in range(i + 2, len(s) - 1):
                sub_str2 = s[j] + s[j + 1]
                if sub_str == sub_str2:
                    count += 1
        valid = count >= 1

        count = 0
        i = 0
        while i < len(s) - 2:
            if s[i] == s[i + 2]:
                count += 1
                i += 2
            i += 1
        valid &= count >= 1
        if valid:
            l.append(s)
    return l

def day5_1(data):
    return len(day5_solve1(data))

def day5_2(data):
    return len(day5_solve2(data))


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, globals(), 2015)
