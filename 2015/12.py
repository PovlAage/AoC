import dataclasses
import functools
from collections import defaultdict
from itertools import permutations, pairwise

import numpy as np
import re
from enum import StrEnum

def rec_sum(d, ignore_red):
    if isinstance(d, str):
        return 0
    elif isinstance(d, int):
        return d
    elif isinstance(d, list):
        return sum(rec_sum(e, ignore_red) for e in d)
    elif isinstance(d, dict):
        return 0 if "red" in d.values() and ignore_red else sum(rec_sum(d[k], ignore_red) for k in d)

assert rec_sum([1, 2, [3, 4]], ignore_red=False) == 10
assert rec_sum([1, 2, 3], ignore_red=False) == 6
assert rec_sum({"a":2,"b":4}, ignore_red=False) == 6
assert rec_sum({"a":[-1,1]}, ignore_red=False) == 0
assert rec_sum([-1,{"a":1}], ignore_red=False) == 0
assert rec_sum([], ignore_red=False) == 0
assert rec_sum({}, ignore_red=False) == 0

def parse(json):
    return eval(json)
assert parse("[1, 2, [3, 4]]") == [1, 2, [3, 4]]
assert parse('{"a":2,"b":4}') == {"a":2,"b":4}

input = open('input/12').read()
print(rec_sum(parse(input), ignore_red=False))
print(rec_sum(parse(input), ignore_red=True))