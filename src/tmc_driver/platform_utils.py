"""Platform utility functions for TMC Driver library"""

import sys
import time

MICROPYTHON = sys.implementation.name == "micropython"


def get_time_us():
    """Get current time in microseconds, compatible with both CPython and MicroPython"""
    if MICROPYTHON:
        return time.ticks_us()  # pylint: disable=no-member
    return time.time_ns() // 1000
