import collections
import queue
from dataclasses import dataclass, field
import functools
import itertools
from collections import defaultdict
from itertools import permutations, pairwise, count
from math import *
from time import time

import numpy as np
import re
from enum import StrEnum

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

def parse(text: str):
    blocks = parse_blocks(text)
    def parse_range(r):
        return Range(int(r.split('-')[0]), int(r.split('-')[1]))
    ranges = [parse_range(r) for r in blocks[0]]
    ids = [int(id) for id in blocks[1]]
    return ranges, ids


@dataclass(frozen=True, order=True)
class Range:
    a: int
    b: int

    @property
    def length(self):
        return self.b - self.a + 1

    def is_disjoint_from(self, other):
        if other is None:
            return True
        if other < self:
            return other.is_disjoint_from(self)
        assert self.a <= other.a
        return self.b < other.a

    def intersect(self, other):
        if other is None: return None
        if other.a < self.a:
            return other.intersect(self)

        assert self.a <= other.a
        if self.b < other.a:
            return None
        if other.b <= self.b:
            return other
        return Range(other.a, self.b)

assert Range(1, 4).intersect(Range(2, 3)) == Range(2, 3)
assert Range(1, 4).intersect(Range(2, 5)) == Range(2, 4)
assert Range(1, 4).intersect(Range(4, 5)) == Range(4, 4)
assert Range(1, 4).intersect(Range(5, 5)) is None, Range(1, 4).intersect(Range(5, 5))


def verify_sorted_disjoint(xs: list[Range]):
    for x1, x2 in pairwise(xs):
        assert x1.a <= x1.b < x2.a <= x2.b

def sort_and_squash_disjoint(xs: list[Range]) -> list[Range]:
    xs = sorted(xs)
    verify_sorted_disjoint(xs)

    def _append(xs: list[Range], y: Range) -> list[Range]:
        if xs and not xs[-1].is_disjoint_from(y):
            raise ValueError(f"x {y} must be strictly after last xs {xs[-1]}")
        if len(xs) == 0:
            return [y]
        else:
            assert xs[-1].is_disjoint_from(y)
            assert xs[-1].b < y.a
            ys = []
            if xs[-1].b == y.a - 1:
                return xs[:-1] + [Range(xs[-1].a, y.b)]
            else:
                return xs + [y]

    result = []
    for i in range(len(xs)):
        result = _append(result, xs[i])
    return result

@dataclass
class Set1:
    ranges: list[Range]

    @staticmethod
    def empty() -> Set1:
        return Set1(ranges=[])

    @staticmethod
    def from_single(r: Range):
        return Set1(ranges=[] if r is None else [r])

    @staticmethod
    def union_disjoint_2(x: Range, y: Range) -> Set1:
        if x is None: return Set1.from_single(y)
        if y is None: return Set1.from_single(x)
        if y < x:
            return Set1.union_disjoint_2(y, x)
        assert x.is_disjoint_from(y)
        assert x.b < y.a
        if x.b == y.a - 1:
            return Set1.from_single(Range(x.a, y.b))
        else:
            return Set1(ranges=[x, y])

    @staticmethod
    def union_2(x: Range, y: Range) -> Set1:
        if x is None: return Set1.from_single(y)
        i = x.intersect(y)
        if i is None:
            return Set1.union_disjoint_2(x, y)
        else:
            return Set1.from_single(Range(min(x.a, y.a), max(x.b, y.b)))

    @staticmethod
    def union_disjoint_many(xs: list[Range]):
        return Set1(sort_and_squash_disjoint(xs))

    @staticmethod
    def minus_subset(x: Range, s: Range) -> Set1:
        if s is None:
            return Set1.from_single(x)
        if x is None:
            raise ValueError(f'x is None but s is {s}')
        assert x.intersect(s) == s
        if s == x:
            return Set1.empty()
        elif s.a == x.a:
            return Set1.from_single(Range(s.b + 1, x.b))
        elif s.b == x.b:
            return Set1.from_single(Range(x.a, s.a - 1))
        else:
            return Set1.union_disjoint_2(Range(x.a, s.a - 1), Range(s.b + 1, x.b))

    def union_1(self, y: Range) -> Set1:
        xs = self.ranges
        intersecting = [index for index, x in enumerate(xs) if not x.is_disjoint_from(y)]
        if len(intersecting) == 0:
            index = next((i for i, x in enumerate(xs) if y.a > x.a), -1)
            zs = xs[:index] + [y] + xs[index:]
        else:
            i_first, i_last = intersecting[0], intersecting[-1]
            y = Range(min(y.a, xs[i_first].a), max(y.b, xs[i_last].b))
            zs = xs[:i_first] + [y] + xs[i_last + 1:]
        return Set1.union_disjoint_many(zs)


assert Set1.minus_subset(Range(1, 4), None) == Set1.from_single(Range(1, 4))
assert Set1.minus_subset(Range(1, 4), Range(1, 2)) == Set1.from_single(Range(3, 4))
assert Set1.minus_subset(Range(1, 4), Range(2, 4)) == Set1.from_single(Range(1, 1))
assert Set1.minus_subset(Range(1, 5), Range(2, 3)) == Set1.union_disjoint_2(Range(1, 1), Range(4, 5))
assert Set1.union_2(Range(1, 4), Range(6, 7)) == Set1.union_disjoint_2(Range(1, 4), Range(6, 7))
assert Set1.union_2(Range(1, 4), Range(3, 5)) == Set1.from_single(Range(1, 5)), Set1.union_2(Range(1, 4), Range(3, 5))
assert Set1.union_2(Range(1, 4), Range(2, 3)) == Set1.from_single(Range(1, 4))
assert Set1.union_2(Range(1, 2), Range(3, 4)) == Set1.from_single(Range(1, 4)), Set1.union_2(Range(1, 2), Range(3, 4))


def is_fresh(ranges, id):
    for r in ranges:
        if r.a <= id <= r.b:
            return True
    return False

def a(ranges, ids):
    return len([id for id in ids if is_fresh(ranges, id)])
def b(ranges):
    valid_ranges = functools.reduce(Set1.union_1, ranges, Set1.empty())
    return sum(r.length for r in valid_ranges.ranges)

test_input = """
3-5
10-14
16-20
12-18

1
5
8
11
17
32
""".strip()

ranges, ids = parse(test_input)
assert a(ranges, ids) == 3, a(ranges, ids)
assert b(ranges) == 14, b(ranges)

input = read_input()
ranges, ids = parse(input)
verify(a(ranges, ids), 770)
verify(b(ranges), 357674099117260)

print(f"Elapsed: {time() - start_time:.3f}s")
