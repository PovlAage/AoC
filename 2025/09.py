import collections
import queue
from bisect import bisect
from dataclasses import dataclass, field
import functools
import itertools
from collections import defaultdict
from itertools import permutations, pairwise
from math import *
from time import time

import numpy as np
import re
from enum import StrEnum, Enum

day = int(__file__.rstrip('.py').split('/')[-1])
print("day", day)
start_time = time()

def verify(actual, expected):
    if actual == expected:
        print("OK", actual)
    else:
        print(f"FAIL {actual}!={expected}")

def read_input() -> str:
    return open(f'input/{day:02}').read().strip()

def read_input_lines() -> str:
    return open(f'input/{day:02}').read().strip().splitlines()

def parse_blocks(text: str):
    blocks = text.split('\n\n')
    return blocks[0].split('\n'), blocks[1].split('\n')

@dataclass(frozen=True, order=True)
class Point:
    y: int
    x: int

@dataclass(frozen=True)
class Direction:
    dy: int
    dx: int

north = Direction(dy=-1, dx=0)
south = Direction(dy=1, dx=0)
west = Direction(dy=0, dx=-1)
east = Direction(dy=0, dx=1)
directions: list[Direction] = [north, south, east, west]
Line = tuple[Point, Point]
Corner = tuple[Point, Point, Point, Direction, Direction]  # first two points are corner point and next point, directions are the two "out" directions from the third point

def get_line(corner: Corner) -> Line:
    return corner[0], corner[1]

def get_directions(corner: Corner) -> tuple[Direction, Direction]:
    return corner[2], corner[3]

def opposite(direction: Direction) -> Direction:
    return Direction(dy=-direction.dy, dx=-direction.dx)

def rotate_positive(direction: Direction) -> Direction:
    return Direction(dy=direction.dx, dx=-direction.dy)

def sign(x):
    return (x > 0) - (x < 0)

def d(p1, p2) -> Direction:
    assert (p1.y == p2.y) != (p1.x == p2.x), "netop én koordinat skal være forskellig"
    return Direction(dy=sign(p2.y - p1.y), dx=sign(p2.x - p1.x))

def add(p: Point, d: Direction) -> Point:
    return Point(y=p.y + d.dy, x=p.x + d.dx)

def parse(lines) -> list[Point]:
    def parse_line(line: str) -> Point:
        s0, s1 = line.split(',')
        return Point(y=int(s0), x=int(s1))
    return [parse_line(line) for line in lines]

def build(points: list[Point]) -> tuple[list[Corner], list[Line]]:
    # verify assumptions
    def only_90_degree_turns():
        dprev = d(points[-1], points[0])  # first side
        for p1, p2 in pairwise(points):
            dnext = d(p1, p2)
            assert (dprev.dy != dnext.dy) and (dprev.dx != dnext.dx), "begge koordinater skal ændres"
            dprev = dnext

    only_90_degree_turns()

    # points lexicographical ordered, so min(p) is "a northwest corner"
    _, nw_index = min((p, i) for i, p in enumerate(points))
    min_y, max_y = min(p.y for p in points), max(p.y for p in points)
    min_x, max_x = min(p.x for p in points), max(p.x for p in points)
    n = len(points)
    corners: list[Corner] = []
    prev_index = (nw_index + n - 1) % n
    if points[prev_index].x > points[nw_index].x:
        dprev = west
        clockwise = False
    elif points[prev_index].y < points[nw_index].y:
        dprev = north
        clockwise = True
    else:
        raise ValueError("Unexpected direction")
    for (p1, p2) in ((points[(nw_index + j) % n], points[(nw_index + j + 1) % n]) for j in range(n)):
        dnext = d(p1, p2)
        assert dnext == rotate_positive(dprev) or dprev == rotate_positive(dnext)
        is_outside_corner = ((not clockwise) and dprev == rotate_positive(dnext)) or (clockwise and dnext == rotate_positive(dprev))
        if is_outside_corner:
            corner = (p1, p2, p1, dprev, opposite(dnext))
        else:
            corner = (p1, p2, add(add(p1, opposite(dprev)), dnext), opposite(dprev), dnext)
        _, _, cp, _, _ = corner
        assert min_y <= cp.y <= max_y and min_x <= cp.x <= max_x
        corners.append(corner)
        dprev = dnext

    assert corners[0][3] == dprev, f"{corners[0]}"

    east_west_sorted_y: list[Line] = sorted(((p1, p2) for p1, p2, _, _, _ in  corners if p1.y == p2.y), key=lambda pp: pp[0].y)
    north_south_sorted_x: list[Line] = sorted(((p1, p2) for p1, p2, _, _, _ in  corners if p1.x == p2.x), key=lambda pp: pp[0].x)
    black_lines: list[Line] = []
    for p1, _, p, d1, d2 in corners:
        for dd in (d1, d2):
            line_start = add(p, dd) if p == p1 else p
            if not (min_y <= line_start.y <= max_y and min_x <= line_start.x <= max_x):
                continue
            if dd == north or dd == south:
                s = -1 if dd == north else 1
                # go through east_west lines in order, to see if our line hits any of them
                # start with the first one
#                i = bisect(east_west_sorted_y, s * line_start[0], key=lambda pp: s * pp[0][0])
                line_end = Point(y=min_y if dd == north else max_y, x=line_start.x)  # default if nothing found
                rng = range(0, len(east_west_sorted_y)) if s == 1 else range(len(east_west_sorted_y) - 1, -1, -1)
                for i in rng:
                    # skip the ones in the wrong direction
                    ll = east_west_sorted_y[i]
                    ll_y = ll[0].y
                    if ll_y < line_start.y and dd == south:
                        continue
                    if ll_y > line_start.y and dd == north:
                        continue
                    l1, l2 = (ll[0], ll[1]) if ll[0] < ll[1] else (ll[1], ll[0])
                    if l1.x <= line_start.x <= l2.x:
                        assert l1.y == l2.y
                        line_end = add(Point(y=l1.y, x=line_start.x), opposite(dd))
                        break
            elif dd == west or dd == east:
                s = -1 if dd == west else 1
#                i = bisect(north_south_sorted_x, s * line_start[1], key=lambda pp: s * pp[0][1])
                line_end = Point(y=line_start.y, x=min_x if dd == west else max_x)  # default if nothing found
                rng = range(0, len(north_south_sorted_x)) if s == 1 else range(len(north_south_sorted_x) - 1, -1, -1)
                for i in rng:
                    # skip the ones in the wrong direction
                    ll = north_south_sorted_x[i]
                    ll_x = ll[0].x
                    if ll_x < line_start.x and dd == east:
                        continue
                    if ll_x > line_start.x and dd == west:
                        continue
                    l1, l2 = (ll[0], ll[1]) if ll[0] < ll[1] else (ll[1], ll[0])
                    if l1.y <= line_start.y <= l2.y:
                        assert l1.x == l2.x
                        line_end = add(Point(y=line_start.y, x=l1.x), opposite(dd))
                        break
            else:
                raise ValueError(f"Invalid direction: {dd}")

            if line_end != line_start:
                assert line_start.y == line_end.y or line_start.x == line_end.x
                black_lines.append((line_start, line_end))

    return corners, black_lines

def area(p1: Point, p2: Point) -> int:
    return (abs(p2.x - p1.x) + 1) * (abs(p2.y - p1.y) + 1)

def plot(corners, black_lines):
    min_y, max_y = min(c[0].y for c in corners), max(c[0].y for c in corners)
    min_x, max_x = min(c[0].x for c in corners), max(c[0].x for c in corners)
    assert max_x >= 0 and max_y >= 0
    canvas = [(max_x + 1) * ["."] for _ in range(max_y + 1)]
    def plot_point(p, c):
        y, x = p.y, p.x
        # print("plot", y, x, c)
        if not (min_y <= y <= max_y and min_x <= x <= max_x):
            print("ERROR")
            return
        assert min_y <= y <= max_y, f"y: {min_y} <= {y} <= {max_y}"
        assert min_x <= x <= max_x, f"x: {min_x} <= {x} <= {max_x}"
        assert canvas[y][x] == '.' or canvas[y][x] == c
        canvas[y][x] = c

    for p1, p2, _, _, _ in corners:
        assert p1.y == p2.y or p1.x == p2.x
        plot_point(p1, "R")
        dd = Direction(dy=sign(p2.y-p1.y), dx=sign(p2.x-p1.x))
        pp = add(p1, dd)
        while pp != p2:
            plot_point(pp, "G")
            pp = add(pp, dd)

    for p1, p2 in black_lines:
        plot_point(p1, "B")
        plot_point(p2, "B")

    for y in canvas:
        row = "".join(y)
        print(row)

def a(lines):
    points = parse(lines)
    return max(area(p1, p2) for p1, p2 in permutations(points, 2))

def b(lines, verbose=False):
    points = parse(lines)
    corners, black_lines = build(points)
    if verbose:
        if len(corners) > 20:
            print("Cannot plot this large")
        else:
            plot(corners, black_lines)

    def intersect_normalized_rect_line(r1x, r1y, r2x, r2y, l: Line):
        l0x, l0y, l1x, l1y = l[0].x, l[0].y, l[1].x, l[1].y
#        assert r1x <= r2x and r1y <= r2y and l0x <= l1x and l0y <= l1y

        def rect_contains(p: Point):
            return r1x <= p.x <= r2x and r1y <= p.y <= r2y

        if rect_contains(l[0]) or rect_contains(l[1]):
            return True
        is_vertical = l0y != l1y
        if is_vertical:
            return r1x <= l0x <= r2x and l0y < r1y <= r2y < l1y
        else:
            return r1y <= l0y <= r2y and l0x < r1x <= r2x < l1x

    def normalize_line(l: Line):
        return (
            Point(x=min(l[0].x, l[1].x), y=min(l[0].y, l[1].y)),
            Point(x=max(l[0].x, l[1].x), y=max(l[0].y, l[1].y)),
        )

    black_lines = [normalize_line(l) for l in black_lines]

    def is_admissible_rect(p1, p2):
        # normalized rect
        r1x, r1y = min(p1.x, p2.x), min(p1.y, p2.y)
        r2x, r2y = max(p1.x, p2.x), max(p1.y, p2.y)

        def intersect_line(l):
            return intersect_normalized_rect_line(r1x, r1y, r2x, r2y, l)

        return not any(intersect_line(l) for l in black_lines)

    l = len(list(permutations(points, 2)))
    i = 0
    pct = l // 100 + 1
    area_and_permutations = sorted([(area(p1, p2), p1, p2) for p1, p2 in permutations(points, 2)], reverse=True)
    for a, p1, p2 in area_and_permutations:
        i += 1
        if i % (5 * pct) == 0: print(f"{i}/{l}")
        if is_admissible_rect(p1, p2):
            return a
    raise ValueError("No admissible rect found")

test_input = """
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
""".strip().splitlines()

assert a(test_input) == 50, a(test_input)
assert b(test_input, verbose=False) == 24, b(test_input)

verify(a(read_input_lines()), 4755429952)
verify(b(read_input_lines(), verbose=False), 1429596008)

print(f"Elapsed: {time() - start_time:.3f}s")
