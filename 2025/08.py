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

def verify(actual, expected):
    if actual == expected:
        print("OK", actual)
    else:
        print(f"FAIL {actual}!={expected}")

def read_input() -> str:
    return open(f'input/{day:02}').read().strip()

def read_input_lines() -> str:
    return open(f'input/{day:02}').read().strip().splitlines()

def parse_blocks(text: str):
    blocks = text.split('\n\n')
    return blocks[0].split('\n'), blocks[1].split('\n')


Box = tuple[int, int, int]
CircuitElement = tuple[Box, list[int]]

@dataclass
class Playground:
    boxes: list[Box]
    box_circuit: list[int]
    circuit_boxes: dict[int, list[int]]
    circuit_count: int
    circuit_len: list[int]

    @staticmethod
    def from_boxes(boxes: list[Box]):
        n = len(boxes)
        return Playground(
            boxes=boxes,
            box_circuit=[i for i in range(n)],
            circuit_boxes={},
            circuit_count=n,
            circuit_len=[1] * n,
        )

    def connect(self, bi1, bi2):
        assert bi1 != bi2
        ci1, ci2 = self.box_circuit[bi1], self.box_circuit[bi2]
        if ci1 == ci2:
            # already same circuit
            pass
        else:
            # merge circuits
            if ci1 in self.circuit_boxes and ci2 in self.circuit_boxes:
                # merge existing
                c2 = self.circuit_boxes[ci2]
                for i in c2:
                    self.box_circuit[i] = ci1
                self.circuit_boxes[ci1].extend(c2)
                c2.clear()
                self.circuit_len[ci1] += self.circuit_len[ci2]
                self.circuit_len[ci2] = 0
            elif ci1 in self.circuit_boxes or ci2 in self.circuit_boxes:
                # enlarge existing
                if ci2 in self.circuit_boxes:
                    ci2, ci1 = ci1, ci2
                    bi2, bi1 = bi1, bi2
                self.box_circuit[bi2] = ci1
                self.circuit_boxes[ci1].append(bi2)
                self.circuit_len[ci1] += 1
            else:
                # new circuit
                self.circuit_boxes[ci1] = [bi1, bi2]
                self.circuit_len[ci1] = 2
                self.box_circuit[bi1] = self.box_circuit[bi2] = ci1
            self.circuit_count -= 1

    def get_circuits_by_size(self):
        return sorted(self.circuit_len, reverse=True)

    def connect_shortest_n(self: Playground, n: int):
        sorted_dists = sorted([(dist_sq(self.boxes[i1], self.boxes[i2]), i1, i2) for i1 in range(len(self.boxes)) for i2 in range(len(self.boxes)) if i1 < i2])
        for i1, i2 in ((i1, i2) for _, i1, i2 in sorted_dists[:n]):
            self.connect(i1, i2)

    def connect_until(self: Playground) -> tuple[Box, Box]:
        sorted_dists = sorted([(dist_sq(self.boxes[i1], self.boxes[i2]), i1, i2) for i1 in range(len(self.boxes)) for i2 in range(len(self.boxes)) if i1 < i2])
        for i1, i2 in ((i1, i2) for _, i1, i2 in sorted_dists):
            self.connect(i1, i2)
            if self.circuit_count == 1:
                return self.boxes[i1], self.boxes[i2]
        raise ValueError("Never connected")

def parse_box(line) -> Box:
    return tuple(int(i) for i in line.split(','))

def parse(lines) -> Playground:
    return Playground.from_boxes([parse_box(line) for line in lines])

def dist_sq(b1: Box, b2: Box):
    return sum((w2-w1)**2 for w1, w2 in zip(b1, b2))

def a(input_lines, n_connections):
    circuit = parse(input_lines)
    circuit.connect_shortest_n(n_connections)
    c1, c2, c3 = circuit.get_circuits_by_size()[:3]
    return c1 * c2 * c3

def b(input_lines):
    circuit = parse(input_lines)
    b1, b2 = circuit.connect_until()
    x1, _, _ = b1
    x2, _, _ = b2
    return x1 * x2


example_input = """
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
""".strip().splitlines()
example_circuit = parse(example_input)
example_boxes = example_circuit.boxes
assert example_boxes[0] == (162, 817, 812), example_boxes[0]
example_circuit.connect_shortest_n(1)
assert list(example_circuit.get_circuits_by_size())[:2] == [2, 1], list(example_circuit.get_circuits_by_size())[:2]

example_circuit = parse(example_input)
example_circuit.connect_shortest_n(10)
assert list(example_circuit.get_circuits_by_size())[:5] == [5, 4, 2, 2, 1], list(example_circuit.get_circuits_by_size())[:5]
assert a(example_input, n_connections=10) == 40, a(example_input, 10)
assert b(example_input) == 25272, b(example_input)
verify(a(read_input_lines(), n_connections=1000), 66912)
verify(b(read_input_lines()), 724454082)

print(f"Elapsed: {time() - start_time:.3f}s")
