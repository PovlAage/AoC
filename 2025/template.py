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

def read_input() -> str:
    return open(f'input/{day:02}').read().strip()

def read_input_lines() -> str:
    return open(f'input/{day:02}').read().strip().splitlines()

test_input = """
""".strip().splitlines()

print(f"Elapsed: {time() - start_time:.3f}s")
