# -*- coding: utf-8 -*-
# pylint: disable=import-error
# pylint: disable=unused-import
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# pylint: disable=wrong-import-position
# pylint: disable=consider-using-enumerate
import os
import sys
from heapq import heappop, heappush

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main, day_with_validation  # NOQA: E402
# pylint: enable=import-error
# pylint: enable=wrong-import-position

YEAR = 2022
DAY = 15
EXPECTED_1 = 26
EXPECTED_2 = 56000011


""" DAY 15 """

def day15_parse(data):
    sensors = []
    for line in data:
        # Sensor at x=2, y=18: closest beacon is at x=-2, y=15
        parts = line.split(":")
        sensor_x = int(parts[0].split(",")[0].split("=")[1])
        sensor_y = int(parts[0].split(",")[1].split("=")[1])
        beacon_x = int(parts[1].split(",")[0].split("=")[1])
        beacon_y = int(parts[1].split(",")[1].split("=")[1])
        sensors.append(((sensor_x, sensor_y), (beacon_x, beacon_y)))
    return sensors

def day15_1(data):
    sensors = day15_parse(data)
    target_y = 10
    if len(sensors) > 15:
        # real input
        target_y = 2000000

    max_sensor_range = max(abs(beacon_x - sensor_x)
                           for (sensor_x, _), (beacon_x, _) in sensors)
    lowest_x = min(sensor_x for (sensor_x, _), _ in sensors)
    highest_x = max(sensor_x for (sensor_x, _), _ in sensors)
    not_in = set()
    for x in range(lowest_x - max_sensor_range, highest_x + max_sensor_range + 1):
        y = target_y
        for (sensor_x, sensor_y), (beacon_x, beacon_y) in sensors:
            sensor_range = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)
            dist = abs(sensor_x - x) + abs(sensor_y - y)
            if dist <= sensor_range and not (x == beacon_x and y == beacon_y):
                not_in.add((x, y))
                break
    # 4797228
    return len([_ for _, y in not_in if y == target_y])

def day15_flood(x, y, dist, not_in, DP):
    if dist < 0:
        return
    key = (x, y)
    if key in DP and DP[key] >= dist:
        return
    DP[key] = dist
    not_in.add((x, y))
    D = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    for dx, dy in D:
        day15_flood(x + dx, y + dy, dist - 1, not_in, DP)

def day15_get_cost(x, y, sensors):
    cost = 0
    for (sensor_x, sensor_y), (beacon_x, beacon_y) in sensors:
        sensor_range = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)
        dist = abs(sensor_x - x) + abs(sensor_y - y)
        # How inside of the range is x,y
        cost += max(sensor_range - dist + 1, 0)
    return cost

def day15_within_range(x, y, sensors):
    for (sensor_x, sensor_y), (beacon_x, beacon_y) in sensors:
        sensor_range = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)
        dist = abs(sensor_x - x) + abs(sensor_y - y)
        # How inside of the range is x,y
        if dist <= sensor_range:
            return True
    return False

def day15_get_coords(sensor_x, sensor_y, radius, edge):
    coords = []
    top_left_x = sensor_x - radius
    top_left_y = sensor_y - (edge - radius)
    coords.append((top_left_x, top_left_y))
    top_right_x = sensor_x + radius
    top_right_y = sensor_y - (edge - radius)
    coords.append((top_right_x, top_right_y))
    bot_left_x = sensor_x - radius
    bot_left_y = sensor_y + (edge - radius)
    coords.append((bot_left_x, bot_left_y))
    bot_right_x = sensor_x + radius
    bot_right_y = sensor_y + (edge - radius)
    coords.append((bot_right_x, bot_right_y))

    return coords

def day15_visit_all_borders(sensors, max_limit):
    for (sensor_x, sensor_y), (beacon_x, beacon_y) in sensors:
        sensor_range = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)
        edge = sensor_range + 1
        for radius in range(1, edge + 1):
            for x, y in day15_get_coords(sensor_x, sensor_y, radius, edge):
                if 0 <= x <= max_limit and 0 <= y <= max_limit:
                    if not day15_within_range(x, y, sensors):
                        return x * 4000000 + y
    assert False

def day15_next_positions(x, y, sensors):
    positions = set()
    for (sensor_x, sensor_y), (beacon_x, beacon_y) in sensors:
        sensor_range = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)
        dist = abs(sensor_x - x) + abs(sensor_y - y)
        if dist <= sensor_range:
            edge = sensor_range + 1
            for radius in range(1, edge + 1):
                for xx, yy in day15_get_coords(sensor_x, sensor_y, radius, edge):
                    positions.add((xx, yy))
    return positions

def day15_original(sensors, max_limit):
    visited = set()
    start_x = max_limit // 2
    start_y = max_limit // 2
    queue = [(day15_get_cost(start_x, start_y, sensors), start_x, start_y)]
    while queue:
        cost, x, y = heappop(queue)
        if cost == 0:
            return x * 4000000 + y
        if (x, y) in visited:
            continue
        visited.add((x, y))
        for xx, yy in day15_next_positions(x, y, sensors):
            if (xx, yy) not in visited and 0 <= xx <= max_limit and 0 <= yy <= max_limit:
                heappush(queue, (day15_get_cost(xx, yy, sensors), xx, yy))
    assert False

def day15_2(data):
    sensors = day15_parse(data)
    max_limit = 20
    if len(sensors) > 15:
        # real input
        max_limit = 4000000

    return day15_visit_all_borders(sensors, max_limit)

    # Original solution
    # return day15_original(sensors, r)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
