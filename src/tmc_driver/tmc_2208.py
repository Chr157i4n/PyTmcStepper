# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
"""Tmc2208 stepper driver module.

this module has two different functions:
1. access register via tmc_com (UART, SPI)
2. Enable motor control via tmc_ec (TOFF, PIN)
3. move the motor via tmc_mc (STEP/DIR, STEP/REG, VACTUAL)
"""

from .tmc_220x import *


class Tmc2208(Tmc220x):
    """Tmc2208."""

    DRIVER_FAMILY = "TMC2208"
