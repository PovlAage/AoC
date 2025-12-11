import collections
import queue
from dataclasses import dataclass, field
import functools
import itertools
from collections import defaultdict
from itertools import permutations, pairwise
from math import *
from time import time
from typing import Tuple

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

Device = Tuple[str, list[str]]

def parse_device(s: str) -> Device:
    name, soutputs = s.split(': ')
    outputs = soutputs.split()
    return name, outputs
assert parse_device("aaa: you hhh") == ("aaa", ["you", "hhh"])

def parse(input_lines):
    return [parse_device(s) for s in input_lines]

def count_paths(devices: list[Device], start, finish, avoid=None):
    m = {name: outputs for name, outputs in devices}
    cache = {}
    def loop(current: str):
        if current == avoid:
            return 0
        if current == finish:
            return 1
        elif current == "out":
            return 0
        s = 0
        for n in m[current]:
            if n not in cache:
                cache[n] = loop(current=n)
            s += cache[n]
        return s
    return loop(current=start)

def a(input_lines):
    devices = parse(input_lines)
    return count_paths(devices, "you", "out")

def b(input_lines):
    devices = parse(input_lines)
    dac_fft = count_paths(devices, "dac", "fft")  # 0
    svr_dac = count_paths(devices, "svr", "dac", avoid="fft")
    fft_out = count_paths(devices, "fft", "out", avoid="dac")
    dac_out = count_paths(devices, "dac", "out")  # 9676
    svr_fft = count_paths(devices, "svr", "fft", avoid="dac")
    fft_dac = count_paths(devices, "fft", "dac", avoid="svr")
    return svr_dac * dac_fft * fft_out + svr_fft * fft_dac * dac_out

test_input = """
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
""".strip().splitlines()

test_input_b = """
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
""".strip().splitlines()

assert len(parse(test_input)) == 10

assert a(test_input) == 5
assert b(test_input_b) == 2
verify(a(read_input_lines()), 643)
verify(b(read_input_lines()), 417190406827152)

print(f"Elapsed: {time() - start_time:.3f}s")
