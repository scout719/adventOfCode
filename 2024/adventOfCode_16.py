# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
from ast import Not
from collections import deque
from heapq import heappop, heappush
import os
import sys
from time import sleep

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import RED_SMALL_SQUARE, main  # NOQA: E402
from common.utils import day_with_validation, WHITE_SQUARE, BLUE_CIRCLE  # NOQA: E402


YEAR = 2024
DAY = 16
EXPECTED_1 = 11048  # 7036
EXPECTED_2 = 64  # 45

def day16_parse(data: list[str]):
    return data

def day16_print(rr, cc, walls, path):
    R = max(r for r, _ in walls) + 1
    C = max(c for _, c in walls) + 1
    show = ""
    for r in range(R):
        line = ""
        for c in range(C):
            if (r, c) in walls:
                line += WHITE_SQUARE
            elif r == rr and c == cc:
                line += RED_SMALL_SQUARE
            elif (r, c) in path:
                line += BLUE_CIRCLE
            else:
                line += " "
        show += line + "\n"
    print(show)
    sys.stdout.flush()

def day16_solve2(DP, walls, score, er, ec, r, c, dr, dc, path):
    ROT = {
        (0, -1): [(1, 0), (-1, 0)],
        (0, 1): [(1, 0), (-1, 0)],
        (-1, 0): [(0, 1), (0, -1)],
        (1, 0): [(0, 1), (0, -1)],
    }

    if score > DP["best"]:
        return 1e9, set()

    # print(score)
    # print(abs(er - r) + abs(ec - c), score)
    if (len(DP) > 1):
        print(len(DP))

    key = (r, c, dr, dc)
    if key in DP:
        if DP[key][0] <= score:
            return DP[key]

    if (r, c) == (er, ec):
        # print(sorted({(r, c) for r, c, _, _ in path}))
        return score, {(r, c) for r, c in path}.union({(r, c)})

    if (r, c) in path:
        return 1e9, set()

    path = path.union({(r, c)})

    rr, cc = r + dr, c + dc
    best_score = 1e9
    tiles = set()
    if (rr, cc) not in walls:
        best_score, tiles = day16_solve2(DP,
                                         walls, score + 1, er, ec, rr, cc, dr, dc, path.union(set()))
        # if (rr,cc) == (er,ec):
        #     print("HERE")
        #     print(ec, er ,r,c, rr,cc,dr,dc,best_score, tiles)

        # if best_score != 1e9:
        #     best_score += 1
        #     # print(ec, er ,r,c, rr,cc,dr,dc,best_score, tiles)
    # DP[key] = (best_score, tiles)
    for drr, dcc in ROT[(dr, dc)]:
        rrr, ccc = r + drr, c + dcc
        if (rrr, ccc) in walls:
            continue
        best_score2, tiles2 = day16_solve2(DP,
                                           walls, score + 1001, er, ec, rrr, ccc, drr, dcc, path.union(set()))
        if best_score2 == 1e9:
            continue
        # best_score2 += 1000
        if best_score2 < best_score:
            best_score = best_score2
            tiles = tiles2
        elif best_score2 == best_score:
            tiles = tiles.union(tiles2)
    if best_score != 1e9:
        DP[key] = (best_score, tiles)
    return best_score, tiles

def day16_quickest(walls, score, er, ec, r, c, dr, dc):
    q = [(score, er, ec, 0, 1), (score, er, ec, 0, -1),
         (score, er, ec, -1, 0), (score, er, ec, 1, 0)]

    ROT = {
        (0, -1): [(1, 0), (-1, 0)],
        (0, 1): [(1, 0), (-1, 0)],
        (-1, 0): [(0, 1), (0, -1)],
        (1, 0): [(0, 1), (0, -1)],
    }
    seen = {}
    count = 0
    while q:
        score_left, rr, cc, drr, dcc = q.pop(0)

        key = (rr, cc, drr, dcc)
        if key in seen and seen[key] > score_left:
            continue

        if score_left < 0:
            continue

        seen[key] = score_left
        if (rr, cc, drr, dcc) == (r, c, dr, dc):
            assert score_left == 0
            count += 1

        rrr, ccc = rr + drr, cc + dcc
        if (rrr, ccc) not in walls:
            q.append((score_left - 1, rrr, ccc, drr, dcc))

        for drrr, dccc in ROT[(drr, dcc)]:
            # rrrr, cccc = rr + drrr, cc + dccc
            q.append((score_left - 1000, rr, cc, drrr, dccc))
    return count

def day16_search(DP, ROT, walls, er, ec, size2, left, r, c, dr, dc, path: set[tuple[int, int]], visited, v2):
    if left < 0:
        return False, 1e9

    # if len(path) + abs(er - r) + abs(ec - c) > size2:
    #     return False, 1e9

    if (r, c) == (er, ec):
        visited.add((r, c))
        return True, 0

    if (r, c) in walls:
        return False, 1e9

    if (r, c) in path:
        return False, 1e9

    if (r, c, dr, dc) in DP:
        # if left == DP[(r, c, dr, dc)]:
        #     return True, left
        # assert DP[(r, c, dr, dc)] == 1e9 or DP[(r, c, dr, dc)] == left, (r, c, left,
        #                                                                  DP[(r, c, dr, dc)], DP)
        return DP[(r, c, dr, dc)] != 1e9, DP[(r, c, dr, dc)]
        # if DP[(r, c, dr, dc)] + score == target:
        #     # visited.add((r, c))
        # else:
        #     return True, 1e9
    # sleep(.1)
    # day16_print(r, c, walls, path)

    path.add((r, c))
    rr, cc = r + dr, c + dc

    succ = []
    if (rr, cc) not in path:
        succ.append((rr, cc, dr, dc, 1))

    for drr, dcc in ROT[(dr, dc)]:
        rrr, ccc = r + drr, c + dcc
        if (rrr, ccc) not in path:
            succ.append((rrr, ccc, drr, dcc, 1001))

    possible = False

    min_res = 1e9
    for rr, cc, drr, dcc, cost in succ:
        res, res2 = day16_search(DP, ROT, walls, er, ec, size2,
                                 left - cost, rr, cc, drr, dcc, path, visited, v2)
        possible |= res
        min_res = min(min_res, res2 + cost)

    if min_res == left:
        # DP[(r, c, dr, dc)] = min_res
        visited.add((r, c))
    else:
        possible = False
        min_res = 1e9
    path.remove((r, c))
    # print(len(DP))
    return possible, min_res

def day16_search2(DP, ROT, walls, er, ec, size2, left, r, c, dr, dc, path: set[tuple[int, int]], visited, v2):
    dist = {}

    # if left < 0:
    #     return None, 1e9
    print(r, c, dr, dc)
    G = {(r, c, dr, dc): 0}
    H = {(r, c, dr, dc): abs(er - r) + abs(ec - c)}
    F = {(r, c, dr, dc): G[(r, c, dr, dc)] + H[(r, c, dr, dc)]}
    P = {}
    open_list = [(F[(r, c, dr, dc)], r, c, dr, dc)]
    closed_list = set()

    nodes = set()

    while open_list:
        f, r, c, dr, dc = heappop(open_list)
        if (r, c) == (er, ec):
            print("hehe")
            path.add((r, c))
            p = (r, c)
            while p in P:
                path.add(p)
                p = P[p]
            continue

        closed_list.add((r, c, dr, dc))

        succ = []
        rr, cc = r + dr, c + dc
        if (rr, cc) not in walls:
            succ.append((rr, cc, dr, dc, 1))

        for drr, dcc in ROT[(dr, dc)]:
            rr, cc = r + drr, c + dcc
            if (rr, cc) not in walls:
                succ.append((rr, cc, drr, dcc, 1001))

        for rr, cc, drr, dcc, cost in succ:
            if (rr, cc, drr, dcc) in closed_list:
                continue
            tentative = G[(r, c, dr, dc)] + cost
            if tentative > left:
                continue
            if (rr, cc, drr, dcc) in G and tentative > G[(rr, cc, drr, dcc)]:
                # this is not better
                continue

            P[(rr, cc, dr, dc)] = (r, c, dr, dc)
            G[(rr, cc, drr, dcc)] = tentative
            H[(rr, cc, drr, dcc)] = abs(er - rr) + abs(ec - cc)
            F[(rr, cc, drr, dcc)] = G[(rr, cc, drr, dcc)] + H[(rr, cc, drr, dcc)]
            heappush(open_list, (F[(rr, cc, drr, dcc)], rr, cc, drr, dcc))

    return True
    if (len(path) > size2 + 10):
        return None, 1e9

    # if len(path) + abs(er - r) + abs(ec - c) > size2:
    #     return False, 1e9

    if (r, c) == (er, ec):
        visited.add((r, c, dr, dc))
        return True, 0

    if (r, c) in walls:
        return False, 1e9

    if (r, c) in path:
        return None, 1e9

    if (r, c, dr, dc) in DP:
        # if left == DP[(r, c, dr, dc)]:
        #     return True, left
        # assert DP[(r, c, dr, dc)] == 1e9 or DP[(r, c, dr, dc)] == left, (r, c, left,
        #                                                                  DP[(r, c, dr, dc)], DP)
        return DP[(r, c, dr, dc)] == 1e9, DP[(r, c, dr, dc)]
        # if DP[(r, c, dr, dc)] + score == target:
        #     # visited.add((r, c))
        # else:
        #     return True, 1e9
    sleep(.1)
    day16_print(r, c, walls, path)

    path.add((r, c))
    rr, cc = r + dr, c + dc

    succ = []
    if (rr, cc) not in path:
        succ.append((rr, cc, dr, dc, 1))

    for drr, dcc in ROT[(dr, dc)]:
        rrr, ccc = r + drr, c + dcc
        if (rrr, ccc) not in path:
            succ.append((rrr, ccc, drr, dcc, 1001))

    possible = False

    min_res = 1e9
    some_none = False
    for rr, cc, drr, dcc, cost in succ:
        res, res2 = day16_search2(DP, ROT, walls, er, ec, size2,
                                  left - cost, rr, cc, drr, dcc, path, visited, v2)
        if res:
            possible |= res
            min_res = min(min_res, res2 + cost)
        else:
            some_none = True

    if not possible and not some_none:
        DP[(r, c, dr, dc)] = 1e9
    elif possible and min_res == left:
        # assert min_res == left
        DP[(r, c, dr, dc)] = min_res
        visited.add((r, c))
    path.remove((r, c))
    # print(len(DP))
    return possible, min_res

def day16_solve(data, part2):
    data = day16_parse(data)
    grid = data
    R = len(grid)
    C = len(grid[0])
    ir, ic = 0, 0
    er, ec = 0, 0
    walls = set()
    for r in range(R):
        for c in range(C):
            if grid[r][c] == "S":
                ir, ic = r, c
            elif grid[r][c] == "E":
                er, ec = r, c
            elif grid[r][c] == "#":
                walls.add((r, c))
            else:
                assert grid[r][c] == "."

    ROT = {
        (0, -1): [(1, 0), (-1, 0)],
        (0, 1): [(1, 0), (-1, 0)],
        (-1, 0): [(0, 1), (0, -1)],
        (1, 0): [(0, 1), (0, -1)],
    }

    DP = {"best": 1e9}
    q = [(abs(ir - er) + abs(ic - ec), 0, ir, ic, 0, 1, 0)]
    seen = set()
    size2 = 0
    tiles = set()
    while q:
        cost, score, r, c, dr, dc, size = heappop(q)
        if (r, c, dr, dc) in seen:
            continue
        seen.add((r, c, dr, dc))

        if (r, c) == (er, ec):
            if not part2:
                return score
            DP["best"] = score
            size2 = size + 1
            break

        rr, cc = r + dr, c + dc
        if (rr, cc) not in walls:
            heappush(q, (abs(er - rr) + abs(ec - cc) +
                     score + 1, score + 1, rr, cc, dr, dc, size + 1))

        for drr, dcc in ROT[(dr, dc)]:
            rrr, ccc = r + drr, c + dcc
            if (rrr, ccc) in walls:
                continue
            heappush(q, (abs(er - rrr) + abs(ec - ccc) + score + 1001, score + 1001,
                     rrr, ccc, drr, dcc, size))
    if not part2:
        return DP["best"]

    B = {}
    P = {}

    q = [(abs(er - ir) + abs(ec - ic), 0, ir, ic, 0, 1, set())]
    bests = []
    nodes = set()
    best = 1e9
    while q:
        cost, score, r, c, dr, dc, path = heappop(q)
        key = (r, c, dr, dc)
        if key in B and B[key] < score:
            continue
        B[key] = score

        if (r, c) == (er, ec):
            if best == 1e9:
                best = score
            elif score > best:
                continue
            # print(score)
            nodes |= path
            continue

        rr, cc = r + dr, c + dc
        if (rr, cc) not in walls:
            # key2 = (rr, cc, dr, dc)
            # if key2 not in B or B[key2] > score + 1:
            #     P[key2] = [key]
            # elif B[key2] == score + 1:
            #     P[key2].append(key)
            heappush(q, (abs(er - rr) + abs(ec - cc) +
                     score + 1, score + 1, rr, cc, dr, dc, path | {(r, c)}))

        for drr, dcc in ROT[(dr, dc)]:
            rrr, ccc = r + drr, c + dcc
            if (rrr, ccc) in walls:
                continue
            # key2 = (rrr, ccc, drr, dcc)
            # if key2 not in B or B[key2] > score + 1001:
            #     P[key2] = [key]
            # elif B[key2] == score + 1001:
            #     P[key2].append(key)
            heappush(q, (abs(er - rrr) + abs(ec - ccc) + score + 1001, score + 1001,
                     rrr, ccc, drr, dcc, path | {(r, c)}))

    # nodes = set()
    # print(P[bests[0]])
    # print(P)
    # for (r, c, dr, dc) in bests:
    #     nodes.add((r, c))
    #     q: list[tuple[int, int, int, int]] = [] + P[(r, c, dr, dc)]
    #     while q:
    #         r, c, dr, dc = q.pop()
    #         nodes.add((r, c))
    #         if (r, c, dr, dc) in P:
    #             for rr, cc, drr, dcc in P[(r, c, dr, dc)]:
    #                 q.append((rr, cc, drr, dcc))
    #         # r, c, dr, dc = P[(r, c, dr, dc)]

    return len(nodes)+1

    s = set()
    day16_search2({}, ROT, walls, er, ec, size2,
                  DP["best"], ir, ic, 0, 1, set(), s, set())
    return len(s)
    DP = {"best": 1e9}
    best = DP["best"]
    q = [(abs(ir - er) + abs(ic - ec), 0, ir, ic, 0, 1, 0)]
    seen = set()
    size2 = 0
    tiles = set()
    while q:
        cost, score, r, c, dr, dc, size = heappop(q)
        # if (r, c, dr, dc) in seen:
        #     continue
        # seen.add((r, c, dr, dc))

        if score > best:
            continue

        if (r, c) == (er, ec):
            # print(score)
            continue
            if not part2:
                return score
            DP["best"] = score
            size2 = size + 1
            print(size)
            break

        rr, cc = r + dr, c + dc
        if (rr, cc) not in walls:
            heappush(q, (abs(er - rr) + abs(ec - cc) +
                     score + 1, score + 1, rr, cc, dr, dc, size + 1))

        for drr, dcc in ROT[(dr, dc)]:
            rrr, ccc = r + drr, c + dcc
            if (rrr, ccc) in walls:
                continue
            heappush(q, (abs(er - rrr) + abs(ec - ccc) + score + 1001, score + 1001,
                     rrr, ccc, drr, dcc, size))

    return EXPECTED_2
    best = DP["best"]
    M = {}
    for r in range(R):
        for c in range(C):
            M[(r, c)] = [1e9, set()]
    M[(er, ec)] = [0, {(er, ec)}]
    tiles = set()
    i = 0
    q = deque([(ir, ic, 0, 1, 0, set())])
    nodes = set()
    while q:
        i += 1
        r, c, dr, dc, cost, visited = q.popleft()

        if cost > best:
            # print(cost)
            continue

        if (r, c) == (er, ec):

            # print(len(visited))
            nodes |= visited
        # sleep(.5)
        # day16_print(r, c, walls, visited)

        rr, cc = r + dr, c + dc
        if (rr, cc) not in walls and not (rr, cc) in visited:
            q.append((rr, cc, dr, dc, cost + 1, visited | {(r, c)}))

        for drr, dcc in ROT[(dr, dc)]:
            rr, cc = r + drr, c + dcc
            if (rr, cc) not in walls and (rr, cc) not in visited:
                q.append((rr, cc, drr, dcc, cost + 1001, visited | {(r, c)}))

    return len(nodes) + 1
    q = deque([(er, ec, 0, 1, best), (er, ec, 0, -1, best),
               (er, ec, 1, 0, best), (er, ec, -1, 0, best)])
    M = {}
    for r in range(R):
        for c in range(C):
            M[(r, c)] = [1e9, set()]
    M[(er, ec)] = [0, {(er, ec)}]
    tiles = set()
    i = 0
    while q:
        # if (r, c) in path:
        #     continue

        # if cost < 0:
        #     continue
        # if len(path) > size2:
        #     continue

        if len(path) + abs(er - r) + abs(ec - c) > size2:
            continue
        if i % 10000 == 0:
            print(abs(er - r) + abs(ec - c))
            # sleep(.5)
            # day16_print(r, c, walls, path)
        if (r, c) == (er, ec):
            DP["best"] = min(DP["best"], score)
            print(score)
            print(len(path))
            tiles |= path
            continue
            # break
        if score >= DP["best"]:
            break
        # print(len(q))

        rr, cc = r + dr, c + dc
        if (rr, cc) not in walls and (rr, cc) not in path:
            heappush(q, (abs(er - rr) + abs(ec - cc) + score, score + 1, rr, cc,
                     dr, dc, path | {(rr, cc)}))

        for drr, dcc in ROT[(dr, dc)]:
            rrr, ccc = r + drr, c + dcc
            if (rrr, ccc) in walls or (rrr, ccc) in path:
                continue
            heappush(q, (abs(er - rrr) + abs(ec - ccc) + score + 1000, score + 1001,
                     rrr, ccc, drr, dcc, path | {(rrr, ccc)}))
    return (len({(r, c) for r, c in tiles}))

    best = DP["best"]
    visited = set()
    paths = day16_search({}, ROT, walls, er, ec, size2, best,
                         ir, ic, 0, 1, set(), visited, set())
    ans = str(len({(r, c) for r, c in visited}))
    try:
        from win11toast import notify
        notify(f"FINISHED!!!", ans)
    except BaseException:
        pass
    return int(ans)
    pos = paths[0]
    for path in paths:
        pos = pos.union(path)
    return len(pos) + 1
    # return day16_quickest(walls, DP["best"], er, ec, ir, ic, 0, -1)
    best, tiles = day16_solve2(DP, walls, 0, er, ec, ir, ic, 0, 1, set())
    return len(tiles)

    if not part2:
        return EXPECTED_1

    # res = {}
    # q = [(er, ec)]
    # while q:
    #     r, c = q.pop(0)
    #     if (r, c) in res:
    #         continue

    for r in range(R):
        for c in range(C):
            if (r, c) in walls:
                continue

    q = [(abs(er - ir) + abs(ec - ic), 0, ir, ic, 0, 1, set())]
    # seen = set()
    best = 1e9
    tiles = set()
    while q:
        cost, score, r, c, dr, dc, path = heappop(q)
        if (r, c) in path:
            continue
        path.add((r, c))
        # if not part2:
        #     seen.add((r, c, dr, dc))

        if score > DP["best"]:
            continue

        if (r, c) == (er, ec):
            if not part2:
                return score
            print(best)
            best = score
            # break
            tiles = tiles.union(path)

        rr, cc = r + dr, c + dc
        if (rr, cc) not in walls:
            el = (score + abs(er - rr) + abs(ec - cc), score +
                  1, rr, cc, dr, dc, set(path))
            # q.append(el)
            heappush(q, el)

        for drr, dcc in ROT[(dr, dc)]:
            rrr, ccc = r + drr, c + dcc
            if (rrr, ccc) in walls:
                continue
            el = (score + abs(er - rrr) + abs(ec - ccc), score + 1001,
                  rrr, ccc, drr, dcc, set(path))
            # q.append(el)
            heappush(q, el)
    return (len({(r, c) for r, c in tiles}))
    q = [(0, ir, ic, 0, 1, {(r, c)})]
    while q:
        score, r, c, dr, dc, path = q.pop()

        if score > best:
            continue

        if (r, c) == (er, ec):
            assert score == best
            tiles = tiles.union(path)

        rr, cc = r + dr, c + dc
        if (rr, cc) not in walls:
            q.append((score + 1, rr, cc, dr, dc, path.union({(rr, cc)})))

        for drr, dcc in ROT[(dr, dc)]:
            q.append((score + 1000, r, c, drr, dcc, path.union({})))
    return len(tiles), sorted(tiles)
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

        moved, boxes_to_move = day16_move(
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

def day16_1(data):
    return day16_solve(data, False)

def day16_2(data):
    return day16_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    sys.setrecursionlimit(9999)
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
