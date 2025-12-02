import dataclasses
import functools
import itertools
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


def parse_replacement(s):
    """H => HO"""
    split = s.split(" => ")
    return split[0], split[1]

def parse(replacement_lines):
    replacement_dict = defaultdict(list)
    for line in replacement_lines:
        k, v = parse_replacement(line)
        replacement_dict[k].append(v)
    return replacement_dict

def products_1(replacements, input: str):
    result = set()
    for k in replacements:
        for v in replacements[k]:
            for i in range(len(input) - len(k) + 1):
                if input[i:i+len(k)] == k:
                    result.add(input[:i] + v + input[i+len(k):])
    return result

def shortest_path(fun_neighbours, start, end):
    queue = PrioritizedQueue()
    visited = set()
    queue.add_task(start, 0)
    dist_graph = {start: 0}
    pred_graph = {start: None}
    MAX_DIST = 1E9
    min_length = len(start)
    while v := queue.pop_task():
        dist_v = dist_graph[v]
        if len(v) < min_length - 10:
            min_length = len(v)
            print(min_length, dist_v, v)
        visited.add(v)
        if v == end:
            return dist_v
        ns = fun_neighbours(v)
        for n, dist_v_n in ns:
            if n not in visited:
                new_dist = dist_v + dist_v_n
                queue.add_task(n, new_dist)
                if dist_graph.get(n, MAX_DIST) > new_dist:
                    dist_graph[n] = new_dist
                    pred_graph[n] = v

def b(replacements, medicine):
    reductions = defaultdict(list)
    for k, v in replacements.items():
        for r in v:
            reductions[r].append(k)
    @functools.lru_cache(maxsize=None)
    def fun_neighbours(v):
        return [(p, 1) for p in products_1(reductions, v)]
    return shortest_path(fun_neighbours, medicine, "e")


test_input = """H => HO
H => OH
O => HH""".strip()
replacements = parse(test_input.splitlines())
assert len(products_1(replacements, "HOH")) == 4, products_1(replacements, "HOH")
assert len(products_1(replacements, "HOHOHO")) == 7, products_1(replacements, "HOHOHO")


input = open('input/19').read()
replacement_lines, medicine = input.split("\n\n")
replacements = parse(replacement_lines.splitlines())
print(len(products_1(replacements, medicine)))
print(b(replacements, medicine))