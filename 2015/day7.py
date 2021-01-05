# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
# pylint: enable=wrong-import-position

def day7_parse(data):
    # lf AND lq -> ls
    # bo OR bu -> bv
    # iu RSHIFT 1 -> jn
    # gj LSHIFT 1 -> hc
    # NOT e -> hc
    # 123 -> x
    m = {}
    for line in data:
        left, wire = line.split(" -> ")
        if "AND" in left:
            l, r = left.split(" AND ")
            m[wire] = ("AND", l, r)
        elif "OR" in left:
            l, r = left.split(" OR ")
            m[wire] = ("OR", l, r)
        elif "RSHIFT" in left:
            w, value = left.split(" RSHIFT ")
            m[wire] = ("RSHIFT", w, int(value))
        elif "LSHIFT" in left:
            w, value = left.split(" LSHIFT ")
            m[wire] = ("LSHIFT", w, int(value))
        elif "NOT" in left:
            w = left[4:]
            m[wire] = ("NOT", w)
        else:
            if left.isnumeric():
                value = int(left)
                m[wire] = ("VALUEN", value)
            else:
                value = left
                m[wire] = ("VALUE", value)
    return m

def day7_get_value(w, m):
    if w.isnumeric():
        return int(w)
    elif w in m:
        return m[w]
    else:
        return None

def day7_solve(circuit):
    m = {}
    for w in circuit:
        op = circuit[w][0]
        if op == "VALUEN":
            m[w] = circuit[w][1]

    while 'a' not in m:
        for w in circuit:
            if w in m:
                continue
            op = circuit[w][0]
            if op == "AND":
                _, l, r = circuit[w]
                l = day7_get_value(l, m)
                r = day7_get_value(r, m)
                if not l is None and not r is None:
                    m[w] = l & r
            elif op == "OR":
                _, l, r = circuit[w]
                l = day7_get_value(l, m)
                r = day7_get_value(r, m)
                if not l is None and not r is None:
                    m[w] = l | r
            elif op == "RSHIFT":
                _, l, v = circuit[w]
                l = day7_get_value(l, m)
                if not l is None:
                    m[w] = l >> v
            elif op == "LSHIFT":
                _, l, v = circuit[w]
                l = day7_get_value(l, m)
                if not l is None:
                    m[w] = l << v
            elif op == "NOT":
                _, l = circuit[w]
                l = day7_get_value(l, m)
                if not l is None:
                    m[w] = (1 << 16) - 1 - l
            elif op == "VALUE":
                _, l = circuit[w]
                if l in m:
                    m[w] = m[l]
    return m

def day7_1(data):
    circuit = day7_parse(data)
    m = day7_solve(circuit)
    return m['a']

def day7_2(data):
    a_val = day7_1(data)
    circuit = day7_parse(data)
    circuit["b"] = ("VALUEN", a_val)
    m = day7_solve(circuit)
    return m['a']


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, globals(), 2015)
