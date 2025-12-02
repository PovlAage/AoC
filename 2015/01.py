def a(s):
    floor = 0
    for i in range(len(s)):
        ss = s[i]
        if ss == '(':
            floor += 1
        elif ss == ')':
            floor -= 1
    return floor

def b(s):
    floor = 0
    for i in range(len(s)):
        ss = s[i]
        if ss == '(':
            floor += 1
        elif ss == ')':
            floor -= 1
        if floor == -1:
            return i + 1
    return floor

assert a('(())') == 0
assert a('()()') == 0
assert a('(((') == 3
assert a('))(') == -1
assert a(')))')
assert a('))(((((') == 3

input = open('input/01').read()

print(a(input))

assert b(')') == 1
assert b('()())') == 5

print(b(input))
