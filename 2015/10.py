import dataclasses
import functools
from collections import defaultdict
from itertools import permutations, pairwise

import numpy as np
import re
from enum import StrEnum

def say(n, _=None):
    n = str(n)
    i = 0
    result = ""
    while i < len(n):
        j = 0
        while j < len(n) - i and n[i] == n[i+j]:
            j += 1
        result += str(j) + n[i]
        i += j
    return result

def say_many(n, times):
    return functools.reduce(say, range(times), str(n))

def ab(n, k):
    return len(say_many(n, k))

assert say(211) == "1221"
assert say_many(211, 1) == "1221"
assert say_many(1, 1) == "11"
assert say_many(1, 2) == "21"
assert say_many(1, 3) == "1211"
assert say_many(1, 4) == "111221"
assert say_many(1, 5) == "312211"

assert ab(1321131112, 40) == 492982
assert ab(1321131112, 50) == 6989950
