# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
from collections import defaultdict
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2024
DAY = 9
EXPECTED_1 = 1928
EXPECTED_2 = 2858


""" DAY 9 """

def day9_parse(data: list[str]):
    return [int(s) for s in data[0]]

def day9_1(data):
    disk = day9_parse(data)
    disk_clone = [] + disk
    curr_file = len(disk) - 1
    if curr_file % 2 != 0:
        curr_file -= 1
    curr_space = 1
    new_disk = defaultdict(list)
    space_start = disk[0]
    while curr_file > curr_space:
        if disk[curr_file] > disk[curr_space]:
            new_disk[curr_file //
                     2].append((space_start, space_start + disk[curr_space]))
            space_start += disk[curr_space] + disk[curr_space + 1]
            disk[curr_file] -= disk[curr_space]
            curr_space += 2
        elif disk[curr_file] < disk[curr_space]:
            new_disk[curr_file //
                     2].append((space_start, space_start + disk[curr_file]))
            space_start += disk[curr_file]
            disk[curr_space] -= disk[curr_file]
            curr_file -= 2
        else:
            new_disk[curr_file //
                     2].append((space_start, space_start + disk[curr_space]))
            space_start += disk[curr_file] + disk[curr_space + 1]
            disk[curr_file] -= disk[curr_file]
            disk[curr_space] -= disk[curr_space]
            curr_file -= 2
            curr_space += 2

    curr_space = 0
    for pos, p in enumerate(disk_clone):
        if pos <= curr_file:
            if pos % 2 == 0 and disk[pos] > 0:
                new_disk[pos // 2].append((curr_space, curr_space + disk[pos]))
        curr_space += p

    ans = 0
    for file_id, chunks in new_disk.items():
        for l, r in chunks:
            for pos in range(l, r):
                ans += pos * file_id
    return ans

def day9_2(data):
    disk = day9_parse(data)
    space = []
    new_disk = defaultdict(list)
    curr_space = 0
    for pos, s in enumerate(disk):
        if pos % 2 != 0:
            space.append((curr_space, curr_space + s))
        else:
            new_disk[pos // 2].append((curr_space, curr_space + s))
        curr_space += s

    curr_file = len(disk) - 1
    if curr_file % 2 != 0:
        curr_file -= 1
    while curr_file >= 0:
        file_left_pos = new_disk[curr_file // 2][0][0]
        for pos, (l, r) in enumerate(space):
            if l > file_left_pos:
                # we only move files to the left
                break
            if r - l >= disk[curr_file]:
                new_disk[curr_file // 2] = [(l, l + disk[curr_file])]
                space[pos] = (l + disk[curr_file], r)
                disk[curr_file] = 0
                break
        curr_file -= 2

    ans = 0
    for file_id, chunks in new_disk.items():
        assert len(chunks) == 1
        for l, r in chunks:
            for pos in range(l, r):
                ans += pos * file_id
    # high 8632330985597
    return ans


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
