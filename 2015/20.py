import dataclasses
import functools
import itertools
from math import *
from collections import defaultdict
from itertools import permutations, pairwise
from priorityq import PrioritizedQueue

import numpy as np
import re
from enum import StrEnum

day = int(__file__.rstrip('.py').split('/')[-1])
print("day", day)

def read_input():
    return open(f'input/{day}').read()

def presents(house):
    count = 0
    for k in range(1, house + 1):
        if house % k == 0:
            count += k
    return 10 * count
assert presents(1) == 10
assert presents(2) == 30
assert presents(3) == 40
assert presents(4) == 70
assert presents(5) == 60
assert presents(6) == 120
assert presents(7) == 80
assert presents(8) == 150
assert presents(9) == 130

primes = [2, 3, 5, 7, 11, 13, 17, 19]

def calc_dict(d: dict[int, int]):
    n = 1
    v = 1
    for k in d:
        n *= k ** d[k]
        fac = sum((k ** j for j in range(d[k] + 1)))
        v *= fac
    return 10 * v
assert calc_dict({}) == 10
assert calc_dict({2: 0}) == 10, calc_dict({2: 0})
assert calc_dict({2: 0, 3: 0}) == 10
assert calc_dict({2: 1}) == 30, calc_dict({2: 1})
assert calc_dict({3: 1}) == 40
assert calc_dict({2: 2}) == 70
assert calc_dict({2: 1, 3: 1}) == 120
assert calc_dict({2: 3}) == 150

def a(input):
    def get_max_pow(p):
        for max_pow in itertools.count(0):
            if calc_dict({p: max_pow - 1}) < input:
                continue
            n = p ** max_pow
            presents = calc_dict({p: max_pow})
            print(f"max_pow {p}={max_pow}, n={n}, presents={presents}")
            return n, presents

    best_n = 1e15
    for p in primes:
        n, presents = get_max_pow(p)
        assert presents >= input
        if n < best_n:
            print("Best: ", n)
        best_n = min(best_n, n)


input = 36_000_000
a(input)
