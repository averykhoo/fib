from time import time

from decorators import memodict, verbose


def fibonacci6(n):
    if n < 0:
        raise ValueError("Negative arguments not implemented")
    bits = bin(n)[2:]
    a, b = 0, 1
    for bit in bits:
        if bit == '1':
            a, b = b * b + a * a, b * ((a << 1) + b)
        else:
            a, b = a * ((b << 1) - a), b * b + a * a
    return a


# @verbose
def fibonacci1(num):
    "O(log(n)) implementation of fibonacci using fast doubling."
    if num >= 0:
        return fib_helper(num)[0]


# @verbose
def fib_helper(num):
    # print('->', num)
    "Helper function for fibonacci()."
    if num == 0:
        return (0, 1)
    elif num == 1:
        return (1, 1)
    else:
        f_k, f_k_1 = fib_helper(num // 2)  # this is floordiv
        f_k_even = f_k * (2 * f_k_1 - f_k)
        f_k_odd = f_k_1 * f_k_1 + f_k * f_k
        if num % 2 == 0:
            return (f_k_even, f_k_odd)
        else:
            return (f_k_odd, f_k_even + f_k_odd)


"""
the following code used decimal.Decimal to avoid binary -> decimal conversion
because that is quadratic with bit length
"""

import decimal
from decimal import Decimal as D

DO = D(0)
D1 = D(1)


# @verbose
def fibonacci2(num):
    from math import log10

    if num >= 0:
        # ndigits = int(log10(1.62) * num + 100)
        # decimal.getcontext().prec = ndigits
        # decimal.getcontext().Emax = ndigits
        return fib_helper2(num)[0]


# @verbose
def fib_helper2(num):
    # print('->', n)
    if num == 0:
        return 1, 1
    elif num == 1:
        return 1, 1
    else:
        f_k, f_k_1 = fib_helper2(num // 2)
        f_k_even = f_k * (2 * f_k_1 - f_k)
        f_k_odd = f_k_1 * f_k_1 + f_k * f_k
        return (f_k_even, f_k_odd) if num % 2 == 0 else (f_k_odd, f_k_even + f_k_odd)


#
# Fast doubling Fibonacci algorithm
#
# Copyright (c) 2013 Nayuki Minase
# All rights reserved. Contact Nayuki for licensing.
# http://nayuki.eigenstate.org/page/fast-fibonacci-algorithms
#


# Returns F(n)
# @verbose
def fibonacci3(n):
    if n < 0:
        raise ValueError("Negative arguments not implemented")
    return _fib3(int(n))[0]


# Returns a tuple (F(n), F(n+1))
# @verbose
def _fib3(n):
    if n == 0:
        return (0, 1)
    else:
        a, b = _fib3(n >> 1)
        if n & 1:
            e = b * ((a << 1) + b)
            d = b * b + a * a
            return (d, e)
        else:
            c = a * ((b << 1) - a)
            d = b * b + a * a
            return (c, d)


# Returns F(n)
# @verbose
def fibonacci3b(n):
    if n < 0:
        raise ValueError("Negative arguments not implemented")
    return _fib3b(int(n))[0]


# Returns a tuple (F(n), F(n+1))
# @verbose
def _fib3b(n):
    if n < 10:
        return [(0, 1), (1, 1), (1, 2), (2, 3), (3, 5), (5, 8), (8, 13), (13, 21), (21, 34), (34, 55)][n]
    else:
        a, b = _fib3b(n >> 1)
        if n & 1:
            return b * b + a * a, b * ((a << 1) + b)
        else:
            return a * ((b << 1) - a), b * b + a * a


# (not so fast)
# Fast Fibonnaci
# @verbose
def fibonacci4(n):
    if n <= 2:
        return 1
    return _fib4(n)

def _fib4(n):
    # print('->', n)
    k = n / 2
    a = _fib4(k + 1)
    b = _fib4(k)
    if n % 2 == 1:
        return a * a + b * b
    else:
        return b * (2 * a - b)

def fibonacci5(n):
    return _fib5(n)

# what a difference memoization makes
@memodict
def _fib5(n):
    # print('->', n)
    if n <= 2:
        return 1
    k = n / 2
    a = _fib5(k + 1)
    b = _fib5(k)
    if n % 2 == 1:
        return a * a + b * b
    else:
        return b * (2 * a - b)


# Returns F(n)
# @verbose
def fibonacci3c(n):
    if n < 0:
        raise ValueError("Negative arguments not implemented")
    return _fib3c(int(n))[0]


# Returns a tuple (F(n), F(n+1))
# @verbose
def _fib3c(n):
    if n < 10:
        a, b = [(0, 1), (1, 1), (1, 2), (2, 3), (3, 5), (5, 8), (8, 13), (13, 21), (21, 34), (34, 55)][int(n)]
        return decimal.Decimal(a), decimal.Decimal(b)
    else:
        a, b = _fib3c(n // decimal.Decimal(2))
        if n % decimal.Decimal(2):
            return b * b + a * a, b * ((a * decimal.Decimal(2)) + b)
        else:
            return a * ((b * decimal.Decimal(2)) - a), b * b + a * a


if __name__ == '__main__':
    import pandas as pd

    t = time()
    print(fibonacci2(20))
    print(fibonacci3(20))
    a = fibonacci3c(20000)
    print(a)
    print(time() - t)

    test_list = [fibonacci3,
                 fibonacci1,  # fast doubling
                 fibonacci3b,
                 fibonacci3c,
                 fibonacci6,  # bits -> string
                 # fibonacci4,  # slow!
                 fibonacci5,
                 fibonacci2,
                 ]
    test_numbers = [10, 20, 50,
                    100, 200, 500,
                    1000, 2000, 5000,
                    10000, 20000, 50000,
                    100000, 200000, 500000,
                    1000000, 2000000, 5000000]
    print('\ntest1\n')
    df_times = []
    for n in test_numbers:
        times = {'n': n}
        print(n)
        for f in test_list:
            t0 = time()
            for i in range(10000):
                f(i)
            t1 = time()
            times[f.__name__] = t1 - t0
            print('%s(%d)' % (f.__name__, n), 'time =', t1 - t0)
        df_times.append(times)
    df_times = pd.DataFrame(df_times)

    print(df_times)
    print(df_times.sum())
