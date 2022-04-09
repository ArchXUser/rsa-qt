import random

from math import gcd
from typing import Tuple
from miller_rabin import miller_rabin


def generate_large_number(n: int) -> int:
    return random.randrange(10**(n-1) + 1, 10**n)


def is_prime(num: int) -> bool:
    # get rid of it?
    low_primes = [
        2,   3,   5,   7,   11,  13,  17,  19,  23,  29,  31,  37,
        41,  43,  47,  53,  59,  61,  67,  71,  73,  79,  83,  89,
        97,  101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151,
        157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223,
        227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281,
        283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359,
        367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433,
        439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503,
        509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593,
        599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659,
        661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743,
        751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827,
        829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911,
        919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997
    ]
    if num in low_primes:
        return True

    for prime in low_primes:
        if num % prime == 0 and prime**2 <= num:
            return False

    return miller_rabin(num, 40)


def generate_prime_number(length: int) -> int:
    while True:
        num = generate_large_number(length)
        if not is_prime(num):
            continue
        return num


def is_coprime(a: int, b: int) -> bool:
    return gcd(a, b) == 1


def generate_keys(keysize: int) -> Tuple[int, int, int]:
    n = p = q = 0

    while len(str(n)) != keysize or p == q:
        p = generate_prime_number(keysize//2)
        q = generate_prime_number(keysize//2 + 1)
        n = p*q

    phiN = (p-1) * (q-1)
    # e = 65537
    while True:
        e = generate_large_number(keysize-1)
        if is_coprime(e, phiN):
            break

    d = pow(e, -1, phiN)

    return (e, n, d)


def encrypt(e: int, n: int, msg: str) -> str:
    cipher = ""

    for c in msg:
        m = ord(c)
        cipher += str(pow(m, e, n)) + " "

    return cipher


def decrypt(d: int, n: int, cipher: str) -> str:
    msg = ""

    parts = cipher.split()
    for part in parts:
        if part:
            try:
                c = int(part)
            except ValueError as err:
                print(f"{err=}, {type(err)=}")
                break
            msg += chr(pow(c, d, n))

    return msg
