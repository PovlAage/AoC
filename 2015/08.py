import dataclasses
import functools

import numpy as np
import re
from enum import StrEnum

def unquote(s):
    return s[1:-1]

def strlen(s):
    code_len = len(s)
    s = unquote(s)
    mem_len = 0
    i = 0
    while i < len(s):
        if s[i] == '\\':
            if s[i+1] == '\\' or s[i+1] == '"':
                i += 1
            elif s[i+1] == 'x':
                i += 3
            else:
                assert False
        mem_len += 1
        i += 1
    return code_len, mem_len

def encode(s):
    return '"' + s.replace('\\', '\\\\').replace('"', r'\"') + '"'

def a(strings):
    lengths = [strlen(s) for s in strings]
    return sum(code_len - mem_len for code_len, mem_len in lengths)


s1 = '""'
s2 = '"abc"'
s3 = '"aaa\\"aaa"'
s4 = r'"\x27"'
assert strlen(s1) == (2, 0)
assert strlen(s2) == (5, 3)
assert strlen(s3) == (10, 7)
assert strlen(s4) == (6, 1)
assert a([s1, s2, s3, s4]) == 12

assert encode(s1) == r'"\"\""'
assert encode(s2) == r'"\"abc\""'
assert encode(s3) == r'"\"aaa\\\"aaa\""'
assert encode(s4) == r'"\"\\x27\""'

input = open('input/08').read()

print(a(input.splitlines()))
print(sum((len(encode(s))-len(s) for s in input.splitlines())))
