# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
from collections import defaultdict, deque
from copy import deepcopy
import functools
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2024
DAY = 24
EXPECTED_1 = None
EXPECTED_2 = None

def day24_parse(data: list[str]):
    wires, gates_str = "\n".join(data).split("\n\n")
    wires = [w.split(": ") for w in wires.split("\n")]
    wires = {w: bool(int(v)) for w, v in wires}

    gates: set[tuple[str, str, str, str]] = set()
    for gate in gates_str.split("\n"):
        w1, op, w2, _, w3 = gate.split(" ")
        gates.add((w1, op, w2, w3))
    return wires, gates

def day24_get_value(wires, s):
    ans = 0
    for w in wires:
        if not w.startswith(s) or not wires[w]:
            continue

        bit = int(w.strip(s))
        value = 1
        while bit > 0:
            value = value << 1
            bit -= 1
        ans += value
    return ans

def day24_execute(wires, gates):
    OPS = {
        "AND": lambda a, b: a & b,
        "OR": lambda a, b: a | b,
        "XOR": lambda a, b: a ^ b,
    }
    wires_gates = defaultdict(list)
    for gate in gates:
        l, _, r, _ = gate
        wires_gates[l].append(gate)
        wires_gates[r].append(gate)

    ready = set()
    for wire in wires:
        for gate in wires_gates[wire]:
            l, _, r, _ = gate
            if l in wires and r in wires:
                ready.add(gate)

    q = deque(ready)
    seen = set()
    while q:
        gate = q.popleft()
        l, op, r, o = gate
        assert l in wires and r in wires
        if gate in seen:
            return None
        seen.add(gate)

        if o in wires:
            return None

        assert op in OPS
        wires[o] = OPS[op](wires[l], wires[r])

        for gate2 in wires_gates[o]:
            a, _, b, _ = gate2
            if a in wires and b in wires:
                q.append(gate2)

def day24_find_gate_by_op(l, op, r, gates) -> str | None:
    for gate in gates:
        ll, opp, rr, o = gate
        if op == opp:
            if (l == ll and r == rr) or (l == rr and r == ll):
                return o
    return None

def day24_find_gate_by_out(out, gates) -> tuple[str, str, str, str]:
    for gate in gates:
        _, _, _, o = gate
        if o == out:
            return gate
    assert False

def day24_swap(a, b, gates: set[tuple[str, str, str, str]]):
    gate_a = day24_find_gate_by_out(a, gates)
    gate_b = day24_find_gate_by_out(b, gates)
    l_a, op_a, r_a, o_a = gate_a
    l_b, op_b, r_b, o_b = gate_b
    gates.remove(gate_a)
    gates.remove(gate_b)
    gates.add((l_a, op_a, r_a, o_b))
    gates.add((l_b, op_b, r_b, o_a))

def day24_process_adder(bit, Cin, gates: set[tuple[str, str, str, str]]):
    # Sout = Cin XOR (x XOR y)
    # Cout = ((x XOR y) AND Cin) OR (x AND y)

    # a = x XOR y
    # b = x AND y
    # c = a AND Cin
    # Cout = c OR b
    # SOut = Cin XOR a

    x = f"x{bit:02d}"
    y = f"y{bit:02d}"
    z = f"z{bit:02d}"
    swapped = set()
    a = day24_find_gate_by_op(x, "XOR", y, gates)
    assert a is not None and not a.startswith("z")
    Sout = day24_find_gate_by_op(a, "XOR", Cin, gates)
    if Sout is None:
        # We couldn't find the XOR for the Sout,
        # so we need to find the right XOR to swap with a
        gate = day24_find_gate_by_out(z, gates)
        l, _, r, _ = gate
        to_swap = l
        if l == Cin:
            to_swap = r
        day24_swap(to_swap, a, gates)
        swapped.add(to_swap)
        swapped.add(a)
        a = to_swap
    elif Sout != z:
        # We found the right gate but it didn't write to the Out
        # So find the gate that has the target Out and swap them
        day24_swap(z, Sout, gates)
        swapped.add(z)
        swapped.add(Sout)
    b = day24_find_gate_by_op(x, "AND", y, gates)
    assert b is not None and not b.startswith("z")
    c = day24_find_gate_by_op(a, "AND", Cin, gates)
    assert c is not None and not c.startswith("z")
    Cout = day24_find_gate_by_op(c, "OR", b, gates)
    return Cout, swapped

def day24_solve(data, part2):
    data = day24_parse(data)
    wires, gates = data

    if not part2:
        day24_execute(wires, gates)
        ans = day24_get_value(wires, "z")
        return ans

    # Find first adder Cin
    x0 = "x00"
    y0 = "y00"
    Cin = None
    for l, op, r, o in gates:
        if l == x0 and op == "AND" and r == y0:
            Cin = o
            break

    swapped = set()
    max_b = int(sorted(wires)[-1].strip("y"))
    for b in range(1, max_b + 1):
        Cout, swapped2 = day24_process_adder(b, Cin, gates)
        swapped |= swapped2
        Cin = Cout

    # Ensure original sum works
    day24_execute(wires, gates)

    x, y, z = day24_get_value(wires, "x"), day24_get_value(
        wires, "y"), day24_get_value(wires, "z")

    assert x + y == z
    return ",".join(sorted(swapped))

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
