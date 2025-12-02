def nice_vowels(s):
    vowels = 'aeiou'
    count = 0
    for ss in s:
        if ss in vowels:
            count += 1
        if count >= 3:
            return True
    return False
assert nice_vowels('aei')
assert nice_vowels('xazegov')
assert nice_vowels('aeiouaeiouaeiou')

def nice_twice(s):
    for i in range(len(s)-1):
        if s[i] == s[i+1]:
            return True
    return False
assert nice_twice('xx')
assert nice_twice('abcdde')
assert nice_twice('aabbccdd')

def nice_not_bad(s):
    bad = ['ab', 'cd', 'pq', 'xy']
    return not any((b in s for b in bad))

def nice(s):
    return nice_vowels(s) and nice_twice(s) and nice_not_bad(s)

def naughty(s):
    return not nice(s)

def nice_b_pair(s):
    for i in range(len(s)-3):
        pair = s[i:i+2]
        if pair in s[i+2:]:
            return True
    return False
assert nice_b_pair('xyxy')
assert nice_b_pair('aabcdefgaa')

def nice_b_repeat(s):
    for i in range(len(s)-2):
        if s[i] == s[i+2]:
            return True
    return False
assert nice_b_repeat('xyx')
assert nice_b_repeat('abcdefeghi')
assert nice_b_repeat('aaa')

def nice_b(s):
    return nice_b_pair(s) and nice_b_repeat(s)

assert nice_not_bad('xcx')
assert not nice_not_bad('xcdy')

assert nice('ugknbfddgicrmopn')
assert nice('aaa')
assert naughty('jchzalrnumimnmhp')
assert naughty('haegwjzuvuyypxyu')
assert naughty('dvszwmarrgswjxmb')

input = open('input/05').read()

print(len(list(filter(nice, input.splitlines()))))
print(len(list(filter(nice_b, input.splitlines()))))
