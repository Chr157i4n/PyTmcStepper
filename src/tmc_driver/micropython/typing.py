"""
MicroPython typing dummy module

This module provides a drop-in replacement for Python's typing module.
It allows code that uses type hints to run on MicroPython
without modifications.

Usage on Pico:
    Copy this file to /lib/typing.py on the Pico
"""

# Basic types - just return the argument or a dummy
def _dummy(*args, **kwargs):
    del kwargs
    if args:
        return args[0]
    return None

# Generic types
List = _dummy
Dict = _dummy
Set = _dummy
Tuple = _dummy
Optional = _dummy
Union = _dummy
Any = None
Callable = _dummy
Type = _dummy
Sequence = _dummy
Iterable = _dummy
Iterator = _dummy
Mapping = _dummy
MutableMapping = _dummy
MutableSequence = _dummy
MutableSet = _dummy
