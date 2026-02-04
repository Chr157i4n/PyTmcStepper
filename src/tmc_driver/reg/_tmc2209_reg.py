# pylint: disable=too-many-instance-attributes
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
"""Register module."""

from ._tmc220x_reg import *
from . import _tmc_shared_regs as shared


class TCoolThrs(shared.TCoolThrs):
    """TCOOLTHRS register class."""

    ADDR = 0x14

    tcoolthrs: int
    _REG_MAP = (TmcRegField("tcoolthrs", 0, 0xFFFFF, int, None, ""),)


class SgThrs(shared.SgThrs):
    """SGTHRS register class."""

    ADDR = 0x40

    sgthrs: int
    _REG_MAP = (TmcRegField("sgthrs", 0, 0xFFFFF, int, None, ""),)


class SgResult(shared.SgResult):
    """SGRESULT register class."""

    ADDR = 0x41

    sgresult: int
    _REG_MAP = (TmcRegField("sgresult", 0, 0xFFFFF, int, None, ""),)


class CoolConf(shared.CoolConf):
    """COOLCONF register class."""

    ADDR = 0x42

    seimin: bool
    sedn: int
    semax: int
    seup: int
    semin: int
    _REG_MAP = (
        TmcRegField("seimin", 15, 0x1, bool, None, ""),
        TmcRegField("sedn", 13, 0x3, int, None, ""),
        TmcRegField("semax", 8, 0xF, int, None, ""),
        TmcRegField("seup", 5, 0x3, int, None, ""),
        TmcRegField("semin", 0, 0xF, int, None, ""),
    )
