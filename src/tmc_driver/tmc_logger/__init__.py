# pylint: disable=unused-import
"""
Tmc logger module
"""

import sys
from ._tmc_logger_base import Loglevel

MICROPYTHON = sys.implementation.name == "micropython"
CIRCUITPYTHON = sys.implementation.name == "circuitpython"

if MICROPYTHON or CIRCUITPYTHON:
    from ._tmc_logger_micropython import TmcLogger
else:
    import logging
    from ._tmc_logger_cpython import TmcLogger
