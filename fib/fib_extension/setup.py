from distutils.core import Extension
from distutils.core import setup

ext_module = Extension('fibonacciext', sources=['fib_extension.c'])


setup(name='fibonacciext',
      version='0.1.1',
      license='BSD',
      description='C extension for Fibonacci numbers generation function',
      author="Oleksii Potorzhynskyi",
      author_email="oleksii_potorzhynskyi@epam.com",
      ext_modules=[ext_module])
