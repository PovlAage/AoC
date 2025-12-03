from dataclasses import dataclass, field
import functools
import itertools
from collections import defaultdict
from itertools import permutations, pairwise
from math import *

import numpy as np
import re
from enum import StrEnum

day = int(__file__.rstrip('.py').split('/')[-1])
print("day", day)

def read_input() -> str:
    return open(f'input/{day:02}').read()


def parse(ranges):
    def parse_r(r):
        return int(r.split('-')[0]), int(r.split('-')[1])
    assert parse_r("11-22") == (11, 22)

    return [parse_r(r) for r in ranges.split(',')]
assert parse("11-22") == [(11,22)]
assert parse("11-22,95-115") == [(11,22), (95,115)]

def all_equal(id):
    sid = str(id)
    l = len(sid)
    return all((sid[k] == sid[0] for k in range(1, l)))

def is_invalid_p(id, p):
    sid = str(id)
    l = len(sid)
    if p == l and all_equal(id):
        return True
    elif l % p != 0:
        return False
    else:
        s = l // p
        sequence = sid[:s]
        return all((sid[k*s:k*s+s] == sequence for k in range(1, p)))

primes = [2, 3, 5, 7]
max_id = max((max(r1, r2) for r1, r2 in parse(read_input())))
max_len = len(str(max_id))
print(max_id, max_len)
assert primes[-1] >= max_len // 2

def is_invalid(id, b=False):
    primes_to_use = primes if b else [2]
    return any((is_invalid_p(id, p=p) for p in primes_to_use))

assert is_invalid(55)
assert is_invalid(6464)
assert is_invalid(123123)
assert not is_invalid(1231234)
assert is_invalid(12341234, b=True)
assert is_invalid(123123123, b=True)
assert is_invalid(1212121212, b=True)
assert is_invalid_p(1111111, p=7)
assert is_invalid(1111111, b=True)

def get_invalids(r, b=False):
    start, end = r
    return [id for id in range(start, end + 1) if is_invalid(id, b=b)]
assert get_invalids((11, 22)) == [11, 22]
assert get_invalids((95, 115)) == [99], get_invalids((95, 115))
assert get_invalids((998, 1012)) == [1010]
assert get_invalids((95, 115), b=True) == [99, 111]
assert get_invalids((998, 1012), b=True) == [999, 1010]
assert get_invalids((565653, 565659), b=True) == [565656]
assert get_invalids((824824821, 824824827), b=True) == [824824824]

def ab(input, b):
    return sum((sum(get_invalids(r, b=b)) for r in parse(input)))

test_input = """
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124
"""
assert ab(test_input, b=False) == 1227775554
assert ab(test_input, b=True) == 4174379265
print(ab(read_input(), b=False))
print(ab(read_input(), b=True))