input = open('input/02').read().splitlines()

def parse(s):
    return tuple(sorted(int(x) for x in s.split('x')))

def a(s):
    x, y, z = parse(s)
    return 3 * x * y + 2 * x * z + 2 * y * z

def b(s):
    x, y, z = parse(s)
    return 2 * x + 2 * y + x * y * z

assert a('2x3x4') == 58
assert a('1x1x10') == 43

print(sum((a(line) for line in input)))

assert b('2x3x4') == 34
assert b('1x1x10') == 14

print(sum((b(line) for line in input)))

