import dataclasses
import functools
from collections import defaultdict
from itertools import permutations, pairwise

import numpy as np
import re
from enum import StrEnum

def parse(s):
    """Alice would gain 54 happiness units by sitting next to Bob."""
    regex = re.compile(r"(\w+) would (\w+) (\d+) happiness units by sitting next to (\w+).")
    m = regex.match(s)
    delta = int(m.group(3)) if m.group(2) == "gain" else -int(m.group(3))
    return m.group(1), m.group(4), delta
assert parse("Alice would gain 54 happiness units by sitting next to Bob.") == ("Alice", "Bob", 54)
assert parse("Bob would lose 7 happiness units by sitting next to Carol.") == ("Bob", "Carol", -7)

def a(input, extra=None):
    config = defaultdict(dict)
    for x, y, d in [parse(s) for s in input]:
        config[x][y] = d
    def evaluate(seating):
        def symm(x, y):
            if x == extra or y == extra:
                return 0
            return config[x][y] + config[y][x]
        s = sum(symm(x, y) for x, y in pairwise(seating))
        s += symm(seating[-1], seating[0])
        return s
    names = list(config.keys())
    if extra is None:
        first = names[0]
        return max(evaluate([first] + list(p)) for p in permutations(names[1:]))
    else:
        first = extra
        return max(evaluate([first] + list(p)) for p in permutations(names))

test_input = """Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol."""

assert a(test_input.splitlines()) == 330

input = open('input/13').read()
print(a(input.splitlines()))
print(a(input.splitlines(), extra="Self"))

