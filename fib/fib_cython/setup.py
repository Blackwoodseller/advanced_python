from Cython.Build import cythonize
from distutils.core import setup

cython_module = cythonize("fib_cython.pyx")

setup(name='fibonacci_cython',
      version='0.1',
      license='BSD',
      description='This is a Fibonacci numbers generation demo package',
      author="Oleksii Potorzhynskyi",
      author_email="oleksii_potorzhynskyi@epam.com",
      ext_modules=cython_module)
