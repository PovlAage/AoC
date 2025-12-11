import collections
import queue
from dataclasses import dataclass, field
import functools
import itertools
from collections import defaultdict
from itertools import permutations, pairwise
from math import *
from time import time
from ortools.linear_solver import pywraplp

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

@dataclass(frozen=True)
class Machine:
    lights: int
    buttons: list[int]

    def is_solution(self, button_presses: list[int]):
        button_effects = [self.buttons[bp] for bp in button_presses]
        return self.lights == functools.reduce(lambda a, b: a ^ b, button_effects, 0)

@dataclass(frozen=True)
class MachineJoltage:
    buttons: list[list[int]]
    joltage_requirements: list[int]

    def is_solution(self, button_presses: list[int]):
        j = self.joltage_requirements.copy()
        for bp in button_presses:
            for bbb in self.buttons[bp]:
                j[bbb] -= 1
                if j[bbb] < 0:
                    return False
        if sum(j) == 0:
            return True

def parse_light_spec(s: str) -> int:
    bits = 0
    for k in range(0, len(s) - 2):
        bit = 1 if s[k + 1] == '#' else 0
        bits += bit * 2 ** k
    return bits
assert parse_light_spec("[.##.]") == 6

def parse_button_spec(s: str) -> int:
    numbers = list(map(int, s.strip("()").split(",")))
    return sum((2**k for k in numbers))
assert parse_button_spec("(3)") == 2**3
assert parse_button_spec("(0,1)") == 2**0 + 2**1

def parse_button_spec_b(s: str) -> list[int]:
    return list(map(int, s.strip("()").split(",")))
assert parse_button_spec_b("(3)") == [3]
assert parse_button_spec_b("(0,1)") == [0, 1]

def parse_joltage_requirement_spec(s: str) -> int:
    return list(map(int, s.strip("{}").split(",")))
assert parse_joltage_requirement_spec("{3,5,4,7}") == [3, 5, 4, 7]

def parse_machine(s: str):
    # [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
    light_spec, *button_specs = s.split(' ')
    button_specs, joltage = button_specs[:-1], button_specs[-1]
    lights = parse_light_spec(light_spec)
    buttons = [parse_button_spec(s) for s in button_specs]
    joltage_requirements = parse_joltage_requirement_spec(joltage)
    return Machine(lights=lights, buttons=buttons)
assert parse_machine("[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}").lights == 2+4
assert parse_machine("[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}").buttons[:3] == [2**3, 2**1 + 2**3, 2**2]

def parse_machine_b(s: str):
    # [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
    light_spec, *button_specs = s.split(' ')
    button_specs, joltage = button_specs[:-1], button_specs[-1]
    buttons = [parse_button_spec_b(s) for s in button_specs]
    joltage_requirements = parse_joltage_requirement_spec(joltage)
    return MachineJoltage(buttons=buttons, joltage_requirements=joltage_requirements)
assert parse_machine_b("[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}").buttons[:3] == [[3], [1, 3], [2]]
assert parse_machine_b("[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}").joltage_requirements == [3, 5, 4, 7]

def parse(lines: list[str], b):
    return [parse_machine_b(s) if b else parse_machine(s) for s in lines]

def parse_joltage(lines: list[str]) -> list[MachineJoltage]:
    return [parse_machine_b(s) for s in lines]

def shortest(m: Machine):
    for l in range(1, len(m.buttons) + 1):
        for comb in itertools.combinations(range(len(m.buttons)), l):
            if m.is_solution(comb):
                return l
    raise ValueError("No solution")


@functools.cache
def partitions(total, count):
    if count == 0:
        return ((),)
    elif count == 1:
        return ((total,),)
    else:
        out = []
        for x in range(total + 1):
            for p in partitions(total - x, count - 1):
                out.append((x,) + p)
        return tuple(out)

assert partitions(0, 0) == ((),), partitions(0, 0)
assert partitions(0, 1) == ((0,),)
assert partitions(0, 2) == ((0, 0),)
assert partitions(3, 0) == ((),)
assert partitions(3, 1) == ((3,),)
assert partitions(3, 2) == ((0, 3), (1, 2), (2, 1), (3, 0))
assert partitions(1, 3) == ((0, 0, 1), (0, 1, 0), (1, 0, 0))

call_count = 0
def shortest_b(machine: MachineJoltage, verbose=False):
    global call_count
    if verbose: print(call_count, machine)
    call_count += 1
    jcount, bcount = len(machine.joltage_requirements), len(machine.buttons)
    req_j = np.array(machine.joltage_requirements, dtype=int)
    button_arr_2 = np.zeros(shape=(bcount, jcount), dtype=int)
    for bi in range(bcount):
        for ji in machine.buttons[bi]:
            button_arr_2[bi, ji] = 1


    A = np.matrix(button_arr_2).transpose()
    b = req_j
    m, n = A.shape

    solver = pywraplp.Solver.CreateSolver("CBC")
    x = [solver.IntVar(0, solver.infinity(), f"x{i}") for i in range(n)]
    for i in range(m):
        solver.Add(sum(A[i, j] * x[j] for j in range(n)) == b[i])
    solver.Minimize(solver.Sum(x))

    status = solver.Solve()
    if status == solver.OPTIMAL:
        s = sum([xi.solution_value() for xi in x])
        assert int(s) == s
        return int(s)
    else:
        raise ValueError("No solution")

def a(lines: list[str]):
    return sum(shortest(m) for m in parse(lines, b=False))

def b(lines: list[str], verbose=False):
    return sum(shortest_b(m, verbose=verbose) for m in parse(lines, b=True))

test_input = """
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
""".strip().splitlines()

test_machines = parse(test_input, b=False)
assert test_machines[0].lights == 2**1 + 2**2
assert test_machines[0].is_solution([4, 5])
assert test_machines[0].is_solution([0, 1, 2])
assert test_machines[0].is_solution([1, 3, 5, 5])
assert test_machines[0].is_solution([0, 2, 3, 4, 5])
assert not test_machines[0].is_solution([4])
assert not test_machines[0].is_solution([])
assert shortest(test_machines[0]) == 2
assert shortest(test_machines[1]) == 3
assert shortest(test_machines[2]) == 2

test_machines_b = parse(test_input, b=True)
assert test_machines_b[0].is_solution([0, 1, 1, 1, 3, 3, 3, 4, 5, 5])
assert test_machines_b[1].is_solution([0, 0, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3])
assert test_machines_b[2].is_solution([0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 3])
assert shortest_b(test_machines_b[0]) == 10, shortest_b(test_machines_b[0])
assert shortest_b(test_machines_b[1]) == 12, shortest_b(test_machines_b[1])
assert shortest_b(test_machines_b[2]) == 11, shortest_b(test_machines_b[2])

assert a(test_input) == 7
assert b(test_input) == 33

verify(a(read_input_lines()), 401)
verify(b(read_input_lines()), 15017)

print(f"Elapsed: {time() - start_time:.3f}s")
