from __future__ import annotations
from dataclasses import dataclass
import random 

@dataclass
class Curve:
    """
    Elliptic Curve over the field of integers modulo a prime.
    Points on the curve satisfy y^2 = x^3 + a * x + b (mod p).
    """
    p: int
    a: int
    b: int

@dataclass 
class Point:
    """ An integer point (x,y) on a Curve """
    curve: Curve
    x: int
    y: int

@dataclass
class Generator:
    """
    A generator over a curve: an initial point and the (pre-computed) order
    """
    G: Point # a generator point on the curve
    n: int   # the order of the generating point, so 0*G = n*G = INF

# secp256k1 uses a = 0, b = 7, so we're dealing with the curve y^2 = x^3 + 7 (mod p)
bitcoin_curve = Curve(
    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F,
    a = 0x0000000000000000000000000000000000000000000000000000000000000000, # a = 0
    b = 0x0000000000000000000000000000000000000000000000000000000000000007, # b = 7
)

# Bitcoin generator point
G = Point(
    bitcoin_curve,
    x = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
    y = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8,
)

bitcoin_gen = Generator(
        G = G,
        # the order of G is known and can be mathematically derived (not by me tho lol)
        n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141,
        )

INF = Point(None, None, None) # point at "infinity"

def extended_euclidean_algorithm(a, b):
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
    return old_r, old_s, old_t

def inv(n, p):
    """ returns mod mult inv m st (n * m) % p == 1 """
    gcd, x, y = extended_euclidean_algorithm(n, p)
    return x % p

def elliptic_curve_addition(self, other: Point) -> Point:
    # handle special case of P + 0 = 0 + P = 0
    if self == INF:
        return other
    if other == INF:
        return self
    # handle special case of P + (-P) = 0
    if self.x == other.x and self.y != other.y:
        return INF
    # compute the "slope"
    if self.x == other.x: # (self.y = other.y is guaranteed too per above check)
        m = (3 * self.x**2 + self.curve.a) * inv(2 * self.y, self.curve.p)
    else:
        m = (self.y - other.y) * inv(self.x - other.x, self.curve.p)
    # compute the new point
    rx = (m**2 - self.x - other.x) % self.curve.p
    ry = (-(m*(rx - self.x) + self.y)) % self.curve.p
    return Point(self.curve, rx, ry)


if __name__ == "__main__":
    # Checking that the point is actually on the curve
    print("Generator IS on the curve:", (G.y**2 - G.x**3 - 7) % bitcoin_curve.p == 0)
    
    # Checking that a random point is not on the curve
    random.seed(1337)
    x = random.randrange(0, bitcoin_curve.p)
    y = random.randrange(0, bitcoin_curve.p)
    print("Random point is on curve:", (y**2 - x**3 - 7) % bitcoin_curve.p == 0)

    # secret_key = random.randrange(1, bitcoin_gen.n)
    secret_key = int.from_bytes(b'Sice deets', 'big')
    assert 1 <= secret_key < bitcoin_gen.n
    print("Secret key:", secret_key)


    
    
    
