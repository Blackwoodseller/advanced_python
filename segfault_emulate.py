"""Initiates segfault in ctypes.string_at by reading a word from NULL"""

import ctypes


ctypes.string_at(0)
