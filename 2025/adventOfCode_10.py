# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
from collections import deque
import os
import sys
import z3

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2025
DAY = 10
EXPECTED_1 = 7
EXPECTED_2 = 33

def day10_parse(data: list[str]):
    machines = []
    for line in data:
        lights = set(i for i, c in enumerate(
            line.split("[")[1].split("]")[0]) if c == "#")
        buttons = []
        buttons_str = line.split("]")[1].split("{")[0].strip()
        for button in buttons_str.split(" "):
            buttons.append(set(int(l) for l in button.replace(
                "(", "").replace(")", "").split(",")))
        joltages = [int(n)
                    for n in line.split("{")[1].split("}")[0].split(",")]

        machines.append((lights, buttons, joltages))
    return machines

def day10_solve(data, part2):
    machines = day10_parse(data)

    if not part2:
        total = 0
        for lights, buttons, _ in machines:
            q = deque([(0, set())])
            while q:
                presses, on = q.popleft()
                if on == lights:
                    total += presses
                    break

                for button in buttons:
                    new_on = set(on)
                    for l in button:
                        if l in new_on:
                            new_on.remove(l)
                        else:
                            new_on.add(l)
                    q.append((presses + 1, new_on))

        return total

    total = 0
    for _, buttons, joltages in machines:
        # Use Z3 solver
        z3_solver = z3.Optimize()

        # For a machine with n buttons,
        # create n integer variables b_0, b_1, ..., b_(n-1)
        # representing how many times each button is pressed.
        buttons_vars = [z3.Int(f"b{i}") for i in range(len(buttons))]
        # Minimize the ammount of presses
        z3_solver.minimize(sum(buttons_vars))
        # Ensure positive presses only
        z3_solver.add([b >= 0 for b in buttons_vars])

        for i, joltage in enumerate(joltages):
            # Constraints for the solver:
            # We want the sum of the ammount of presses on each button,
            # that contributes to each position,
            # to be equal to the corresponding joltage.
            # Eg. If button 0 toggles lights 0, 2,
            # and button 1 toggles lights 1 and 2,
            # and the joltage requirements are [1, 0, 2],
            # then we have the following constraints:
            # b_0       = 1  (for light 0) # Only button 0 affects light 0
            #       b_1 = 0  (for light 1) # Only button 1 affects light 1
            # b_0 + b_1 = 2  (for light 2) # Both buttons affect light 2

            z3_solver.add(sum([buttons_vars[b_i] for b_i, b_pos in enumerate(
                buttons) for pos in b_pos if pos == i]) == joltage)

        assert z3_solver.check() == z3.sat

        total += sum(z3_solver.model()[b].as_long()  # type: ignore
                     for b in buttons_vars)

    return total

def day10_1(data):
    return day10_solve(data, False)

def day10_2(data):
    return day10_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
