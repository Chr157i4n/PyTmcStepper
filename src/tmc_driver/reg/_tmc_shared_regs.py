# pylint: disable=too-many-instance-attributes
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# pylint: disable=too-few-public-methods
"""
Register module with shared registers without implementation
"""

from ._tmc_reg import TmcReg


class TCoolThrs(TmcReg):
    """TCOOLTHRS register class stub"""

    tcoolthrs: int


class SGThrs(TmcReg):
    """SGTHRS register class stub"""

    sgthrs: int


class SGResult(TmcReg):
    """SGRESULT register class stub"""

    sgresult: int


class CoolConf(TmcReg):
    """COOLCONF register class stub"""

    seimin: bool
    sedn: int
    semax: int
    seup: int
    semin: int


class GStat(TmcReg):
    """GSTAT register class stub"""

    uv_cp: bool
    drv_err: bool
    reset: bool


class Ioin(TmcReg):
    """IOIN register class stub"""

    version: int
    dir: bool
    step: bool
    enn: bool
