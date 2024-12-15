# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation, WHITE_SQUARE, BLUE_CIRCLE  # NOQA: E402

YEAR = 2024
DAY = 15
EXPECTED_1 = 10092
EXPECTED_2 = 9021

def day15_parse(data: list[str]):
    boxes = set()
    walls = set()
    robot = -1, -1
    i = 0
    while data[i]:
        for j, c in enumerate(data[i]):
            if c == "O":
                boxes.add((i, j))
            elif c == "#":
                walls.add((i, j))
            elif c == "@":
                assert robot == (-1, -1)
                robot = i, j
            else:
                assert c == "."
        i += 1
    i += 1

    moves = []
    for l in data[i:]:
        for m in l:
            M = {
                "v": (1, 0),
                "^": (-1, 0),
                ">": (0, 1),
                "<": (0, -1)}
            moves.append(M[m])
    return boxes, walls, robot, moves

def day15_print(rr, cc, boxes, walls):
    R = max(r for r, _ in walls) + 1
    C = max(c for _, c in walls) + 1
    for r in range(R):
        line = ""
        for c in range(C):
            if (r, c) in walls:
                line += WHITE_SQUARE
            elif (r, c, r, c + 1) in boxes or (r, c - 1, r, c) in boxes:
                line += BLUE_CIRCLE
            elif r == rr and c == cc:
                line += "@"
            else:
                line += " "
        print(line)
    print()

def day15_move(walls, boxes, box_width, box, dr, dc) -> tuple[bool, set[tuple[int, int, int, int]]]:
    # move box in dr,dc direction
    r, c, r2, c2 = box
    new_space = r + dr, c + dc, r2 + dr, c2 + dc

    # new_space has walls
    if (r + dr, c + dc) in walls or (r2 + dr, c2 + dc) in walls:
        return False, set()

    # box with right side blocking
    space_left = (r + dr, c + dc - (box_width - 1), r + dr, c + dc)
    # box with left side blocking
    space_right = (r2 + dr, c2 + dc, r2 + dr, c2 + dc + (box_width - 1))
    boxes_to_try_move = set()
    if new_space in boxes:
        # a box is in the space, so we need to move it as well
        assert (new_space == space_left or space_left not in boxes) and (
            new_space == space_right or space_right not in boxes)
        boxes_to_try_move.add(new_space)

    if space_left in boxes and space_left != box:
        # a box has the right side blocking, so we need to move it as well
        boxes_to_try_move.add(space_left)

    if space_right in boxes and space_right != box:
        # a box has the right side blocking, so we need to move it as well
        boxes_to_try_move.add(space_right)

    if len(boxes_to_try_move) == 0:
        return True, set([box])

    boxes_to_move: set[tuple[int, int, int, int]] = set()
    can_move = True
    for new_space in boxes_to_try_move:
        can_move_inner, boxes_should_move_inner = day15_move(
            walls, boxes, box_width, new_space, dr, dc)

        can_move &= can_move_inner
        boxes_to_move = boxes_to_move.union(boxes_should_move_inner)

    if can_move:
        return True, boxes_to_move.union([box])
    return False, set()


def day15_solve(data, part2):
    data = day15_parse(data)
    boxes, walls, robot, moves = data

    box_width = 2 if part2 else 1
    new_boxes = []
    for r, c in boxes:
        new_boxes.append(
            (r, c * box_width, r, c * box_width + (box_width - 1)))
    new_walls = set()
    for r, c in walls:
        new_walls.add((r, c * box_width))
        new_walls.add((r, c * box_width + (box_width - 1)))

    walls = new_walls
    boxes = new_boxes
    r, c = robot
    c = c * box_width
    n_boxes = len(boxes)
    for dr, dc in moves:
        rr, cc = r + dr, c + dc

        if (rr, cc) in walls:
            continue

        # TODO: This could probably be moved to the move function
        space_right = (rr, cc, rr, cc + (box_width - 1))
        space_left = (rr, cc - (box_width - 1), rr, cc)
        if space_right in boxes:
            # there is a box with the left side blocking, so we need to move it
            assert space_right == space_left or space_left not in boxes, (
                space_right, space_left, boxes)
        elif space_left in boxes:
            # there is a box with the right side blocking, so we need to move it
            assert space_right not in boxes
            space_right = space_left
        else:
            r, c = rr, cc
            continue

        moved, boxes_to_move = day15_move(
            walls, boxes, box_width, space_right, dr, dc)
        if moved:
            for box in boxes_to_move:
                b_r, b_c, b_r2, b_c2 = box
                boxes.remove((b_r, b_c, b_r2, b_c2))
                boxes.append((b_r + dr, b_c + dc, b_r2 + dr, b_c2 + dc))
            r, c = rr, cc
        assert len(boxes) == n_boxes

    ans = 0
    for r, c, b_r, b_c in boxes:
        ans += r * 100 + c
    return ans

def day15_1(data):
    return day15_solve(data, False)

def day15_2(data):
    return day15_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
