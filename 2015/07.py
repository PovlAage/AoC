import dataclasses
import functools

import numpy as np
import re
from enum import StrEnum

class Circuit:
    def __init__(self, wires):
        self.wires = wires
        self.eval = functools.lru_cache(maxsize=16)(self.eval)

    def eval(self, x):
        try:
            x = int(x)
            return x
        except ValueError:
            return self.wires[x].eval(self)

def eval(x, circuit):
    return circuit.eval(x)

@dataclasses.dataclass
class Signal:
    source: str | int

    @staticmethod
    def try_parse(s):
        expr = r'^(\w+)$'
        m = re.match(expr, s)
        if not m:
            return None
        source = m.group(1)
        try:
            source = int(source)
        except ValueError:
            pass
        return Signal(source)

    def eval(self, circuit):
        return self.source if isinstance (self.source, int) else eval(self.source, circuit)

@dataclasses.dataclass
class AndGate:
    x: str
    y: str

    @staticmethod
    def try_parse(s):
        expr = rf'^(\w+) AND (\w+)$'
        m = re.match(expr, s)
        return AndGate(x=m.group(1), y=m.group(2)) if m else None

    def eval(self, circuit):
        return eval(self.x, circuit) & eval(self.y, circuit)


@dataclasses.dataclass
class OrGate:
    x: str
    y: str

    @staticmethod
    def try_parse(s):
        expr = rf'^(\w+) OR (\w+)$'
        m = re.match(expr, s)
        return OrGate(x=m.group(1), y=m.group(2)) if m else None

    def eval(self, circuit):
        return eval(self.x, circuit) | eval(self.y, circuit)

@dataclasses.dataclass
class NotGate:
    x: str

    @staticmethod
    def try_parse(s):
        expr = rf'^NOT (\w+)$'
        m = re.match(expr, s)
        return NotGate(x=m.group(1)) if m else None

    def eval(self, circuit):
        return ~eval(self.x, circuit)


@dataclasses.dataclass
class LshiftGate:
    x: str
    d: int

    @staticmethod
    def try_parse(s):
        expr = rf'^(\w+) LSHIFT (\d+)$'
        m = re.match(expr, s)
        return LshiftGate(x=m.group(1), d=int(m.group(2))) if m else None

    def eval(self, circuit):
        return eval(self.x, circuit) << self.d

@dataclasses.dataclass
class RshiftGate:
    x: str
    d: int

    @staticmethod
    def try_parse(s):
        expr = rf'^(\w+) RSHIFT (\d+)$'
        m = re.match(expr, s)
        return RshiftGate(x=m.group(1), d=int(m.group(2))) if m else None

    def eval(self, circuit):
        return eval(self.x, circuit) >> self.d

def parse(instruction):
    """
    123 -> x means that the signal 123 is provided to wire x.
    x AND y -> z means that the bitwise AND of wire x and wire y is provided to wire z.
    p LSHIFT 2 -> q means that the value from wire p is left-shifted by 2 and then provided to wire q.
    NOT e -> f means that the bitwise complement of the value from wire e is provided to wire f.
    """
    try:
        s, target = instruction.split(' -> ')
    except:
        raise ValueError(f'Invalid instruction: {instruction}')
    gate = Signal.try_parse(s) or AndGate.try_parse(s) or OrGate.try_parse(s) or NotGate.try_parse(s) or LshiftGate.try_parse(s) or RshiftGate.try_parse(s)
    if not gate:
        raise ValueError(f'Invalid instruction: {instruction}')
    return gate, target
assert parse('123 -> x') == (Signal(123), 'x')
assert parse('x AND y -> z') == (AndGate('x', 'y'), 'z')
assert parse('p LSHIFT 2 -> q') == (LshiftGate('p', 2), 'q')
assert parse('NOT e -> f') == (NotGate('e'), 'f')

def parse_circuit(lines):
    instructions = [parse(line) for line in lines]
    wires = {x: gate for gate, x in instructions}
    return Circuit(wires)


circuit = parse_circuit("""123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i""".splitlines())
assert eval('d', circuit) == 72
input = open('input/07').read()
circuit = parse_circuit(input.splitlines())

signal_a = eval('a', circuit)
print(signal_a)
circuit.wires['b'] = Signal(signal_a)
circuit_b = Circuit(circuit.wires)
print(eval('a', circuit_b))

