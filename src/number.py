# Commonly used number-related functions
from __future__ import division
import math
import random


prime_100 = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97)
set_prime_100 = set(prime_100)

module_primes = None

def sieve(n):
    """Sieve of Eratosthenes. Returns a list. About O(n)"""
    nums = [0] * n
    for i in range(2, int(n**0.5)+1):
        if nums[i] == 0:
            for j in range(i*i, n, i):
                nums[j] = 1

    return [i for i in range(2, n) if nums[i] == 0]


def sieve_set(n):
    """Returns a set of sieve(n)"""
    return set(sieve(n))


def is_prime(n, trials=20):
    """Returns whether a number is prime or not using Miller-Rabin. Credit: Albert Sweigart
    First check divisibility by small primes (below 100).
    Deterministic variant by checking small set of potential witnesses.
    Smallest number requiring first n prime numbers is A006945."""
    if n < 2: return False
    # Small trial division
    if n in set_prime_100: return True
    if any(n % p == 0 for p in prime_100): return False

    s = n - 1
    t = 0
    while s % 2 == 0:
        s = s // 2
        t += 1

    # Testing is_prime set of potential witnesses is big speedup! (n<10^6: 13.8 -> 3.1 s, n<10^7: 136.2 -> 34.9 s)
    # Still twice as slow as gmpy2 though :(
    witness_sets = (
        (2047, (2,)),
        (1373653, (2, 3)),
        (25326001, (2, 3, 5)),
        (3215031751, (2, 3, 5, 7)),
        (3474749660383, (2, 3, 5, 7, 11, 13)),
        (341550071728321, (2, 3, 5, 7, 11, 13, 17))
    )

    small_n = n < 341550071728321
    for witness_set in witness_sets:
        if n < witness_set[0]:
            witnesses = witness_set[1]
            trials = len(witnesses)
            break

    for trial in range(trials):
        if small_n:
            a = witnesses[trial]
        else:
            a = random.randrange(2, n - 1)

        v = pow(a, s, n)
        if v != 1: # this test does not apply if v is 1.
            i = 0
            while v != (n - 1):
                if i == t - 1:
                    return False
                else:
                    i = i + 1
                    v = (v ** 2) % n
    return True


def is_square(n):
    """Returns if a number is square without floating point math. Credit: Alex Martelli"""
    if n == 1: return True
    x = n // 2
    seen = set([x])
    while x * x != n:
        x = (x + (n // x)) // 2
        if x in seen: return False
        seen.add(x)
    return True


def is_square_fp(n):
    """Returns if a number is square, avoiding some floating point errors"""
    return int(n**0.5 + 0.5)**2 == n


def is_square_gmpy(n):
    import gmpy2
    return gmpy2.is_square(n)


def prime_factors(n, N_MAX=10000):
    """Return all factors. Calculates primes once to use."""
    global module_primes
    if not module_primes:
        module_primes = sieve(N_MAX)

    assert(n <= N_MAX**2)  # Assert big enough prime factors to test
    
    factors = []
    m = n
    prime = False
    while not prime:
        prime = True
        for i in module_primes:
            if m%i == 0:
                m //= i
                factors.append(i)
                prime = False
                break

    if m != 1: factors += [m]
    return factors


def combination(n, k):
    f = math.factorial
    return f(n) // f(k) // f(n-k)


def permutation(n, k):
    f = math.factorial
    return f(n) // f(n-k)


def take_closest(l, n, bisect=True):
    """If bisect (binary search): Assumes l is sorted. Returns closest value to n.
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


def gcd(a, b):
    """Euclid's algorithm. Identical to fractions.gcd(a, b)"""
    while b:
        a, b = b, a%b
    return a


def lcm(a, b):
    """Get lcm by reduction of the gcd"""
    return a * b // gcd(a, b)


def lcm_n(n):
    """Find lcm of integers 1 to n.
    Skip calculating lcm for 1 to n/2 since those are covered by the upper half"""
    x = 1
    for i in range(max(n//2, 1), n+1):
        x = lcm(x, i)
    return x

def phi(n, product_formula=True):
    """Euler's product formula or straightforward calculation of Euler's totient function."""
    if n == 0: return 0
    if product_formula:
        spf = set(prime_factors(n))
        r = n
        for p in spf:
            r -= r//p  # r *= (1 - 1/p)
        return r

    else:
        r = 0
        for k in range(1, n+1):
            if gcd(n, k) == 1:
                r += 1
        return r


def dijkstra(graph, start):
    """Dijkstra's algorithm using heaps.
    Test using g = {0:{1:2}, 1:{0:2, 2:6}, 2:{1:6}}  Credit: Janne Karila"""
    from heapq import heappush, heappop

    A = [None] * len(graph)
    queue = [(0, start)]
    while queue:
        path_len, v = heappop(queue)
        if A[v] is None: # v is unvisited
            A[v] = path_len
            for w, edge_len in graph[v].items():
                if A[w] is None:
                    heappush(queue, (path_len + edge_len, w))

    return A


def product(iterable):
    product = 1
    for i in iterable: product *= i  # No reduce() :(
    return product


def highly_composite():
    hc = []
    with open("highly_composite.txt", 'r') as f:
        for rows in f:
            hc.append(int(rows.split(' ')[1]))
    return hc


def mul_inv(a, b):
    """Modular multiplicative inverse, ax = 1 mod m. Credit: rosettacode.org"""
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        assert b != 0, "a and b must be coprime"
        q = a // b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1


def powerset(iterable):
    """From itertools recipes
    powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"""
    from itertools import chain, combinations
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def custom_powerset(s, min_combo, max_combo):
    from itertools import chain, combinations
    return chain.from_iterable(combinations(s, r) for r in range(min_combo, max_combo+1))


def totient_sum(N):
    """Find the sum of phi(n) for 1 to N. O(log n) space, O(n^(3/4)) time
    Credit: daniel.is.fischer"""
    K = int((N/2)**0.5)
    M = N // (2*K+1)
    rsmall = [0]*(M+1)
    rlarge = [0]*K

    def F(n):
        return (n+1)*n//2

    def R(n):
        switch = int((n/2)**0.5)
        count = F(n) - F(n//2)
        m = 5
        k = (n-5)//10
        while k >= switch:
            nextk = (n // (m+1) - 1) // 2
            count -= (k - nextk)*rsmall[m]
            k = nextk
            m += 1

        while k > 0:
            m = n // (2*k+1)
            if m <= M:
                count -= rsmall[m]
            else:
                count -= rlarge[((N//m) - 1) // 2]
            k -= 1

        if n <= M:
            rsmall[n] = count
        else:
            rlarge[((N//n) - 1) // 2] = count


    for n in range(5, M+1):
        R(n)

    for j in range(K-1, -1, -1):
        R(N // (2*j + 1))

    #print(rlarge, rsmall)
    return rlarge[0]


def totient_range(n):
    """Calculates all totients in a range using a sieve and Euler's product formula for O(n log log n) time.
    Credit: Marcus Stuhr"""
    tots = [x for x in range(0, n+1)]
    for p in range(2, n+1):
        if p == tots[p]:
            k = p
            while k <= n:
                tots[k] -= tots[k] // p
                k += p

    return tots


def factors(n):
    """Naive implementation"""
    f = []
    for i in range(1, int(n**0.5)+1):
        if n%i == 0:
            f += [i]
            if i != n//i: f += [n//i]
    return f


def timeit(f):
    """Timing decorator for functions. Example usage: sieve = timeit(sieve)"""
    from time import clock
    def timed(*args, **kwargs):
        time_start = clock()
        result = f(*args, **kwargs)
        time_end = clock()

        all_args = list(map(str, args))
        for key in kwargs:
            all_args.append("{}={}".format(key, kwargs[key]))

        print("{}({})   took {:2.4f}s".format(f.__name__, ', '.join(all_args),
                                              time_end - time_start))
        return result

    return timed


def int_to_base(n, b):
    """Returns a list of digits in arbitrary base"""
    assert n >= 0  # Untested for negative nums

    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]


def pandigital(n, b):
    """Checks if n contains all digits from 0 to b-1"""
    digit_list = int_to_base(n, b)
    return set(digit_list) == set(range(b))


def is_smooth(n, primes):
    """Test if n has only factors in primes"""
    for p in primes:
        while n % p == 0:
            n //= p

    return n == 1


if __name__ == "__main__":
    print(lcm_n(1))