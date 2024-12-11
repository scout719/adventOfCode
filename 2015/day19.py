# -*- coding: utf-8 -*-
# pylint: disable=import-error
# pylint: disable=unused-import
# pylint: disable=wildcard-import
# pylint: disable=wrong-import-position
# pylint: disable=consider-using-enumerate
import os
from random import shuffle
import sys
from collections import defaultdict, deque
from heapq import heappop, heappush
from difflib import SequenceMatcher
from time import time


FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import read_input, main, clear  # NOQA: E402
from common.utils import day_with_validation, bcolors, WHITE_CIRCLE, WHITE_SQUARE  # NOQA: E402
from common.utils import BLUE_CIRCLE, RED_SMALL_SQUARE  # NOQA: E402
from common.utils import EXERCISE_TIMEOUT  # NOQA: E402
# pylint: enable=import-error
# pylint: enable=wrong-import-position

YEAR = 2015
DAY = 19
EXPECTED_1 = 7
EXPECTED_2 = 6


""" DAY 19 """

def day19_parse(data: list[str]):
    i = 0
    R: defaultdict[str, list[str]] = defaultdict(list)
    while i < len(data):
        line = data[i]
        if not line:
            molecule = data[i + 1]
            break
        words = line.split()
        R[words[0]].append(words[2])
        i += 1

    return R, molecule

def day19_replace(molecule: str, R: defaultdict) -> set:
    res = set()
    for k, v in R.items():
        for r in v:
            idx = []
            i = 0
            while molecule.find(k, i) != -1:
                f = molecule.find(k, i)
                idx.append(f)
                i = f + 1

            for i in idx:
                curr = molecule[:i] + r + molecule[i + len(k):]
                res.add(curr)
    return res

def day19_replace_reverse(molecule: str, R: defaultdict) -> set:
    res = set()
    items = list(R.items())
    shuffle(items)
    for k, v in items:
        for r in v:
            idx = []
            idx2 = molecule.find(r)
            while idx2 != -1:
                idx.append(idx2)
                idx2 = molecule.find(r, idx2 + 1)

            for i in idx:
                curr = molecule[:i] + k + molecule[i + len(r):]
                res.add(curr)
    return res

def day19_cost(e, molecule):
    return (-len(e))
    i = 0
    while i < len(molecule) and i < len(e):
        if molecule[i] != e[i]:
            break
        i += 1
    return (-i)
    return (-len(e), -SequenceMatcher(None, e, molecule).ratio(), -i)

def day19_1(data):
    R, molecule = day19_parse(data)
    return len(day19_replace(molecule, R))

def day19_r(R: defaultdict[str, list[str]], mem, target: str):
    if target == "e":
        return 0
    if target in mem:
        return mem[target]

    ans = 1e90
    for k, l in R.values():
        for rep in l:
            idx = target.find(rep)
            while idx != -1:
                tmp = day19_r(R, mem, target[:idx] +
                              k + target[idx + len(rep):])
                if tmp < ans:
                    ans = tmp
    mem[target] = ans
    return mem[target]

def get_bigrams(string):
    """
    Take a string and return a list of bigrams.
    """
    if string is None:
        return ""

    s = string.lower()
    return [s[i: i + 2] for i in list(range(len(s) - 1))]

def simon_similarity(str1, str2):
    """
    Perform bigram comparison between two strings
    and return a percentage match in decimal form.
    """
    pairs1 = get_bigrams(str1)
    pairs2 = get_bigrams(str2)
    union = len(pairs1) + len(pairs2)

    if union == 0 or union is None:
        return 0

    hit_count = 0
    for x in pairs1:
        for y in pairs2:
            if x == y:
                hit_count += 1
                break
    return (2.0 * hit_count) / union

def day19_cost_new(curr, target):
    from fastDamerauLevenshtein import damerauLevenshtein
    damerauLevenshtein(curr, target, similarity=True)

    return simon_similarity(curr, target)

def day19_solve2(R, mem, start, target):
    q = [(0, start)]
    seen = set()
    while q:
        steps, curr = heappop(q)
        if curr == target:
            return steps

        # if len(curr) > len(molecule):
        #     continue

        if curr in seen:
            continue
        seen.add((curr))

        for rep in day19_replace_reverse(curr, R):
            heappush(q, (steps + 1, rep))
            # q.appendleft((steps + 1, rep))
    return None

def get_pairing(molecule):
    stack: list[int] = []
    for i in range(len(molecule)):
        if molecule[i:].startswith("Rn"):
            stack.append(i)
        elif molecule[i:].startswith("Ar"):
            return stack.pop(), i
    return None

def day19_possible(R, t, mem, molecule: str, target: str):
    if target == "":
        return 0
    res = get_pairing(molecule)
    if res:
        l, r = res
        start = molecule[l + 2:r]

        ans = 1e9
        for le, trg, ri, k in t:
            tmp = day19_possible(R, t, mem, start, trg)
            if tmp:
                tmp2 = day19_possible(R, t, mem, molecule[:l], le)
                if tmp2:
                    tmp3 = day19_possible(R, t, mem, molecule[r + 2:], ri)
                    if tmp3:
                        tmp4 = day19_possible(R, t, mem, molecule[r + 2:], ri)
                        if k == target:
                            return tmp + tmp2 + tmp3
    else:
        return day19_solve2(R, mem, molecule, target)

def day19_recurse(R, steps, curr, target):
    if curr == target:
        return steps

    for rep in day19_replace_reverse(curr, R):
        tmp = day19_recurse(R, steps + 1, rep, target)
        if tmp:
            return tmp

    return None

def day19_2(data):
    R, molecule = day19_parse(data)
    # return day19_recurse(R, 0, molecule, "e")
    q = [(0, molecule)]
    while q:
        steps, curr = heappop(q)

        if curr == "e":
            return -steps

        for rep in day19_replace_reverse(curr, R):
            if rep == "e":
                return -(steps - 1)
            heappush(q, (steps - 1, rep))
    return None

    R, molecule = day19_parse(data)
    # if molecule == "HOHOHO":
    #     return day19_solve2(R, {}, molecule, "e")

    # molecule = "ORnPBPMgAr"
    # for k, lst in R.items():
    #     for rep in lst:
    #         if "Rn" in rep:
    #             target = rep[rep.find("Rn") + 2:rep.find("Ar")]
    #             ans = day19_solve2(R, {}, molecule, target)
    #             if ans:
    #                 rep[:rep.find("Rn")]
    # return

    t = []
    for k, lst in R.items():
        for rep in lst:
            idx = rep.find("Rn")
            idx2 = rep.find("Ar")
            if idx != -1:
                assert idx2 == len(rep) - 2
                t.append((rep[:idx], rep[idx + 2:idx2], rep[idx2 + 2:], k))
    print(t)
    return day19_possible(R, t, {}, molecule, "e")
    q = deque([(0, molecule)])
    mem = {}
    while q:
        ans, molecule = q.popleft()
        res = get_pairing(molecule)
        if res:
            l, r = res
            start = molecule[l + 2:r]
            for le, target, ri in t:
                tmp = day19_solve2(R, mem, start, target)
                if tmp:
                    q.append(
                        (tmp + ans, le + k + ri))
        else:
            return day19_solve2(R, mem, molecule, "e")
    return None

    pairings = []
    stack = []
    for i in range(len(molecule)):
        if molecule[i:].startswith("Rn"):
            stack.append(i)
        elif molecule[i:].startswith("Ar"):
            pairings.append((stack.pop(), i))

    for l, r in pairings:
        start = molecule[l + 2:r]
        print(start)
        for k, lst in R.items():
            for rep in lst:
                if "Rn" in rep:
                    target = rep[rep.find("Rn") + 2:rep.find("Ar")]
                    print(l, r, day19_solve2(R, {}, start, target
                                             ))

    return pairings

    idx = molecule.find("Rn")
    left = []
    while idx != -1:
        left.append(idx)
        idx = molecule.find("Rn", idx + 1)

    idx = molecule.find("Ar")
    right = []
    while idx != -1:
        right.append(idx)
        idx = molecule.find("Ar", idx + 1)
    assert len(left) == len(right)

    l, r = left[-1], right[0]

    pairings = []
    for i, pos in enumerate(left):
        pairings.append((pos, right[len(right) - 1 - i]))

    return pairings

    # assert False
    q = [(len(molecule), 0, molecule)]
    seen = set()
    start = time()
    while q:
        _, steps, target = heappop(q)
        if target == "e":
            return steps
        if target in seen:
            continue

        seen.add(target)

        if (int(time()) - int(start)
            ) % 10 == 0:
            print(len(seen), len(target))

        for rep in day19_replace_reverse(target, R):
            if rep in seen:
                continue
            heappush(q, (len(rep), steps + 1, rep))

    return day19_r(R, {}, molecule)

    q = [(day19_cost_new("e", molecule), 0, "e")]
    seen = set()
    while q:
        cost, steps, curr = heappop(q)
        if curr == molecule:
            return steps

        if len(curr) >= len(molecule):
            continue

        if curr in seen:
            continue
        seen.add((curr))

        print(len(curr), curr)
        for rep in day19_replace(curr, R):
            if rep in seen:
                continue
            heappush(q, (-day19_cost_new(rep, molecule), steps + 1, rep))
            # q.appendleft((steps + 1, rep))

    assert False


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
