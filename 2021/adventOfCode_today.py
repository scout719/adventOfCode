# -*- coding: utf-8 -*-
# pylint: disable=import-error
# pylint: disable=unused-import
# pylint: disable=wildcard-import
# pylint: disable=wrong-import-position
# pylint: disable=consider-using-enumerate
from typing import Callable, Iterator, Union, Optional, List
import functools
import math
import os
from os.path import join
import sys
import time
from copy import deepcopy
from collections import Counter, defaultdict, deque
from heapq import heappop, heappush
from typing import ChainMap

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import read_input, main, clear  # NOQA: E402
from common.utils import day_with_validation, bcolors, WHITE_CIRCLE, WHITE_SQUARE  # NOQA: E402
from common.utils import BLUE_CIRCLE, RED_SMALL_SQUARE  # NOQA: E402
# pylint: enable=import-error
# pylint: enable=wrong-import-position

YEAR = 2021
DAY = 22
EXPECTED_1 = None  # 474140
EXPECTED_2 = 2758514936282235


""" DAY 22 """

def day22_parse(data):
    robots = []
    for line in data:
        # on x=10..12,y=10..12,z=10..12
        on = line.startswith("on")
        line = line.replace("on ", "").replace("off ", "")
        x, y, z = line.split(",")
        x = x.replace("x=", "")
        x1, x2 = [int(v) for v in x.split("..")]
        y = y.replace("y=", "")
        y1, y2 = [int(v) for v in y.split("..")]
        z = z.replace("z=", "")
        z1, z2 = [int(v) for v in z.split("..")]
        robots.append((x1, x2, y1, y2, z1, z2, on))

    return robots

def day22_1(data):
    robots = day22_parse(data)

    collapsed = [robots[0]]
    x1, x2, y1, y2, z1, z2, on = robots[0]
    inst = on
    minx, maxx, miny, maxy, minz, maxz = (x1, x2, y1, y2, z1, z2)
    for x1, x2, y1, y2, z1, z2, on in robots[1:]:
        if on == inst:
            minx = min(minx, x1)
            maxx = max(maxx, x2)
            miny = min(miny, y1)
            maxy = max(maxy, y2)
            minz = min(minz, z1)
            maxz = max(maxz, z2)
        else:
            collapsed.append((minx, maxx, miny, maxy, minz, maxz, on))
            inst = on
            minx, maxx, miny, maxy, minz, maxz = (x1, x2, y1, y2, z1, z2)
    robots = collapsed

    lo = -50
    hi = 50
    all_on = set()
    # for x in range(lo, hi + 1):
    #     for y in range(lo, hi + 1):
    #         for z in range(lo, hi + 1):
    #             for x1, x2, y1, y2, z1, z2, on in robots:
    #                 if x1 <= x <= x2 and y1 <= y <= y2 and z1 <= z <= z2:
    #                     if on:
    #                         all_on.add((x, y, z))
    #                     else:
    #                         if (x, y, z) in all_on:
    #                             all_on.remove((x, y, z))

    return len(all_on)

# https://evanw.github.io/csg.js/docs/

class Vector:
    """
    Represents a 3D vector.
    """

    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z

    def clone(self):
        return Vector(self.x, self.y, self.z)

    def negated(self):
        return Vector(-self.x, -self.y, -self.z)

    def plus(self, other: "Vector"):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def minus(self, other: "Vector"):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def times(self, a: int):
        return Vector(self.x * a, self.y * a, self.z * a)

    def dividedBy(self, a: int):
        return Vector(self.x / a, self.y / a, self.z / a)

    def dot(self, other: "Vector"):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def lerp(self, a: "Vector", t: int):
        return self.plus(a.minus(self).times(t))

    def length(self):
        return math.sqrt(self.dot(self))

    def unit(self):
        return self.dividedBy(self.length())

    def cross(self, other: "Vector"):
        return Vector(self.y * other.z - self.z * other.y,
                      self.z * other.x - self.x * other.z,
                      self.x * other.y - self.y * other.x)

class Vertex:
    """
    Represents a vertex of a polygon.
    """

    def __init__(self, pos: Vector, normal: Vector) -> None:
        self.pos = Vector(pos.x, pos.y, pos.z)
        self.normal = Vector(normal.x, normal.y, normal.z)

    def clone(self):
        return Vertex(self.pos.clone(), self.normal.clone())

    def flip(self):
        """
        Invert all orientation-specific data (e.g. vertex normal).
        Called when the orientation of a polygon is flipped.
        """
        self.normal = self.normal.negated()

    def interpolate(self, other: Vector, t: int):
        """
        Create a new vertex between this vertex and other by linearly interpolating all properties using a parameter of t.
        """
        return Vertex(self.pos.lerp(other.pos, t), self.normal.lerp(other.normal, t))

class Plane:
    """
    Represents a plane in 3D space.
    """

    def __init__(self, normal: Vector, w: int) -> None:
        self.normal = normal
        self.w = w

    """
    CSG.Plane.EPSILON is the tolerance used by splitPolygon() to decide if a point is on the plane.
    """
    EPSILON = 1e-5

    @staticmethod
    def fromPoints(a: Vector, b: Vector, c: Vector):
        n = b.minus(a).cross(c.minus(a)).unit()
        return Plane(n, n.dot(a))

    def clone(self):
        return Plane(self.normal.clone(), self.w)

    def flip(self):
        self.normal = self.normal.negated()
        self.w = -self.w

    def splitPolygon(self, polygon: "Polygon", coplanarFront: List["Polygon"], coplanarBack: List["Polygon"], front: List["Polygon"], back: List["Polygon"]):
        """
        Split polygon by this plane if needed, then put the polygon or polygon fragments in the appropriate lists.
        Coplanar polygons go into either coplanarFront or coplanarBack depending on their orientation with respect to this plane.
        Polygons in front or in back of this plane go into either front or back.
        """
        COPLANAR = 0
        FRONT = 1
        BACK = 2
        SPANNING = 3

        polygonType = 0
        types = []
        for i in range(len(polygon.vertices)):
            t = self.normal.dot(polygon.vertices[i].pos) - self.w
            type_ = 0
            if t < -Plane.EPSILON:
                type_ = BACK
            elif t > Plane.EPSILON:
                type_ = FRONT
            else:
                type_ = COPLANAR
            polygonType |= type_
            types.append(type_)

        if polygonType == COPLANAR:
            x = self.normal.dot(polygon.plane.normal)
            if x > 0:
                coplanarFront.append(polygon)
            else:
                coplanarBack.append(polygon)
        elif polygonType == FRONT:
            front.append(polygon)
        elif polygonType == BACK:
            back.append(polygon)
        elif polygonType == SPANNING:
            f = []
            b = []
            for i in range(len(polygon.vertices)):
                j = (i + 1) % len(polygon.vertices)
                ti, tj = types[i], types[j]
                vi, vj = polygon.vertices[i], polygon.vertices[j]
                if (ti != BACK):
                    f.append(vi)
                if (ti != FRONT):
                    if ti != BACK:
                        b.append(vi.clone())
                    else:
                        b.append(vi)
                if ((ti | tj) == SPANNING):
                    t = (self.w - self.normal.dot(vi.pos)) / \
                        self.normal.dot(vj.pos.minus(vi.pos))
                    v = vi.interpolate(vj, t)
                    f.append(v)
                    b.append(v.clone())
            if (len(f) >= 3):
                front.append(Polygon(f, polygon.shared))
            if (len(b) >= 3):
                back.append(Polygon(b, polygon.shared))


class Polygon:
    """
    Represents a convex polygon.
    The vertices used to initialize a polygon must be coplanar and form a convex loop.
    Each convex polygon has a shared property, which is shared between all polygons that are clones of each other or were split from the same polygon.
    This can be used to define per-polygon properties (such as surface color).
    """

    def __init__(self, vertices: List[Vertex], shared) -> None:
        self.vertices = vertices
        self.shared = shared
        self.plane = Plane.fromPoints(
            vertices[0].pos, vertices[1].pos, vertices[2].pos)

    def clone(self):
        vert = [v.clone() for v in self.vertices]
        return Polygon(vert, self.shared)

    def flip(self):
        self.vertices.reverse()
        map(lambda v: v.flip(), self.vertices)
        self.plane.flip()

class Node:
    """
    Holds a node in a BSP tree.
    A BSP tree is built from a collection of polygons by picking a polygon to split along.
    That polygon (and all other coplanar polygons) are added directly to that node and the other polygons are added to the front and/or back subtrees.
    This is not a leafy BSP tree since there is no distinction between internal and leaf nodes.
    """

    def __init__(self, polygons: List[Polygon]) -> None:
        self.plane: Plane = None
        self.front: "Node" = None
        self.back: "Node" = None
        self.polygons: List[Polygon] = []
        if polygons:
            self.build(polygons)

    def clone(self):
        node = Node([])
        if self.plane:
            node.plane = self.plane.clone()
        if self.front:
            node.front = self.front.clone()
        if self.back:
            node.back = self.back.clone()
        node.polygons = [p.clone() for p in self.polygons]
        return node

    def invert(self):
        """
        Convert solid space to empty space and empty space to solid space.
        """
        for i in range(len(self.polygons)):
            self.polygons[i].flip()

        self.plane.flip()
        if (self.front):
            self.front.invert()
        if (self.back):
            self.back.invert()
        temp = self.front
        self.front = self.back
        self.back = temp

    def clipPolygons(self, polygons: List[Polygon]):
        """
        Recursively remove all polygons in polygons that are inside this BSP tree.
        """
        if not self.plane:
            return [p for p in polygons]

        front, back = [], []
        for i in range(len(polygons)):
            self.plane.splitPolygon(polygons[i], front, back, front, back)
        if (self.front):
            front = self.front.clipPolygons(front)

        if (self.back):
            back = self.back.clipPolygons(back)
        else:
            back = []
        return front + back

    def clipTo(self, bsp: "Node"):
        """
        Remove all polygons in this BSP tree that are inside the other BSP tree bsp.
        """
        self.polygons = bsp.clipPolygons(self.polygons)
        if (self.front):
            self.front.clipTo(bsp)
        if (self.back):
            self.back.clipTo(bsp)

    def allPolygons(self):
        """
        Return a list of all polygons in this BSP tree.
        """
        polygons = [p for p in self.polygons]

        if (self.front):
            polygons += self.front.allPolygons()
        if (self.back):
            polygons += self.back.allPolygons()

        return polygons

    def build(self, polygons: List[Polygon]):
        """
        Build a BSP tree out of polygons. 
        When called on an existing tree, the new polygons are filtered down to the bottom of the tree and become new nodes there.
        Each set of polygons is partitioned using the first polygon (no heuristic is used to pick a good split).
        """

        if not polygons:
            return
        if (not self.plane):
            self.plane = polygons[0].plane.clone()
        front, back = [], []

        for i in range(len(polygons)):
            self.plane.splitPolygon(
                polygons[i], self.polygons, self.polygons, front, back)

        if front:
            if not self.front:
                self.front = Node([])
            self.front.build(front)

        if back:
            if not self.back:
                self.back = Node([])
            self.back.build(back)


class CSG:
    def __init__(self) -> None:
        self.polygons: List[Polygon] = []

    @staticmethod
    def fromPolygons(polygons: List[Polygon]):
        t = CSG()
        t.polygons = polygons
        return t

    def clone(self):
        t = CSG()
        t.polygons = [p.clone() for p in self.polygons]
        return t

    def toPolygons(self):
        return self.polygons

    def union(self, csg: "CSG"):
        """
        Return a new CSG solid representing space in either this solid or in the solid csg. 
        Neither this solid nor the solid csg are modified.

A.union(B)

+-------+            +-------+
|       |            |       |
|   A   |            |       |
|    +--+----+   =   |       +----+
+----+--+    |       +----+       |
     |   B   |            |       |
     |       |            |       |
     +-------+            +-------+

        """
        a = Node(self.clone().polygons)
        b = Node(csg.clone().polygons)

        a.clipTo(b)
        b.clipTo(a)
        b.invert()
        b.clipTo(a)
        b.invert()
        a.build(b.allPolygons())
        return CSG.fromPolygons(a.allPolygons())

    def subtract(self, csg: "CSG"):
        """
Return a new CSG solid representing space in this solid but not in the solid csg. 
Neither this solid nor the solid csg are modified.

A.subtract(B)

+-------+            +-------+
|       |            |       |
|   A   |            |       |
|    +--+----+   =   |    +--+
+----+--+    |       +----+
     |   B   |
     |       |
     +-------+

        """
        a = Node(self.clone().polygons)
        b = Node(csg.clone().polygons)
        a.invert()
        a.clipTo(b)
        b.clipTo(a)
        b.invert()
        b.clipTo(a)
        b.invert()
        a.build(b.allPolygons())
        a.invert()
        return CSG.fromPolygons(a.allPolygons())

    def intersect(self, csg: "CSG"):
        """
Return a new CSG solid representing space both this solid and in the solid csg. Neither this solid nor the solid csg are modified.

A.intersect(B)

+-------+
|       |
|   A   |
|    +--+----+   =   +--+
+----+--+    |       +--+
     |   B   |
     |       |
     +-------+

"""
        a = Node(self.clone().polygons)
        b = Node(csg.clone().polygons)
        a.invert()
        b.clipTo(a)
        b.invert()
        a.clipTo(b)
        b.clipTo(a)
        a.build(b.allPolygons())
        a.invert()
        return CSG.fromPolygons(a.allPolygons())

    def inverse(self):
        """
        Return a new CSG solid with solid and empty space switched. This solid is not modified.
        """
        csg = self.clone()
        map(lambda p: p.flip(), csg.polygons)
        return csg

def tmp(i: int, info: List[int], r: List[int], c: Vector):
    pos = Vector(
        c.x + r[0] * (2 * int(i & 1) - 1),
        c.y + r[1] * (2 * int(i & 2) - 1),
        c.z + r[2] * (2 * int(i & 4) - 1)
    )
    return Vertex(pos, Vector(info[1][0], info[1][1], info[1][2]))


def day22_cube(center, radius, shared):
    c = Vector(center[0], center[1], center[2])
    r = radius

    return CSG.fromPolygons(list(map(lambda info: Polygon(list(map(lambda i: tmp(i, info, r, c), info[0])), shared),
                                     [
        [[0, 4, 6, 2], [-1, 0, 0]],
                                    [[1, 3, 7, 5], [+1, 0, 0]],
                                    [[0, 1, 5, 4], [0, -1, 0]],
                                    [[2, 6, 7, 3], [0, +1, 0]],
                                    [[0, 2, 3, 1], [0, 0, -1]],
                                    [[4, 5, 7, 6], [0, 0, +1]]
    ]
    )))

def day22_from_robot(robot):
    x1, x2, y1, y2, z1, z2, on = robot
    radius_x = (x2 - x1) / 2
    # assert radius_x == (x2 - x1) // 2
    radius_y = (y2 - y1) / 2
    # assert radius_y == (y2 - y1) // 2
    radius_z = (z2 - z1) / 2
    # assert radius_z == (z2 - z1) // 2
    # assert radius_x == radius_y == radius_z, (radius_x,radius_y,radius_z)

    center_x = x1 + radius_x
    center_y = y1 + radius_y
    center_z = z1 + radius_z

    print(radius_x, center_x, center_y, center_z)
    return day22_cube([center_x, center_y, center_z], [radius_x, radius_y, radius_z], on)

def day22_2(robots):
    robots = day22_parse(robots)

    state = day22_from_robot(robots[0])
    print(robots[0], [[(v.pos.x, v.pos.y, v.pos.z) for v in p.vertices]
                      for p in state.polygons])
    return
    for robot in robots:
        curr = day22_from_robot(robot)
        if robot[6]:
            state = state.union(curr)
        else:
            state = state.subtract(curr)

    for p in state.polygons:
        print(len(p.vertices))
    return state
    print()

    x1, x2, y1, y2, z1, z2, on = robots[0]
    regions_on = [(x1, x2, y1, y2, z1, z2)]
    inst = on
    minx, maxx, miny, maxy, minz, maxz = (x1, x2, y1, y2, z1, z2)
    for x1, x2, y1, y2, z1, z2, on in robots[1:]:

        if on == inst:
            minx = min(minx, x1)
            maxx = max(maxx, x2)
            miny = min(miny, y1)
            maxy = max(maxy, y2)
            minz = min(minz, z1)
            maxz = max(maxz, z2)
        else:
            collapsed.append((minx, maxx, miny, maxy, minz, maxz, on))
            inst = on
            minx, maxx, miny, maxy, minz, maxz = (x1, x2, y1, y2, z1, z2)
    robots = collapsed

    pts = set()

    for x1, x2, y1, y2, z1, z2, on in robots:
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    pts.add((x, y, z))
    return len(pts)

    min_x = min([x for x, _, y, _, z, _, _ in robots])
    min_y = min([y for x, _, y, _, z, _, _ in robots])
    min_z = min([z for x, _, y, _, z, _, _ in robots])
    max_x = max([x for _, x, _, y, _, z, _ in robots])
    max_y = max([y for _, x, _, y, _, z, _ in robots])
    max_z = max([z for _, x, _, y, _, z, _ in robots])
    lo = -50
    hi = 50
    print(min_x, max_x, min_y, max_y, min_z, max_z)
    all_on = set()

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            for z in range(min_z, max_z + 1):
                for x1, x2, y1, y2, z1, z2, on in robots:
                    if x1 <= x <= x2 and y1 <= y <= y2 and z1 <= z <= z2:
                        if on:
                            all_on.add((x, y, z))
                        else:
                            if (x, y, z) in all_on:
                                all_on.remove((x, y, z))

    return len(all_on)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
