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

def read_input() -> str:
    return open(f'input/{day:02}').read().strip()

def read_input_lines() -> str:
    return open(f'input/{day:02}').read().strip().splitlines()

def subsets_max(x, k):
    if k == 0 or k > len(x):
        yield ''
    elif k < 0:
        raise ValueError('k must be >= 0')
    else:
        max_digit = max((x[i] for i in range(len(x) - k + 1)))
        for i in range(len(x)):
            if x[i] == max_digit:
                for s in subsets_max(x[i + 1:], k - 1):
                    yield x[i] + s

def subset_max(x, k):
    dq = collections.deque()
    result = ''
    count = 0
    for i, n in enumerate(map(int, x)):
        while dq and dq[-1] < n:
            dq.pop()
        dq.append(n)

        if len(x) - i == k - count:
            result += str(dq.popleft())
            count += 1
        if count == k:
            break
    return result
assert subset_max('987', 2) == '98', subset_max('987', 2)
assert subset_max('978', 2) == '98', subset_max('978', 2)

def joltage(s):
    return int(s)

def max_joltage(bank, l):
    return joltage(subset_max(bank, l))
assert max_joltage('789', 2) == 89

def ab(banks, l):
    return sum(max_joltage(bank, l=l) for bank in banks)
def a(banks):
    return ab(banks, 2)
def b(banks):
    return ab(banks, 12)

test_input = """
987654321111111
811111111111119
234234234234278
818181911112111
""".strip().splitlines()

assert a(test_input) == 357, a(test_input)
assert b(test_input) == 3121910778619, b(test_input)

print(a(read_input_lines()))
print(b(read_input_lines()))

print(f"Elapsed: {time() - start_time:.3f}s")
