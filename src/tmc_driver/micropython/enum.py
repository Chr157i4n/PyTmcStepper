"""
MicroPython enum dummy module

This module provides a drop-in replacement for Python's enum module.
It allows code that uses Enum/IntEnum to run on MicroPython
without modifications.

Usage on Pico:
    Copy this file to /lib/enum.py on the Pico
"""


class Enum:
    """Simple Enum replacement for MicroPython

    Works as a base class for enumerations.
    """


class IntEnum(int):
    """Simple IntEnum replacement for MicroPython

    Works as a base class for integer enumerations.
    Values can be compared with integers directly.
    """
