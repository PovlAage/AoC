from hashlib import md5


def f(key, zeroes):
    n = 1
    while not md5((key + str(n)).encode()).hexdigest().startswith(zeroes * '0'):
        n += 1
    return n

def a(key):
    return f(key, 5)

assert a('abcdef') == 609043
assert a('pqrstuv') == 1048970

input = 'ckczppom'

print(a(input))
print(f(input, 6))
