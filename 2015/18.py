import dataclasses
import functools
import itertools
from collections import defaultdict
from itertools import permutations, pairwise

import numpy as np
import re
from enum import StrEnum

day = int(__file__.rstrip('.py').split('/')[-1])
print("day", day)

def read_input():
    return open(f'input/{day}').read()

def parse(lines):
    arr = np.zeros(dtype=np.int8, shape=(len(lines) + 2, len(lines[0]) + 2))
    for x in range(len(lines[0])):
        for y in range(len(lines)):
            arr[y + 1, x + 1] = lines[y][x] == '#'
    return arr

def dump(arr):
    print(arr)


neighbours_8 = [(dx, dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if not dx == dy == 0]
assert len(neighbours_8) == 8

def iter_1(arr, corners_always_on):
    ydim, xdim = arr.shape
    ydim -= 2
    xdim -= 2

    def set_corners_on(arr):
        arr[1, 1] = 1
        arr[1, xdim] = 1
        arr[ydim, 1] = 1
        arr[ydim, xdim] = 1

    if corners_always_on:
        set_corners_on(arr)
    arr_2 = np.zeros_like(arr)
    for x in range(1, xdim + 1):
        for y in range(1, ydim + 1):
            neighbour_count = sum(arr[y + dy, x + dx] for dx, dy in neighbours_8)
            if arr[y, x] == 1:
                arr_2[y, x] = 1 if neighbour_count in [2, 3] else 0
            else:
                arr_2[y, x] = 1 if neighbour_count == 3 else 0

    if corners_always_on:
        set_corners_on(arr_2)
    return arr_2

def iter_n(arr, n, corners_always_on):
    for _ in range(n):
        arr = iter_1(arr, corners_always_on=corners_always_on)
    return arr

test_input = """
.#.#.#
...##.
#....#
..#...
#.#..#
####..
""".strip()

arr = parse(test_input.splitlines())
assert np.sum(iter_n(arr, 4, corners_always_on=False)) == 4
assert np.sum(iter_n(arr, 5, corners_always_on=True)) == 17

input = read_input()
arr = parse(input.splitlines())
print(np.sum(iter_n(arr, 100, corners_always_on=False)))
print(np.sum(iter_n(arr, 100, corners_always_on=True)))