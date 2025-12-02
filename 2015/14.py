import dataclasses
import functools
from collections import defaultdict
from itertools import permutations, pairwise

import numpy as np
import re
from enum import StrEnum

@dataclasses.dataclass(frozen=True)
class Reindeer:
    name: str
    speed: int
    duration: int
    rest: int

@dataclasses.dataclass
class State:
    flying: bool
    duration: int
    distance: int
    score: int

def parse(s):
    """Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds."""
    regex = re.compile(r"(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.")
    m = regex.match(s)
    if not m:
        raise ValueError(f'Invalid reindeer: {s}')
    return Reindeer(name=m.group(1), speed=int(m.group(2)), duration=int(m.group(3)), rest=int(m.group(4)))
comet = parse("Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.")
dancer = parse("Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.")
assert comet == Reindeer(name="Comet", speed=14, duration=10, rest=127)
assert dancer == Reindeer("Dancer", 16, 11, 162)

def race(reindeer: list[Reindeer], total_time):
    states = {r.name: State(flying=True, duration=0, distance=0, score=0) for r in reindeer}
    t = 0
    while t < total_time:
        leading_dist = -1
        for r in reindeer:
            state = states[r.name]
            state.duration += 1
            state.distance += r.speed if state.flying else 0
            if state.duration == (r.duration if state.flying else r.rest):
                state.flying = not state.flying
                state.duration = 0
            if state.distance > leading_dist:
                leading_dist = state.distance
        for state in states.values():
            if state.distance == leading_dist:
                state.score += 1
        t += 1
    return states

def a(reindeer: list[Reindeer], total_time):
    end_states = race(reindeer, total_time)
    return max(state.distance for state in end_states.values())

def b(reindeer: list[Reindeer], total_time):
    end_states = race(reindeer, total_time)
    return max(state.score for state in end_states.values())

assert a([comet, dancer], total_time=1000) == 1120
assert b([comet, dancer], total_time=1000) == 689

input = open('input/14').read()
print(a([parse(line) for line in input.splitlines()], total_time=2503))
print(b([parse(line) for line in input.splitlines()], total_time=2503))
