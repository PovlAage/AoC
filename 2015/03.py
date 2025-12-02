def visited(input):
    visited = set()
    pos = (0, 0)
    visited.add(pos)
    dirs = {'<': (-1, 0), '^': (0, 1), '>': (1, 0), 'v': (0, -1)}
    for d in input:
        dx, dy = dirs[d]
        pos = (pos[0] + dx, pos[1] + dy)
        visited.add(pos)
    return visited

def a(input):
    return len(visited(input))

def b(input):
    l1 = [input[2*i] for i in range(len(input)//2)]
    l2 = [input[2*i + 1] for i in range(len(input)//2)]
    return len(visited(l1) | visited(l2))

input = open('input/03').read()

assert a('>') == 2
assert a('^>v<') == 4
assert a('^v^v^v^v^v') == 2

print(a(input))

assert b('^v') == 3
assert b('^>v<') == 3
assert b('^v^v^v^v^v') == 11

print(b(input))
