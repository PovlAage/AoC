from dataclasses import dataclass, field
import functools
import itertools
from collections import defaultdict
from itertools import permutations, pairwise
from time import time

import numpy as np
import re
from enum import StrEnum

day = int(__file__.rstrip('.py').split('/')[-1])
print("day", day)
start_time = time()

def read_input() -> str:
    return open(f'input/{day:02}').read()

def parse(instruction):
    direction = -1 if instruction[0] == 'L' else +1
    distance = int(instruction[1:])
    return direction, distance

def a(input: str):
    instructions = [parse(i) for i in input.strip().splitlines()]
    pos = 50
    count = 0
    for direction, distance in instructions:
        pos = (pos + distance * direction) % 100
        if pos == 0:
            count += 1
    return count

def b(input: str):
    instructions = [parse(i) for i in input.strip().splitlines()]
    pos = 50
    count = 0
    for direction, distance in instructions:
        assert distance > 0
        count += distance // 100
        distance = distance % 100
        if pos == 0:
            pos = (pos + distance * direction) % 100
        else:
            pos = (pos + distance * direction)
            if pos == 0 or pos != pos % 100:
                count += 1
            pos = pos % 100
    return count

test_input = """
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
"""
assert a(test_input) == 3
assert b(test_input) == 6

print(a(read_input()), 1132)
print(b(read_input()), 6623)

print(f"Elapsed: {time() - start_time:.3f}s")
