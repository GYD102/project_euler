#!/usr/bin/env python3

from functools import lru_cache, wraps
from time import time

# Function courtesy of jonaprieto https://stackoverflow.com/users/1121552/jonaprieto
# https://stackoverflow.com/questions/1622943/timeit-versus-timing-decorator
def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print('func:%r args:[%r, %r] took: %2.4f sec' % \
          (f.__name__, args, kw, te-ts))
        return result
    return wrap

# I discovered lru_cache from user apai https://stackoverflow.com/users/1977906/apai
# on this Stack Overflow thread: https://stackoverflow.com/questions/21099373/memoization-python

# @lru_cache(maxsize=None)

# Unfortunately, lru_cache, though fast, does not give me access to the cache (which I would like)
# So, courtesy of user Bakuriu (https://stackoverflow.com/users/510937/bakuriu)
# from thread https://stackoverflow.com/questions/15585493/store-the-cache-to-a-file-functools-lru-cache-in-python-3-2

def cached(func):
    func.cache = {(1,):2}
    @wraps(func)
    def wrapper(*args):
        try:
            return func.cache[args]
        except KeyError:
            func.cache[args] = result = func(*args)
            return result
    return wrapper

@cached
def prime(n):
    #while n - prime.cache_info()[3] > 330:
    #    prime(prime.cache_info()[3] + 330)
    while n - len(prime.cache) > 330:
        prime(len(prime.cache) + 330)
    if n == 1:
        return 2
    if n == 2:
        return 3
    start = prime(n-1) + 2
    end = start ** 0.5
    i = 2
    p = prime(i)
    while(p <= end):
        if start % p == 0:
            start = start + 2
            end = start ** 0.5
            i = 1
        i += 1
        p = prime(i)
    return start

# For performance testing
@timing
def timed_prime(n):
    return prime(n)

def bin_serc(n, d):
    bottom = 1
    top = max(d.keys())[0]
    mid = round(top / 2)
    ptop = d[(mid,)]
    pbot = d[(mid-1,)]
    while ptop < n or pbot > n:
        if ptop < n:
            bottom = mid
        else:
            top = mid
        mid = round((top + bottom) / 2)
        ptop = d[(mid,)]
        pbot = d[(mid-1,)]
    return (mid - 1)


def primes_up_to(n):
    if len(prime.cache) == 0:
        prime(2)
    # populate from the beginning
    if max(prime.cache.values()) < n:
        start = max(prime.cache.keys())[0] + 1
        while(prime(start) < n):
            start += 1
        return start - 1
    # find smallest prime larger than n
    else:
        return bin_serc(n, prime.cache)

from math import ceil
def largest_prime_factor(n):
    i = primes_up_to(n)
    m = round(n ** 0.5)
    while(i > 0):
        if n % prime.cache[(i,)] == 0:
            return prime.cache[(i,)]
        i -= 1
    return n

@timing
def slow_lpf(n):
    return largest_prime_factor(n)

# Essentially, the above function finds all primes less than or equal to n
# and finds the first prime (highest to lowest) that divides n. However,
# This requires finding all the primes up to that number.

# However, this becomes a bit ridiculous when the number in question is on the
# order of 10^11

def smallest_prime_factor(n):
    i = 1
    p = prime(i)
    while(p <= n ** 0.5):
        if n % p == 0:
            return p
        i += 1
        p = prime(i)
    return n

def fast_largest_pf(n):
    s = smallest_prime_factor(n)
    if s == n:
        return n
    return fast_largest_pf(n / s)

@timing
def fast_lpf(n):
    return fast_largest_pf(n)

