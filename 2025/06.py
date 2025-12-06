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

def parse(input_lines):
    xs = [[int(n) for n in input_lines[k].split()] for k in range(len(input_lines) - 1)]
    ops = [n for n in input_lines[-1].split()]
    result = list(zip(*(xs + [ops])))
    return result

def parse_b(input_lines):
    w = len(input_lines[0])
    assert set(len(l) for l in input_lines[:-1]) == {w}, f"widths must be equal {[len(l) for l in input_lines]}"
    blank_cols = [-1] + [c for c in range(w) if all(l[c] == ' ' for l in input_lines)] + [w]
    problem_cols = list(zip([c + 1 for c in blank_cols[:-1]], blank_cols[1:]))
    def parse_problem(problem_col):
        start, stop = problem_col
        xs = []
        for c in range(start, stop):
            x = 0
            p = 0
            for r in range(len(input_lines) - 2, -1, -1):
                if input_lines[r][c] != ' ':
                    d = int(input_lines[r][c])
                    x += d * 10 ** p
                    p += 1
            xs.append(x)
        problem = (*xs, input_lines[-1][start])
        return problem
    return [parse_problem(pc) for pc in problem_cols]

def calc(problem):
    op = problem[-1]
    xs = problem[:-1]
    if op == '+':
        return functools.reduce(lambda x, y: x + y, xs, 0)
    elif op == '*':
        return functools.reduce(lambda x, y: x * y, xs, 1)
    else:
        raise ValueError(f"Op {op} is not supported")

def ab(lines, b):
    problems = parse_b(lines) if b else parse(lines)
    return sum(calc(p) for p in problems)

test_input = """
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
""".strip().splitlines()

assert(ab(test_input, b=False)) == 4277556
assert(ab(test_input, b=True)) == 3263827
verify(ab(read_input_lines(), b=False), 5667835681547)
verify(ab(read_input_lines(), b=True), 9434900032651)

print(f"Elapsed: {time() - start_time:.3f}s")
