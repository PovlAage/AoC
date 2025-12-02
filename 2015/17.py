import dataclasses
import functools
import itertools
from collections import defaultdict
from itertools import permutations, pairwise

import numpy as np
import re
from enum import StrEnum

def partitions(total, containers):
    def loop(total, containers):
        if total == 0:
            yield []
        elif len(containers) == 0:
            pass
        else:
            remaining_containers = [x for x in containers if x <= total]
            for i in range(len(remaining_containers)):
                x = remaining_containers[i]
                for p in loop(total - x, remaining_containers[i+1:]):
                    yield [x] + p
    return loop(total, sorted(containers))
test_input = [5, 5, 10, 15, 20]
assert list(partitions(25, test_input)) == [[5, 5, 15], [5, 20], [5, 20], [10, 15]], list(partitions(25, test_input))

def a(containers, amount=150):
    return len(list(partitions(amount, containers)))

def b(containers, amount=150):
    ps = list(partitions(amount, containers))
    min_length = min(len(p) for p in ps)
    return len([p for p in ps if len(p) == min_length])

assert a(test_input, amount=25) == 4
assert b(test_input, amount=25) == 3

input = open('input/17').read()
containers = [int(line) for line in input.splitlines()]
print(a(containers))
print(b(containers))
