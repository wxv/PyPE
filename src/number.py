# Commonly used number-related functions
import math

def sieve(n):
    """Sieve of Eratosthenes. Returns a list. About O(n)"""
    nums = [0] * n
    for i in range(2, int(n**0.5)+1):
        if nums[i] == 0:
            for j in range(i*i, n, i):
                nums[j] = 1

    return [i for i in range(2, n) if nums[i] == 0]


def sieve_set(n):
    return set(sieve(n))


def is_prime(n):
    """Returns whether a number is prime or not"""
    if n < 2: return False
    return all(n%i for i in range(2, int(n**0.5)+1))


def is_square(n):
    """Returns if a number is square without floating point math. Credit: Alex Martelli"""
    x = n // 2
    seen = set([x])
    while x * x != n:
        x = (x + (n // x)) // 2
        if x in seen: return False
        seen.add(x)
    return True


def prime_factors(n):
    factors = []
    m = n
    prime = False
    while not prime:
        prime = True
        for i in range(2, int(m**0.5)+1):
            if m%i == 0:
                m //= i
                factors.append(i)
                prime = False
                break

    return factors + [m]


def combination(n, k):
    f = math.factorial
    return f(n) // f(k) // f(n-k)


def permutation(n, k):
    f = math.factorial
    return f(n) // f(n-k)


def take_closest(l, n, bisect=True):
    """If bisect: Assumes l is sorted. Returns closest value to n.
       If two numbers are equally close, return the smallest number. Credit: Lauritz V. Thaulow
       If not bisect: Use lambda and min to go through list, O(n) time."""
    if bisect:
        from bisect import bisect_left
        pos = bisect_left(l, n)
        if pos == 0:
            return l[0]
        if pos == len(l):
            return l[-1]
        before = l[pos - 1]
        after = l[pos]
        if after - n < n - before:
           return after
        else:
           return before

    else:
        return min(l, key=lambda x:abs(x-n))



if __name__ == "__main__":
    pass