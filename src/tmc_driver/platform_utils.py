"""Platform utility functions for TMC Driver library"""

import sys
import time

MICROPYTHON = sys.implementation.name == "micropython"
CIRCUITPYTHON = sys.implementation.name == "circuitpython"


def get_time_us():
    """Get current time in microseconds, compatible with CPython, MicroPython and CircuitPython"""
    if MICROPYTHON:
        return time.ticks_us()  # pylint: disable=no-member
    if CIRCUITPYTHON:
        return time.monotonic_ns() // 1000  # pylint: disable=no-member
    return time.time_ns() // 1000
