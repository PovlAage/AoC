import numpy as np
import re
from enum import StrEnum

class Command(StrEnum):
    ON = 'turn on'
    OFF = 'turn off'
    TOGGLE = 'toggle'

def parse(instruction):
    # turn on 0,0 through 999,999
    expr = rf'^({Command.ON}|{Command.OFF}|{Command.TOGGLE}) (\d+),(\d+) through (\d+),(\d+)$'
    m = re.match(expr, instruction)
    if not m:
        raise ValueError(f'Invalid instruction: {instruction}')
    return m.group(1), (int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5)))
assert parse('turn on 0,0 through 999,999') == (Command.ON, (0, 0, 999, 999))
assert parse('turn off 0,0 through 999,999') == (Command.OFF, (0, 0, 999, 999))
assert parse('toggle 0,0 through 999,999') == (Command.TOGGLE, (0, 0, 999, 999))

def a(lines):
    grid = np.array([[0 for _ in range(1000)] for _ in range(1000)])
    for instruction in lines:
        command, (x1, y1, x2, y2) = parse(instruction)
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                if command == Command.ON:
                    grid[x, y] = 1
                elif command == Command.OFF:
                    grid[x, y] = 0
                elif command == Command.TOGGLE:
                    grid[x, y] ^= 1
    return np.sum(grid)

def b(lines):
    grid = np.array([[0 for _ in range(1000)] for _ in range(1000)])
    for instruction in lines:
        command, (x1, y1, x2, y2) = parse(instruction)
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                if command == Command.ON:
                    grid[x, y] += 1
                elif command == Command.OFF:
                    grid[x, y] -= 1
                elif command == Command.TOGGLE:
                    grid[x, y] += 2
        grid = np.clip(grid, 0, None)
    return np.sum(grid)

assert a(['turn on 0,0 through 999,999']) == 1000000
assert a(['toggle 0,0 through 999,0']) == 1000
assert a(2 * ['toggle 0,0 through 999,0']) == 0

assert b(['turn on 0,0 through 0,0']) == 1
assert b(['turn off 0,0 through 0,0']) == 0
assert b(['toggle 0,0 through 999,999']) == 2000000

input = open('input/06').read()
print(a(input.splitlines()))
print(b(input.splitlines()))

