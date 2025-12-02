import dataclasses
import functools
from collections import defaultdict
from itertools import permutations, pairwise

import numpy as np
import re
from enum import StrEnum

def parse(s):
    "London to Dublin = 464"
    regex = re.compile(r"(\w+) to (\w+) = (\d+)")
    m = regex.match(s)
    x, y, d = (m.group(1), m.group(2), int(m.group(3)))
    return x, y, d

def minmax(lines, minmax):
    dists = defaultdict(dict)
    for x, y, d in [parse(line) for line in lines]:
        dists[x][y] = d
        dists[y][x] = d
    def route_dist(route):
        return sum(dists[x1][x2] for x1, x2 in pairwise(route))

    return minmax(route_dist(r) for r in permutations(dists.keys()))

def a(lines):
    return minmax(lines, min)

def b(lines):
    return minmax(lines, max)

assert parse("London to Dublin = 464") == ("London", "Dublin", 464)

test_input = """London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141"""

assert a(test_input.splitlines()) == 605

input = open('input/09').read()

print(a(input.splitlines()))
print(b(input.splitlines()))
