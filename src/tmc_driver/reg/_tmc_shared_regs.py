# pylint: disable=too-many-instance-attributes
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# pylint: disable=too-few-public-methods
"""
Register module with shared registers without implementation
"""


class TCoolThrs:
    """TCOOLTHRS register class stub"""

    tcoolthrs: int


class SGThrs:
    """SGTHRS register class stub"""

    sgthrs: int


class SGResult:
    """SGRESULT register class stub"""

    sgresult: int


class CoolConf:
    """COOLCONF register class stub"""

    seimin: bool
    sedn: int
    semax: int
    seup: int
    semin: int


class GStat:
    """GSTAT register class stub"""

    uv_cp: bool
    drv_err: bool
    reset: bool


class Ioin:
    """IOIN register class stub"""

    version: int
    dir: bool
    step: bool
    enn: bool
