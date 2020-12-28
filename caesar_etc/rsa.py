import random
import math


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def multiplicative_inverse(e: int, phi: int):
    g, x, y = egcd(e, phi)
    if g != 1:
        raise Exception('Все очень плохо')
    else:
        return x % phi


def gcd(x, y):
    if y == 0:
        return x
    else:
        return gcd(y, x % y)


def is_prime(n: int) -> bool:
    if n == 1:
        return False

    if n in [2, 3]:
        return True

    end = int(math.sqrt(n)) + 1

    for i in range(2, end):
        if n % i == 0:
            return False

    return True


def generate_keypair(p: int, q: int):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("Both numbers must be prime.")
    elif p == q:
        raise ValueError("p and q cannot be equal")

    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randrange(1, phi)
    g = gcd(e, phi)

    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    d = multiplicative_inverse(e, phi)

    return (e, n), (d, n)
