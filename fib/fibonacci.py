"""Benchmark for the Fibonacci numbers calculation"""

from fib_cython import fibcyt
from fibonacciext import fibext
import time

MAX_ITEM_NUMBER = 92


def timeit(func, *args, **kwargs):
    """Calculates function execution time in milliseconds

    :param func: function for execution
    :param args: args list
    :param kwargs: kwargs dict
    :return:  (function result, time in millisends)
    """

    start_time = time.time()
    result = func(*args, **kwargs)
    return result, (time.time() - start_time) * 1000


def fib_with_list(n):
    """Fibonacci numbers with list building"""

    fib_list = [0, 1]
    for item in range(2, n):
        fib_list.append(fib_list[item - 2] + fib_list[item - 1])
    return fib_list[n - 1]


def fib(n):
    """Fibonacci number without list"""
    a, b = 0, 1
    for item in range(3, n + 1):
        a, b = b, a + b
    return b


if __name__ == '__main__':

    print("Calculate {}th item of the Fibonacci sequence:\n".format(
        MAX_ITEM_NUMBER))

    result, exec_time = timeit(fib_with_list, MAX_ITEM_NUMBER)
    print("CPython implementation with list building took {:.4f} ms"
          " with result {} ".format(exec_time, result))

    result, exec_time = timeit(fib, MAX_ITEM_NUMBER)
    print("CPython implementation without recursion took {:.4f} ms"
          " with result {} ".format(exec_time, result))

    result, exec_time = timeit(fibcyt, MAX_ITEM_NUMBER)
    print("Cython implementation without recursion took {:.4f} ms"
          " with result {}".format(exec_time, result))

    result, exec_time = timeit(fibext, MAX_ITEM_NUMBER)
    print("C extension implementation without recursion took {:.4f} ms"
          " with result {}".format(exec_time, result))
