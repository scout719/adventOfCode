# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
from collections import defaultdict, deque
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402


YEAR = 2024
DAY = 24
EXPECTED_1 = 2024
EXPECTED_2 = None

def day24_parse(data: list[str]):
    wires, gates_str = "\n".join(data).split("\n\n")
    wires = [w.split(": ") for w in wires.split("\n")]
    wires = {w: bool(int(v)) for w, v in wires}

    OPS = {
        "AND": lambda a, b: a & b,
        "OR": lambda a, b: a | b,
        "XOR": lambda a, b: a ^ b,
    }

    gates = []
    for gate in gates_str.split("\n"):
        w1, op, w2, _, w3 = gate.split(" ")
        assert op in OPS
        gates.append((w1, OPS[op], w2, w3))
    return wires, gates

def day24_get_value(wires, s):
    ans = 0
    for w in wires:
        if not w.startswith(s) or not wires[w]:
            continue

        bit = int(w.strip(s))
        v = 1
        while bit > 0:
            v = v << 1
            bit -= 1
        ans += v
    return ans

def da24_execute(wires, gates):
    q = deque(gates)
    while q:
        gate = q.popleft()
        w1, op, w2, w3 = gate
        if not (w1 in wires and w2 in wires):
            q.append(gate)
            continue

        wires[w3] = op(wires[w1], wires[w2])

    return wires

def day24_solve(data, part2):
    data = day24_parse(data)
    wires, gates = data

    if not part2:
        wires = da24_execute(wires, gates)
        ans = day24_get_value(wires, "z")
        return ans

    return day24_get_value(wires, "x"), day24_get_value(wires, "y")

def day24_1(data):
    return day24_solve(data, False)

def day24_2(data):
    return day24_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
