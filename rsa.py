import util
import math

def rsa_gen_primes(nlen: int, e: int) -> tuple[int, int]:
    """
    Generate probable primes p and q to be used for RSA as defined in FIPS 186-5.

    Input:
        nlen -- Bit length of desired modulus n
        e    -- Public RSA exponent

    Output:
        (p, q) -- Probable primes p and q or (0, 0) if something went wrong.
    """

    if nlen < 2048:
        raise util.BadArgumentError("Length of n should meet or exceed 2048 bits.")
    
    if e <= 65536 or e >= 2**256 or e % 2 != 1:
        raise util.BadArgumentError("Public exponent e should be odd, greater than 2**16 and less than 2**256.")

    # Generate p
    for i in range(0, 5*nlen+1):
        while True:
            p = util.DRBG_get_bits(nlen // 2)
            if p > math.sqrt(2) * 2**(nlen // 2 - 1):
                break

        if util.gcd(p - 1, e) == 1:
            if util.miller_rabin(p, 4) == "PROBABLE PRIME": # FIPS 186-5 recommends at the minimum 4 witnesses for primes of size 1024 bits.
                break
        
        if i == 5*nlen+1:
            return (0, 0)

    # Generate q
    for i in range(0, 10*nlen+1):
        while True:
            q = util.DRBG_get_bits(nlen // 2)
            if q > math.sqrt(2) * 2**(nlen // 2 - 1) and abs(p - q) > 2**(nlen // 2 - 100):
                break
                
        if util.gcd(q - 1, e) == 1:
            if util.miller_rabin(q, 4) == "PROBABLE PRIME":
                break

        if i == 10*nlen+1:
            return (0, 0)
        
    return (p, q)

if __name__ == "__main__":
    e = 65537

    (p,q) = rsa_gen_primes(2048, e)


