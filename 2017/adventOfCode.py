# pylint: disable=unused-import
# pylint: disable=import-error
# pylint: disable=wrong-import-position
import functools
import math
import multiprocessing as mp
import os
import re
import string
import sys
import time
from collections import Counter, deque
import heapq
from enum import IntEnum
from struct import pack

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
print(FILE_DIR)
sys.path.insert(0, FILE_DIR + "/../")
sys.path.insert(0, FILE_DIR + "/../../")
from common.utils import execute_day, read_input, main  # NOQA: E402
# pylint: enable=unused-import
# pylint: enable=import-error
# pylint: enable=wrong-import-position

start_day = 1

""" DAY 20 """

class I:
    px = 0
    py = 1
    pz = 2
    vx = 3
    vy = 4
    vz = 5
    ax = 6
    ay = 7
    az = 8

def day20_parse_line(line):
    # p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>
    return tuple([int(a) for a in re.findall("p=<(-?\d+),(-?\d+),(-?\d+)>, v=<(-?\d+),(-?\d+),(-?\d+)>, a=<(-?\d+),(-?\d+),(-?\d+)>", line)[0]])

def day20_parse_input(data):
    return [day20_parse_line(line) for line in data]

def day20_update_particle(particle):
    px, py, pz, vx, vy, vz, ax, ay, az = particle
    vx += ax
    vy += ay
    vz += az
    px += vx
    py += vy
    pz += vz
    return (px, py, pz, vx, vy, vz, ax, ay, az)

def day20_closest(particles):
    distances = [abs(particle[I.px]) + abs(particle[I.py]) +
                 abs(particle[I.pz]) for particle in particles]
    keep_going = True
    counter = 0
    prev_closest = 0
    while keep_going:
        particles = [day20_update_particle(particle) for particle in particles]
        old_distances = distances
        distances = [abs(particle[I.px]) + abs(particle[I.py]) +
                     abs(particle[I.pz]) for particle in particles]
        minimum = min(distances)
        keep_going = len([x for x in distances if x == minimum]) != 1
        #keep_going = False
        for i in range(len(particles)):
            if old_distances[i] > distances[i]:
                keep_going = True
                break

        closest = 0
        closest_dist = distances[closest]
        for i in range(len(distances)):
            if distances[i] < closest_dist:
                closest = i
                closest_dist = distances[closest]

        if prev_closest == closest:
            counter += 1

        prev_closest = closest
        keep_going = counter < 500
    return closest

def day20_left(particles):
    alive = [True for i in range(len(particles))]
    keep_going = True
    counter = 0
    prev_alive_count = len(particles)
    while keep_going:
        particles = [day20_update_particle(particle) for particle in particles]
        collided = []
        for i in range(len(particles)):
            if alive[i]:
                for j in range(len(particles)):
                    particle_j = particles[j]
                    particle_i = particles[i]
                    if i != j and alive[j] and particle_i[I.px] == particle_j[I.px] and particle_i[I.py] == particle_j[I.py] and particle_i[I.pz] == particle_j[I.pz]:
                        collided.append(i)
        for col in collided:
            alive[col] = False

        alive_count = len([True for a in alive if a])
        if prev_alive_count == alive_count:
            counter += 1

        prev_alive_count = alive_count
        keep_going = counter < 50

    return alive_count

def day20_1(data):
    #data = read_input(2017, 2001)
    particles = day20_parse_input(data)
    return day20_closest(particles)

def day20_2(data):
    #data = read_input(2017, 2001)
    particles = day20_parse_input(data)
    return day20_left(particles)

""" DAY 21 """

#start_day = 10
""" MAIN FUNCTION """
if __name__ == "__main__":
    for i in range(start_day, 26):
        execute_day(globals(), 2017, i, 1)
        execute_day(globals(), 2017, i, 2)
