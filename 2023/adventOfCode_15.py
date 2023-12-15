# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
from collections import defaultdict
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import day_with_validation  # NOQA: E402
from common.utils import main  # NOQA: E402

YEAR = 2023
DAY = 15
EXPECTED_1 = 1320
EXPECTED_2 = 145

""" DAY 15 """

def day15_parse(data: list[str]):
    return [step for step in data[0].split(",")]

def day15_hash(label):
    hash_ = 0
    for c in label:
        val = ord(c)
        hash_ += val
        hash_ *= 17
        hash_ %= 256
    return hash_

def day15_1(data):
    sequence = day15_parse(data)
    ans = 0
    for step in sequence:
        hash_ = day15_hash(step)
        ans += hash_
    return ans

def day15_2(data: list[str]):
    sequence = day15_parse(data)
    boxes = defaultdict(list)
    for step in sequence:
        label = step.split("=")[0]
        label = label.rstrip("-")
        box_id = day15_hash(label)
        box = boxes[box_id]
        slot = 0
        while slot < len(box) and box[slot][0] != label:
            slot += 1
        if step.endswith("-"):
            if slot != len(box):
                # lens is present
                del box[slot]
        else:
            assert "=" in step
            pair = step.split("=")
            if slot == len(box):
                # not present
                box.append(pair)
            else:
                box[slot] = pair
    ans = 0
    for box_id, pairs in boxes.items():
        for slot, (_, f_length) in enumerate(pairs):
            ans += (box_id + 1) * (slot + 1) * int(f_length)

    return ans


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
