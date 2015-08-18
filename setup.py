#!/usr/bin/python

from distutils.core import setup
from Cython.Build import cythonize

setup(
    name = "SerialProtocol",
    ext_modules = cythonize("*.pyx")
)
