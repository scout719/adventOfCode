# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2025
DAY = 5
EXPECTED_1 = 3
EXPECTED_2 = 14

def day5_parse(data: list[str]):
    ranges = set()
    in_ranges = True
    avail = set()
    for line in data:
        if not line:
            in_ranges = False
            continue
        if in_ranges:
            l, r = line.split("-")
            ranges.add((int(l), int(r)))
        else:
            avail.add(int(line))

    return ranges, avail

def day5_adj(r, c, rolls):
    total = 0
    D = [-1, 0, 1]
    for dr in D:
        for dc in D:
            if dr == dc == 0:
                continue
            rr, cc = r + dr, c + dc
            if (rr, cc) in rolls:
                total += 1
    return total

def day5_solve(data, part2):
    ranges, avail = day5_parse(data)

    if not part2:
        total = 0
        for i in avail:
            for l, r in ranges:
                if l <= i <= r:
                    total += 1
                    break
        return total

    intervals = []
    for l, r in ranges:
        new_intervals = []
        i = 0
        # indicates if we're inside an interval or not
        inside = False

        # keep all intervals until we reach the start of the current range
        while i < len(intervals) and intervals[i] < l:
            inside = not inside
            new_intervals.append(intervals[i])
            i += 1

        if inside:
            # We're already inside an interval,
            # so keep it going as it would be 'opened' by the current range
            pass
        else:
            # We're outside an interval,
            # start a new one for the current range
            new_intervals.append(l)

        # 'Absorb' all intermidiate intervals until we reach the end of the current range
        while i < len(intervals) and intervals[i] <= r:
            inside = not inside
            i += 1

        if not inside:
            # We're in a point where no interval was opened,
            # but we 'opened' one at the start of the current range,
            # so we must close it
            if (i >= len(intervals) or intervals[i] != r):
                # However, we should only close it
                # if next interval wasn't about to open it exactly at r as well
                new_intervals.append(r)
        else:
            # inside, continue range
            pass

        while i < len(intervals):
            new_intervals.append(intervals[i])
            i += 1

        assert len(new_intervals) % 2 == 0, (l, r, intervals, new_intervals)
        # l = 259834369549045
        # r = 260402819310713
        # intervals =     [1138886722630, 1854190426883, 2351348670325, 2617031498963, 4400855877487, 4868742298198, 14267065719571, 19713754885181, 61304715018545, 66159151881093, 81520617554440, 87934729706190, 103525263650762, 109263601125387, 132305455060243, 136355961131249, 183960576643697, 184978726668743, 193190914974227, 194389809136271, 195881464266764, 198893061877806, 254684163193254, 254912091501406, 255753644093984, 256141049798709, 257130691987536, 257951515966143, 260402819310713, 260801313119541, 292907892178176, 295216301045006, 298727251504138, 300461809160696, 302542078244300, 305345714739584, 320106355013024, 320106355013024, 323845023844190, 329536560310239, 349383978844235, 349762616770401, 396167498820829, 398717779535761, 435738105327068, 436449599122321, 436639876131680, 436867778393908, 438992222880514, 439720188043393, 441279431671536, 441734947012175, 444969405647581, 446718802519496, 541881978152383, 541881978152383]
        # new_intervals = [1138886722630, 1854190426883, 2351348670325, 2617031498963, 4400855877487, 4868742298198, 14267065719571, 19713754885181, 61304715018545, 66159151881093, 81520617554440, 87934729706190, 103525263650762, 109263601125387, 132305455060243, 136355961131249, 183960576643697, 184978726668743, 193190914974227, 194389809136271, 195881464266764, 198893061877806, 254684163193254, 254912091501406, 255753644093984, 256141049798709, 257130691987536, 257951515966143, 259834369549045, 260402819310713, 260801313119541, 292907892178176, 295216301045006, 298727251504138, 300461809160696, 302542078244300, 305345714739584, 320106355013024, 320106355013024, 323845023844190, 329536560310239, 349383978844235, 349762616770401, 396167498820829, 398717779535761, 435738105327068, 436449599122321, 436639876131680, 436867778393908, 438992222880514, 439720188043393, 441279431671536, 441734947012175, 444969405647581, 446718802519496, 541881978152383, 541881978152383])
        intervals = new_intervals

    assert len(intervals) % 2 == 0, intervals
    total = 0
    i = 0
    while i < len(intervals):
        total += intervals[i + 1] - intervals[i] + 1
        i += 2
    # low 295780976907849
    # low 225292950610338
    return total

def day5_1(data):
    return day5_solve(data, False)

def day5_2(data):
    return day5_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
