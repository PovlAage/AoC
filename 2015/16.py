import dataclasses
import functools
import itertools
from collections import defaultdict
from itertools import permutations, pairwise

import numpy as np
import re
from enum import StrEnum

@dataclasses.dataclass(frozen=True)
class Sue:
    number: int
    stats: dict[str, int]

def parse_stat(s):
    return s.split(": ")[0], int(s.split(": ")[1])

def parse(s):
    """Sue 190: akitas: 5, cars: 5, cats: 6"""
    name, stats_str = s.split(": ", maxsplit=1)
    number = int(name.split(' ')[1])
    stats = {parse_stat(stats_str)[0]: parse_stat(stats_str)[1] for stats_str in stats_str.split(", ")}
    return Sue(number=number, stats=stats)

sue190 = parse("Sue 190: akitas: 5, cars: 5, cats: 6")
assert sue190 == Sue(number=190, stats={"akitas": 5, "cars": 5, "cats": 6}), sue190

def is_match_a(info, sue: Sue):
    for k in sue.stats:
        if k in info and info[k] != sue.stats[k]:
            return False
    return True

def is_match_b(info, sue: Sue):
    for k in sue.stats:
        if k in info:
            if k in ["cats", "trees"]:
                if not sue.stats[k] > info[k]: return False
            elif k in ["goldfish", "pomeranians"]:
                if not sue.stats[k] < info[k]: return False
            elif sue.stats[k] != info[k]:
                return False
    return True

assert is_match_a({"cars": 5, "cats": 6}, sue190)
assert is_match_a({"perfumes": 4}, sue190)
assert not is_match_a({"cars": 0}, sue190)

assert is_match_b({"cars": 5, "cats": 5}, sue190)
assert not is_match_b({"cars": 5, "cats": 6}, sue190)

def ab(sues, info, is_match):
    matches = [sue for sue in sues if is_match(info, sue)]
    assert len(matches) == 1
    return matches[0].number

info_lines = """children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1"""
info = {parse_stat(line)[0]: parse_stat(line)[1] for line in info_lines.splitlines()}
input = open('input/16').read()
sues = [parse(line) for line in input.splitlines()]
print(ab(sues, info, is_match_a))
print(ab(sues, info, is_match_b))
