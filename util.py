import random
import math

class BadArgumentError(Exception):
    pass

def DRBG_get_bits(n: int) -> int:
    """
    Deterministic random bit generator
    !!! Not implemented

    https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-90Ar1.pdf

    Input:
        n -- number of bits to generate
    """
    return random.getrandbits(n)


def gcd(a: int, b: int) -> int:
    """
    Finds the greatest commom divisor of a and b.
    """
    if a < b:
        tmp = a
        a = b
        b = tmp
    while b != 0:
        r = a % b
        a = b
        b = r
    return a

def miller_rabin_round(w: int) -> str:
    """
    Perform one round of the Miller-Rabin probabilistic primality test with a random witness.
    Input:
        w -- Integer to be tested for primality 

    Output:
        status -- "PROBABLE PRIME" or "COMPOSITE"
    """

    if w % 2 == 0:
        return "COMPOSITE"

    a   = 0
    tmp = w - 1
    while tmp % 2 == 0:
        tmp = tmp // 2
        a = a + 1
    m = (w-1) // 2**a 

    base = 0
    while base <= 1 or base >= w-1:
        base = DRBG_get_bits(int(math.log2(w)))

    p = pow(base, m, w)

    if p == 1 or p == w-1:
        return "PROBABLE PRIME"
    
    for _ in range(1, a):
        p = pow(p, 2, w)
        if p == w-1:
            return "PROBABLE PRIME"
        
    return "COMPOSITE"


def miller_rabin(w: int, iterations: int = 1) -> str:
    """
    Miller-Rabin probabilistic primality test with multiple random witnesses.

    Input:
        w          -- Integer to be tested for primality 
        Iterations -- Number of iterations to perform with random witnesses

    Output:
        status -- "PROBABLE PRIME" or "COMPOSITE"
    """

    if w % 2 == 0:
        return "COMPOSITE"

    for _ in range(0, iterations):
        if miller_rabin_round(w) == "COMPOSITE":
            return "COMPOSITE"

    return "PROBABLE PRIME"       
        

  




