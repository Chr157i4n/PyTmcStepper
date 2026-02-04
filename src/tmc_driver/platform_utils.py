"""Platform utility functions for TMC Driver library."""

import sys
import time

MICROPYTHON = sys.implementation.name == "micropython"
CIRCUITPYTHON = sys.implementation.name == "circuitpython"


def get_time_us():
    """Get current time in microseconds.

    Compatible with CPython, MicroPython and CircuitPython.
    """
    if MICROPYTHON:
        return time.ticks_us()  # pylint: disable=no-member
    if CIRCUITPYTHON:
        return time.monotonic_ns() // 1000  # pylint: disable=no-member
    return time.time_ns() // 1000


def sleep_us(microseconds: int):
    """Sleep for specified microseconds.

    Compatible with CPython, MicroPython and CircuitPython.
    """
    if MICROPYTHON:
        time.sleep_us(microseconds)  # pylint: disable=no-member
    else:
        time.sleep(microseconds / 1_000_000)
