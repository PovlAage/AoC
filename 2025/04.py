import collections
import queue
from dataclasses import dataclass, field
import functools
import itertools
from collections import defaultdict
from itertools import permutations, pairwise
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

n8 = [(dy, dx) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if (dx or dy)]

def parse(lines) -> np.ndarray:
    shape = (len(lines) + 2, len(lines[0]) + 2)
    ydim, xdim = shape
    arr = np.zeros(shape=shape, dtype=int)
    for y in range(1, ydim - 1):
        for x in range(1, xdim - 1):
            arr[y, x] = 1 if lines[y - 1][x - 1] == '@' else 0
    return arr

def set_edge_zero(arr):
    arr[[0, -1], :] = 0
    arr[:, [0, -1]] = 0

def get_neighbour_array(arr: np.ndarray) -> np.ndarray:
    n_arr = np.zeros_like(arr)
    for n in n8:
        n_arr += np.roll(arr, shift=n, axis=(0, 1))
    return n_arr

def count_iterated_remove(arr: np.ndarray, n_arr: np.ndarray, iterations=1):
    remove_count = 0
    while True and iterations != 0:
        iterations -= 1
        arr_accessible = np.logical_and(arr, np.less(n_arr, 4))
        count_accessible = np.count_nonzero(arr_accessible)
        if not count_accessible:
            break
        remove_count += count_accessible
        arr -= arr_accessible
        for n in n8:
            n_arr -= np.roll(arr_accessible, shift=n, axis=(0, 1))
    return remove_count

def ab(lines, b):
    arr = parse(lines)
    n_arr = get_neighbour_array(arr)
    return count_iterated_remove(arr, n_arr, -1 if b else 1)

def a(lines):
    return ab(lines, b=False)

def b(lines):
    return ab(lines, b=True)

test_input = """
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
""".strip().splitlines()

test_lines = test_input
assert a(test_lines) == 13
assert b(test_lines) == 43, b(test_lines)

input_lines = read_input_lines()
verify(a(input_lines), 1344)
verify(b(input_lines), 8112)

print(f"Elapsed: {time() - start_time:.3f}s")
