d = {
    'a':123,
    'b':1234,
    'c':3,
    "d":14
}

class Person:
    def __init__(self, id):
        self.id = id


def find_two_biggest(d:dict) -> list:

    v = sorted(d.values())
    a, b = v[-1], v[-2]
    keys = d.keys()
    a = [key if d.get(key) == a else -1 for key in keys]
    b = [key if d.get(key) == b else -1 for key in keys]
    l = [a, b]
    return l

print(find_two_biggest(d))
print(hash(Person))