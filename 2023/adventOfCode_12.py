# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
import os
import sys
from typing import List, Mapping, Tuple, Union

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import day_with_validation  # NOQA: E402
from common.utils import main  # NOQA: E402

YEAR = 2023
DAY = 12
EXPECTED_1 = 21
EXPECTED_2 = 525152


""" DAY 12 """

def day12_parse(data: List[str]):
    rows = []
    for line in data:
        springs, sizes = line.split(" ")
        sizes = [int(x) for x in sizes.split(",")]
        rows.append([springs, sizes])
    return rows

def day12_valid(springs: str, sizes, strict: bool = False):
    groups = springs.split(".")
    lens = [len(g) for g in groups if g]
    if strict:
        return lens == sizes
    if len(lens) > len(sizes):
        return False
    # compare last sizes
    # print(sizes, lens)
    valid = True
    if len(lens) > 1:
        valid = lens[1:] == sizes[-(len(lens) - 1):]
    if len(lens) > 0:
        # first should be less or equal
        valid &= lens[0] <= sizes[-len(lens)]
    return valid

def day12_final(sizes, springs, mem):
    if not sizes:
        return 1 if all(c == "." or c == "?" for c in springs) else 0

    if not springs:
        return 0

    k = (tuple(sizes), springs)
    if k in mem:
        return mem[k]

    ans = 0
    c = springs[0]
    if c in [".", "?"]:
        # Just skip  this
        ans += day12_final(sizes, springs[1:], mem)
        
    
    if c in ["#", "?"]:
        # consume all current
        s = sizes[0]
        if len(springs) >= s:
            if all(c2 in ["#", "?"] for c2 in springs[:s]):
                springs = springs[s:]
                if springs:
                    if springs[0] in [".", "?"]:
                        ans += day12_final(sizes[1:], springs[1:], mem)
                    else:
                        # can't consume
                        pass
                else:
                    # not enough to consume (we added an extra . to all to handle this)
                    pass
            else:
                # not valid
                pass
        else:
            # not enough
            pass
    mem[k] = ans
    return ans



def day12_x(sizes, springs, consume: bool):
    # c = springs[0]
    # n_springs = springs[1:]
    # chars = [".", "#"] if c == "?" else [c]
    # ans = 0
    # for c in chars:
    #     if c == "#":
    #         if not sizes or sizes[0] < 1:
    #             continue
    #         new_c = sizes[0] - 1
    #         if new_c == 0:
    #             new_sz = sizes[1:]
    #             if not new_sz:
    #                 ans += 1 if all(c == "." or c ==
    #                                 "?" for c in n_springs) else 0
    #                 continue
    #             if not n_springs or n_springs[0] == "#":
    #                 continue
    #             # consume one .
    #             n_springs = n_springs[1:]
    #             if not n_springs:
    #                 continue
    #             ans += day12_x(new_sz, n_springs)
    #         else:
    #             if not n_springs:
    #                 continue
    #             ans += day12_x([new_c] + sizes[1:], n_springs)
    #     elif c == ".":
    #         if consume:
    #             continue
    #         if not n_springs:
    #             continue
    #         ans += day12_x(sizes, n_springs, consume)
    # return ans

    if not sizes:
        return 1 if all(c == "." or c == "?" for c in springs) else 0

    assert len(sizes) > 0
    assert springs

    springs = springs.lstrip(".")

    c = springs[0]
    chars = [".", "#"] if c == "?" else [c]
    ans = 0
    for c in chars:
        count = sizes[0]
        while count > 0:
            # consume #
            if not springs:
                return 0
            c = springs[0]
            springs = springs[1:]
            if c == ".":
                return 0
            count -= 1

        if len(sizes) == 1:
            return 1 if all(c == "." or c == "?" for c in springs) else 0

        # consume a .
        springs = springs[1:]

        if not springs:
            return 0

        c = springs[0]
        if c == "#":
            return day12_x(sizes[1:], springs)
        else:
            assert c == "?"
            # consume as #
            return day12_x(sizes[1:], springs) + \
                day12_x(sizes[1:], springs[1:])

def day12_x2(sizes, springs, consume: bool):
    if not sizes:
        return 1 if all(c == "." or c == "?" for c in springs) else 0

    count = sizes[0]
    while count > 0:
        # consume #
        if not springs:
            return 0
        c = springs[0]
        springs = springs[1:]
        if c == ".":
            return 0
        count -= 1

    if len(sizes) == 1:
        return 1 if all(c == "." or c == "?" for c in springs) else 0

    # consume a .
    springs = springs[1:]

    if not springs:
        return 0

    while springs[0] == ".":
        # consume .
        springs = springs[1:]

    c = springs[0]
    if c == "#":
        return day12_x(sizes[1:], springs)
    else:
        assert c == "?"
        # consume as #
        return day12_x(sizes[1:], springs) + \
            day12_x(sizes[1:], springs[1:])

    if not springs:
        return 0

    c = springs[0]

    if c == "#":
        c = sizes[0] - 1
        new_springs = springs[1:]
        if c == 0:
            if not new_springs:
                # end of springs
                return 1 if len(sizes) == 1 else 0
            if new_springs[0] == "#":
                return 0
            # consume a "."
            assert new_springs[0] in ["?", "."]
            # consume a "."
            return day12_x(sizes[1:], new_springs[1:])
    elif c == ".":
        # just consume it
        return day12_x(sizes, springs[1:])

    if len(sizes) == 1:
        if sizes[0] == 0:
            return 1 if all(c == "." or c == "?" for c in springs) else 0
        if springs[0] == ".":
            return 0

    if springs[0] == "#":
        pass
    if sizes[0] == 0:
        if springs[0] == "#":
            return 0
        elif springs[0] == ".":
            pass
    if s == 0:
        pass

    if not springs:
        return 0


def day12_generate_orig(springs, sizes, mem):
    if not springs:
        return 0

    assert sizes[0] > 0
    s = springs[0]

    chars = [s] if s != "?" else ["#", "."]
    ans = 0
    for c in chars:
        if c == "#":

            sz = sizes[:]
            if springs[1] == ".":
                if sz[0] != 1:
                    continue
                sz = sz[1:]
            else:
                sz[0] -= 1
                if sz[0] == 0:
                    continue

            ans += day12_generate_orig(springs[1:], sz, mem)
        else:
            assert c == "."
            ans += day12_generate_orig(springs[1:], sizes, mem)
    print(springs, sizes, ans)
    return ans

# leftmost group, nr of combinations
def day12_generate(springs: str, sizes, mem) -> Tuple[int, int]:
    s = springs[0]
    if len(springs) == 1:
        if s == "#":
            return (1, 1) if len(sizes) == 1 and sizes[0] == 1 else (1, 0)
        elif s == ".":
            return (0, 1) if len(sizes) == 0 or (len(sizes) == 1 and sizes[0] == 0) else (0, 0)
        elif s == "?":
            if len(sizes) == 0 or (len(sizes) == 1 and sizes[0] == 0):
                return (0, 1)
            elif sizes[0] == 1:
                return (1, 1)
            else:
                return (0, 0)

    if len(sizes) == 0:
        return (0, 1) if all(c == "." or c == "?" for c in springs) else (0, 0)

    assert len(sizes) > 0, f"springs={springs} sizes={sizes}"

    ans = 0
    chars = [s] if s != "?" else ["#", "."]
    for c in chars:
        if c == "#":
            sz = sizes[:]
            if sz[0] == 0:
                continue
            sz[0] -= 1

            left, ans2 = day12_generate(springs[1:], sz, mem)
            ans += ans2
        else:
            assert c == "."
            sz = sizes[:]
            if sz[0] != 0:
                continue
            sz = sz[1:]

            left, ans2 = day12_generate(springs.lstrip("."), sz, mem)
            ans += ans2

    return (0, ans)

    if not springs:
        return 0

    assert sizes[0] > 0
    s = springs[0]

    chars = [s] if s != "?" else ["#", "."]
    ans = 0
    for c in chars:
        if c == "#":

            sz = sizes[:]
            if springs[1] == ".":
                if sz[0] != 1:
                    continue
                sz = sz[1:]
            else:
                sz[0] -= 1
                if sz[0] == 0:
                    continue

            ans += day12_generate(springs[1:], sz, mem)
        else:
            assert c == "."
            ans += day12_generate(springs[1:], sizes, mem)
    print(springs, sizes, ans)
    return ans

def day12_generate2(springs, sizes, mem):
    if len(springs) == 1:
        return ["#", "."] if springs == "?" else [springs]

    k = (springs, tuple(sizes))
    # k = springs
    if k in mem:
        return mem[k]
    candidates = day12_generate2(springs[1:], sizes, mem)
    # if s != "?":
    #     candidates = [
    #         s + rest for rest in ]
    # else:
    #     rests = day12_generate(springs[1:], sizes, mem)
    #     candidates = ["#" + rest for rest in rests] + \
    #         ["." + rest for rest in rests]
    ans = []
    s = springs[0]
    for candidate in candidates:

        new_s = candidate.replace("..", ".")
        while candidate != new_s:
            candidate = new_s
            new_s = new_s.replace("..", ".")

        chars = [s] if s != "?" else ["#", "."]
        for c in chars:
            # sz = sizes if (c == "#") and (candidate[0] == ".") else sizes[1:]
            # print(c + candidate, sz)
            if day12_valid(c + candidate, sizes):
                ans.append(c + candidate)
    mem[k] = ans
    return ans

def day12_generate4(springs: str, sizes) -> List[str]:
    c = springs[0]
    if len(springs) == 1:
        if len(sizes) == 1:
            if sizes[0] == 1:
                if c == "?" or c == "#":
                    return ["#"]
                else:
                    return []
            elif sizes[0] == 0:
                if c == "?" or c == ".":
                    return ["."]
        elif len(sizes) > 1:
            return []
        else:
            return ["."] if c == "." or c == "?" else []
    g: List[str] = []
    chars = ["#", "."] if c == "?" else [c]
    for c in chars:
        if c == "#":
            if not sizes or sizes[0] == 0:
                continue
            g += ["#" +
                  g2 for g2 in day12_generate4(springs[1:], [sizes[0] - 1] + sizes[1:])]
        elif c == ".":
            if sizes and sizes[0] == 0:
                g += ["." +
                      g2 for g2 in day12_generate4(springs[1:], sizes[1:])]
            else:
                g += ["." + g2 for g2 in day12_generate4(springs[1:], sizes)]

    return g

def day12_generate5(springs):
    c = springs[0]
    if len(springs) == 1:
        return [".", "#"] if c == "?" else [c]
    if c == "#" or c == ".":
        return day12_generate5(springs[1:])
    else:
        assert c == "?"
        rest = day12_generate5(springs[1:])
        return ["#" + r for r in rest] + ["." + r for r in rest]

def day12_generate3(i, springs, sizes, mem, consume):
    if not springs:
        if not sizes:
            return 1
        elif len(sizes) == 1 and sizes[0] == 0:
            return 1
        else:
            return 0
    c = springs[0]
    if c == "#":
        if not sizes or sizes[0] < 1:
            return 0
        else:
            return day12_generate3(i + 1, springs[1:], [sizes[0] - 1] + sizes[1:], mem, consume)
    if sizes and sizes[0] == 0:
        if c == "#":
            return 0
        else:
            return day12_generate3(i + 1, springs[1:], sizes[1:], mem)

    if not sizes:
        return day12_generate3(i + 1, springs[1:], sizes, mem)

    # c == . or c == ? and sizes[0] > 0
    if c == ".":
        return 0  # sizes[0] > 0

    return day12_generate3(i + 1, springs[1:], sizes, mem) + \
        day12_generate3(i + 1, springs[1:], [sizes[0] - 1] + sizes[1:], mem)

    if len(springs) == 1:
        return ["#", "."] if springs == "?" else [springs]

    k = (springs, tuple(sizes))
    # k = springs
    # if k in mem:
    # return mem[k]
    candidates = day12_generate2(springs[1:], sizes, mem)
    # if s != "?":
    #     candidates = [
    #         s + rest for rest in ]
    # else:
    #     rests = day12_generate(springs[1:], sizes, mem)
    #     candidates = ["#" + rest for rest in rests] + \
    #         ["." + rest for rest in rests]
    ans = []
    s = springs[0]
    for candidate in candidates:
        chars = [s] if s != "?" else ["#", "."]
        for c in chars:
            sz = sizes if (c == "#") and (candidate[0] == ".") else sizes[1:]
            print(c + candidate, sz)
            if day12_valid(c + candidate, sz):
                ans.append(c + candidate)
    # mem[k] = ans
    return ans

def day12_t(springs:str, sizes: List[int], consume:bool):
    if consume:
        s = sizes[0]
        while s > 0:
            if not springs or springs[0] == ".":
                return 0
            springs = springs[1:]
            s-=1
        
        return day12_t(springs, [0] + sizes[1:], False)
    else:
        if sizes[0] != 0:
            return 0
        if not springs:
            return 1 if not sizes or (len(sizes) == 1 and sizes[0] == 0) else 0
        print(springs, sizes)
        c = springs[0]
        if c == "#":
            return 0
        else:
            return day12_t(springs[1:], sizes, False) + day12_t(springs[1:], sizes[1:], True) 

    c = springs[0]
    if c == "#":
        if not consume:
            return 0
        if sizes[0] == 0:
            return 0
        else:
            return day12_t(springs[1:], [sizes[0]-1] + sizes[1:], sizes[0]-1 > 0)
    elif c == ".":
        if consume:
            return 0


    if consume:

        if not springs:
            return 0
        c = springs[0]
        if c == ".":
            return 0
        else:
            if sizes[0] == 0:
                return 0
            else:
                return day12_t(springs[1:], [sizes[0]-1] + sizes[1:], sizes[0]-1 > 0)
    else:
        if not springs:
            return 1 if not sizes or sizes == [0] else 0
        c = springs[0]
        if c == "#":
            return 0
        elif c == ".":
            return day12_t(springs[1:], sizes, sizes[0]-1 > 0)



def day12_solve(rows: List[Tuple[str, List[int]]]):
    ans = 0
    mem = {}
    for springs, sizes in rows:
        # s = springs.strip(".")
        # new_s = s.replace("..", ".")
        # while s != new_s:
        #     s = new_s
        #     new_s = new_s.replace("..", ".")

        # ans2 = day12_t(new_s, sizes, True)
        # ans += ans2
        # print(springs, ans2)
        ans += day12_final(sizes, springs + ".", mem)
        continue

        gen = day12_generate2(new_s, sizes, mem)
        # for a in ans2:
        # print(a)
        # print(springs, len(ans2))
        # # print(len(gen))
        # ans += ans2
        # # print(gen)
        for s in gen:
            assert "?" not in gen, gen
            # print(s, sizes, day12_valid(s, sizes, strict=True))
            # print(s)
            if day12_valid(s, sizes, strict=True):
                ans += 1

        # assert day12_valid(springs, sizes), f"springs={springs} sizes={sizes}"
    return ans

def day12_1(data: List[str]):
    rows = day12_parse(data)
    return day12_solve(rows)

def day12_2(data: List[str]):
    rows = day12_parse(data)
    for i, row in enumerate(rows):
        rows[i][0] = (row[0] + "?") * 4 + row[0]
        rows[i][1] = row[1] * 5
    # print(rows)
    return day12_solve(rows)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
