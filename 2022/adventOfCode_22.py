# -*- coding: utf-8 -*-
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable-next=wrong-import-position
from common.utils import main, day_with_validation  # NOQA: E402

YEAR = 2022
DAY = 22
EXPECTED_1 = 6032
EXPECTED_2 = 5031

""" DAY 22 """

def day22_parse(data):
    m = set()
    m = {}
    i = 0
    for r,line in enumerate(data):
        if not line:
            break
        for c, char in enumerate(line):
            if char == ".":
                m[(r,c)] = True
            elif char == "#":
                m[(r,c)] = False
    
    path = data[-1]
    path2 = []
    curr = ""
    for c in path:
        # print(c, curr)
        if c in ["R", "L"]:
            path2.append((int(curr), c))
            curr = ""
        else:
            curr += c
    path2.append((int(curr), ""))
    return (m, path2)

def day22_rotate(dr,dc, d):
    if d == "R":
        # 0, 1 -> 1,0
        # 0,-1 -> -1 ,0
        # 1,0 -> 0,-1
        # -1,0 -> 0,1
        dr,dc = dc, -dr
    elif d == "L":
        # 0, 1 -> -1,0
        # 0,-1 -> 1 ,0
        # 1,0 -> 0,1
        # -1,0 -> 0,-1
        dr,dc = -dc, dr
    return dr,dc



def day22_1(data):
    m,path = day22_parse(data)
    pos = set(k for k in m)
    R = max(r for r,c in pos)+1
    C = max(c for r,c in pos)+1
    r = min(r for r,c in pos)
    c = min(c for rr,c in pos if rr == r)
    dr, dc = (0,1)
    print(r,c,dr,dc, R,C)
    print(path[-1])
    i = 0
    for st, d in path:
        i += 1
        for _ in range(st):
            rr,cc = r+dr, c+dc
            if (rr,cc) not in pos:
                while (rr,cc) not in pos:
                    rr,cc = (rr+dr)%R, (cc+dc)%C
            if m[(rr,cc)]:
                r,c = rr,cc
        dr,dc = day22_rotate(dr,dc,d)
    

    f = 0
    if (dr,dc) == (0,1):
        f = 0
    elif (dr,dc) == (1,0):
        f = 1
    elif (dr,dc) == (0,-1):
        f = 2
    else:
        f = 3
    # 43474
    return (r+1)*1000 + (c+1)*4 + f

def day22_face(r,c, L):
    print(r,c,L)
    if 0 <= r < L:
        assert L*2 <= c < L*3
        return 1
    if L <= r < L*2:
        if 0 <= c < L:
            return 2
        elif L <= c < L*2:
            return 3
        else:
            assert L*2 <= c < L*3
            return 4
    assert L*2 <= r < L*3
    if L*2 <= c < L*3:
        return 5
    assert L*3 <= c < L*4
    return 6

def day22_2(data):
    m,path = day22_parse(data)
    pos = set(k for k in m)
    R = max(r for r,c in pos)+1
    C = max(c for r,c in pos)+1
    r = min(r for r,c in pos)
    c = min(c for rr,c in pos if rr == r)
    dr, dc = (0,1)
    print(r,c,dr,dc, R,C)
    print(path[-1])
    i = 0
    L = 50 if R > 20 else 4
    for st, d in path:
        i += 1
        for _ in range(st):
            rr,cc = r+dr, c+dc
            ddr,ddc = dr,dc
            print(rr,cc)
            if (rr,cc) not in pos:
                f = day22_face(r,c,L)
                # print(f)
                print(f, r,c, rr,cc,dr,dc)
                if f == 1:
                    if dr == -1:
                        assert rr == -1
                        rr,cc = R-1, cc
                        ddr,ddc = 1,0
                        assert day22_face(rr,cc,L) == 2
                    elif dc == -1:
                        assert cc == L*2-1
                        rr,cc = L, L + L-rr
                        ddr,ddc = 1,0
                        assert day22_face(rr,cc,L) == 3
                    else:
                        assert dc == 1 and cc == L*3
                        rr,cc = L*3-1-rr, L*4-1
                        ddr,ddc = 0,-1
                        assert day22_face(rr,cc,L) == 6
                elif f == 2:
                    if dr == -1:
                        assert rr == L-1
                        rr,cc = 0, L*2+(L-1-cc)
                        ddr,ddc = 1,0
                        assert day22_face(rr,cc,L) == 1
                    elif dc == -1:
                        assert cc == -1
                        rr,cc = rr, L*3-1
                        ddr,ddc = 0,-1
                        assert day22_face(rr,cc,L) == 6
                    else:
                        assert dr == 1 and rr == L*2
                        rr,cc = L*2-1, L*2+(L-1-cc)
                        ddr,ddc = -1 ,0
                        assert day22_face(rr,cc,L) == 5
                elif f == 3:
                    if dr == -1:
                        assert rr == L-1
                        rr,cc = cc-L, L*2
                        ddr,ddc = 0,1
                        assert day22_face(rr,cc,L) == 1
                    else:
                        assert dr == 1 and rr == L*2
                        rr,cc = L*3 - 1 - (cc-L), L*2
                        ddr,ddc = 0,1
                        assert day22_face(rr,cc,L) == 5
                elif f == 4:
                    assert dc == 1 and cc == L*3
                    rr,cc = L*2, L*4-1 - (rr-L)
                    ddr,ddc = 1,0
                    assert day22_face(rr,cc,L) == 6
                elif f == 5:
                    if dr == 1:
                        assert rr == L*3
                        rr,cc = L*2-1, L-1-(cc-L*2)
                        ddr,ddc = -1,0
                        assert day22_face(rr,cc,L) == 2
                    else:
                        assert dc == -1 and cc == L*2-1
                        rr,cc = L*2-1, L + (rr-L*2)
                        ddr,ddc = -1,0
                        assert day22_face(rr,cc,L) == 3
                else:
                    assert f == 6
                    if dr == 1:
                        assert rr == L*3
                        rr,cc = L*2-1-(cc-L*3), 0
                        ddr,ddc = 0, 1
                        assert day22_face(rr,cc,L) == 2
                    elif dr == -1:
                        assert rr == L*2-1
                        rr,cc = L*2-1-(cc-L*3), L*3-1
                        ddr,ddc = 0,-1
                        assert day22_face(rr,cc,L) == 4
                    else:
                        # print(r,c, rr,cc ,dr,dc,f)
                        assert dc == 1 and cc == L*4
                        rr,cc = L*3-1-rr,L*3-1
                        ddr,ddc = 0,-1
                        assert day22_face(rr,cc,L) == 1
                print(rr,cc)
                assert (rr,cc) in pos, (rr,cc)


                # while (rr,cc) not in pos:
                #     rr,cc = rr+dr,cc+dc

            if m[(rr,cc)]:
                r,c = rr,cc
                dr,dc = ddr,ddc
        dr,dc = day22_rotate(dr,dc,d)
    

    f = 0
    if (dr,dc) == (0,1):
        f = 0
    elif (dr,dc) == (1,0):
        f = 1
    elif (dr,dc) == (0,-1):
        f = 2
    else:
        f = 3
    # 43474
    return (r+1)*1000 + (c+1)*4 + f


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
