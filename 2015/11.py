import dataclasses
import functools
from collections import defaultdict
from itertools import permutations, pairwise

import numpy as np
import re
from enum import StrEnum

def has_straight_3(s):
    for i in range(len(s)-2):
        if ord(s[i]) == ord(s[i+1]) - 1 == ord(s[i+2]) - 2:
            return True
    return False
assert has_straight_3('xbcdx')
assert not has_straight_3('xabdx')

def has_no_iol(s):
    chars = 'iol'
    for c in chars:
        if c in s:
            return False
    return True
assert has_no_iol('hjkmmn')
assert not has_no_iol('aix')

def has_2_pairs(s):
    count = 0
    used = set()
    for i in range(len(s)-1):
        if s[i] == s[i+1] and s[i] not in used:
            count += 1
            used.add(s[i])
            i += 2
        if count >= 2:
            return True
    return False

def is_valid(s):
    return has_straight_3(s) and has_no_iol(s) and has_2_pairs(s)

def a(s):
    def inc(c):
        return chr(ord(c) + 1) if c != 'z' else 'a'

    def incs(s):
        digit = len(s) - 1
        d = inc(s[digit])
        return s[:-1] + d if d != 'a' else incs(s[:-1]) + 'a'

    s = incs(s)
    while not is_valid(s):
        s = incs(s)

    return s

assert has_2_pairs('xxyy')
assert has_2_pairs('xxayy')
assert not has_2_pairs('xxx')
assert not has_2_pairs('xxaxx')

print(a('hxbxwxba'))
print(a(a('hxbxwxba')))