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

from numpy.ma.core import indices

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


def indices_of(l: str, char: str) -> set[int]:
    return set([j for j in range(len(l)) if l[j] == char])

def a(lines: list[str]):
    beams = indices_of(lines[0], 'S')
    split_count = 0
    for i in range(1, len(lines)):
        l = lines[i]
        splitters = indices_of(l, '^')
        splits = beams.intersection(splitters)
        non_splits = beams.difference(splitters)
        split_count += len(splits)
        beams = non_splits | set(b - 1 for b in splits) | set(b + 1 for b in splits)
    return split_count

def b(lines: list[str]):
    w = len(lines[0])
    beams = [1 if c == "S" else 0 for c in lines[0]]
    next_beams = [0] * w
    for i in range(1, len(lines)):
        splitters = [1 if c == "^" else 0 for c in lines[i]]
        for i in range(w):
            # continuing beams
            next_beams[i] = beams[i] if not splitters[i] else 0
        for i in range(w):
            if splitters[i]:
                # splitting beams
                if i > 0:
                    next_beams[i-1] += beams[i]
                if i < len(lines) - 1:
                    next_beams[i+1] += beams[i]
        beams, next_beams = next_beams, beams
    return sum(beams)

test_input = """
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
""".strip().splitlines()

assert a(test_input) == 21, a(test_input)
assert b(test_input) == 40, b(test_input)
verify(a(read_input_lines()), 1560)
verify(b(read_input_lines()), 25592971184998)

print(f"Elapsed: {time() - start_time:.3f}s")
