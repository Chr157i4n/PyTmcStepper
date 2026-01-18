# pylint: disable=too-many-instance-attributes
"""
Register module
"""

import math
from ._tmc_reg import TmcRegField
from . import _tmc_shared_regs as shared
from .._tmc_exceptions import TmcDriverException


class GConf(shared.GConf):
    """GCONF register class"""

    ADDR = 0x0

    test_mode: bool
    multistep_filt: bool
    mstep_reg_select: bool
    pdn_disable: bool
    index_step: bool
    index_otpw: bool
    shaft: bool
    en_spreadcycle: bool
    internal_rsense: bool
    i_scale_analog: bool
    _REG_MAP = (
        TmcRegField("test_mode", 9, 0x1, bool, None, ""),
        TmcRegField("multistep_filt", 8, 0x1, bool, None, ""),
        TmcRegField("mstep_reg_select", 7, 0x1, bool, None, ""),
        TmcRegField("pdn_disable", 6, 0x1, bool, None, ""),
        TmcRegField("index_step", 5, 0x1, bool, None, ""),
        TmcRegField("index_otpw", 4, 0x1, bool, None, ""),
        TmcRegField("shaft", 3, 0x1, bool, None, ""),
        TmcRegField("en_spreadcycle", 2, 0x1, bool, None, ""),
        TmcRegField("internal_rsense", 1, 0x1, bool, None, ""),
        TmcRegField("i_scale_analog", 0, 0x1, bool, None, ""),
    )


class GStat(shared.GStat):
    """GSTAT register class"""

    ADDR = 0x1

    uv_cp: bool
    drv_err: bool
    reset: bool
    _REG_MAP = (
        TmcRegField("uv_cp", 2, 0x1, bool, None, "", 1),
        TmcRegField("drv_err", 1, 0x1, bool, None, "", 1),
        TmcRegField("reset", 0, 0x1, bool, None, "", 1),
    )

    def check(self):
        """check if the driver is ok"""
        self.read()
        if self.uv_cp:
            raise TmcDriverException("TMC220X: undervoltage detected")
        if self.drv_err:
            raise TmcDriverException("TMC220X: driver error detected")
        if self.reset:
            raise TmcDriverException("TMC220X: reset detected")


class IfCnt(shared.IfCnt):
    """IFCNT register class"""

    ADDR = 0x2

    ifcnt: int
    _REG_MAP = (TmcRegField("ifcnt", 0, 0xFF, int, None, ""),)


class Ioin(shared.Ioin):
    """IOIN register class"""

    ADDR = 0x6
    DRIVER_NAME = "TMC220X"

    version: int
    dir: bool
    spread: bool
    step: bool
    ms2: bool
    ms1: bool
    enn: bool
    _REG_MAP = (
        TmcRegField("version", 24, 0xFF, int, None, ""),
        TmcRegField("dir", 9, 0x1, bool, None, ""),
        TmcRegField("spread", 8, 0x1, bool, None, ""),
        TmcRegField("step", 7, 0x1, bool, None, ""),
        TmcRegField("ms2", 3, 0x1, bool, None, ""),
        TmcRegField("ms1", 2, 0x1, bool, None, ""),
        TmcRegField("enn", 0, 0x1, bool, None, ""),
    )


class IHoldIRun(shared.IHoldIRun):
    """IHOLD_IRUN register class"""

    ADDR = 0x10

    iholddelay: int
    irun: int
    ihold: int
    _REG_MAP = (
        TmcRegField("iholddelay", 16, 0xF, int, None, ""),
        TmcRegField("irun", 8, 0x1F, int, None, ""),
        TmcRegField("ihold", 0, 0x1F, int, None, ""),
    )


class TPowerDown(shared.TPowerDown):
    """TPowerDown register class"""

    ADDR = 0x11

    tpowerdown: int
    _REG_MAP = (TmcRegField("tpowerdown", 0, 0xFF, int, None, ""),)


class TStep(shared.TStep):
    """TSTEP register class"""

    ADDR = 0x12

    tstep: int
    _REG_MAP = (TmcRegField("tstep", 0, 0xFFFFF, int, None, ""),)


class TPwmThrs(shared.TPwmThrs):
    """TPWMTHRS register class"""

    ADDR = 0x13

    tpwmthrs: int
    _REG_MAP = (TmcRegField("tpwmthrs", 0, 0xFFFFF, int, None, ""),)


class VActual(shared.VActual):
    """VACTUAL register class"""

    ADDR = 0x22

    vactual: int
    _REG_MAP = (TmcRegField("vactual", 0, 0xFFFFFF, int, None, "", signed=True),)


class MsCnt(shared.MsCnt):
    """MSCNT register class"""

    ADDR = 0x6A

    mscnt: int
    _REG_MAP = (TmcRegField("mscnt", 0, 0xFF, int, None, ""),)


class ChopConf(shared.ChopConf):
    """CHOPCONF register class"""

    ADDR = 0x6C

    diss2vs: bool
    diss2g: bool
    dedge: bool
    intpol: bool
    mres: int
    vsense: bool
    tbl: int
    hend: int
    hstrt: int
    toff: int
    _REG_MAP = (
        TmcRegField("diss2vs", 31, 0x1, bool, None, ""),
        TmcRegField("diss2g", 30, 0x1, bool, None, ""),
        TmcRegField("dedge", 29, 0x1, bool, None, ""),
        TmcRegField("intpol", 28, 0x1, bool, None, ""),
        TmcRegField("mres", 24, 0xF, int, "mres_ms", "mStep"),
        TmcRegField("vsense", 17, 0x1, bool, None, ""),
        TmcRegField("tbl", 15, 0x3, int, None, ""),
        TmcRegField("hend", 7, 0xF, int, None, ""),
        TmcRegField("hstrt", 4, 0x7, int, None, ""),
        TmcRegField("toff", 0, 0xF, int, None, ""),
    )

    @property
    def mres_ms(self) -> int:
        """return µstep resolution"""
        return int(math.pow(2, 8 - self.mres))

    @mres_ms.setter
    def mres_ms(self, mres: int):
        """set µstep resolution"""
        mres_to_bit = {1: 8, 2: 7, 4: 6, 8: 5, 16: 4, 32: 3, 64: 2, 128: 1, 256: 0}
        if mres not in mres_to_bit:
            raise ValueError(
                f"Invalid mres value: {mres}. Must be power of 2 from 1 to 256"
            )
        self.mres = mres_to_bit[mres]


class PwmConf(shared.PwmConf):
    """PWMCONF register class"""

    ADDR = 0x70

    pwm_lim: int
    pwm_reg: int
    freewheel: int
    pwm_autograd: bool
    pwm_autoscale: bool
    pwm_freq: int
    pwm_grad: int
    pwm_ofs: int
    _REG_MAP = (
        TmcRegField("pwm_lim", 28, 0xF, int, None, ""),
        TmcRegField("pwm_reg", 24, 0xF, int, None, ""),
        TmcRegField("freewheel", 20, 0x3, int, None, ""),
        TmcRegField("pwm_autograd", 19, 0x1, bool, None, ""),
        TmcRegField("pwm_autoscale", 18, 0x1, bool, None, ""),
        TmcRegField("pwm_freq", 16, 0x3, int, None, ""),
        TmcRegField("pwm_grad", 8, 0xFF, int, None, ""),
        TmcRegField("pwm_ofs", 0, 0xFF, int, None, ""),
    )


class DrvStatus(shared.DrvStatus):
    """DRVSTATUS register class"""

    ADDR = 0x6F

    stst: bool
    stealth: bool
    cs_actual: int
    t157: bool
    t150: bool
    t143: bool
    t120: bool
    olb: bool
    ola: bool
    s2vsb: bool
    s2vsa: bool
    s2gb: bool
    s2ga: bool
    ot: bool
    otpw: bool
    _REG_MAP = (
        TmcRegField("stst", 31, 0x1, bool, None, ""),
        TmcRegField("stealth", 30, 0x1, bool, None, ""),
        TmcRegField("cs_actual", 16, 0x1F, int, None, ""),
        TmcRegField("t157", 11, 0x1, bool, None, ""),
        TmcRegField("t150", 10, 0x1, bool, None, ""),
        TmcRegField("t143", 9, 0x1, bool, None, ""),
        TmcRegField("t120", 8, 0x1, bool, None, ""),
        TmcRegField("olb", 7, 0x1, bool, None, ""),
        TmcRegField("ola", 6, 0x1, bool, None, ""),
        TmcRegField("s2vsb", 5, 0x1, bool, None, ""),
        TmcRegField("s2vsa", 4, 0x1, bool, None, ""),
        TmcRegField("s2gb", 3, 0x1, bool, None, ""),
        TmcRegField("s2ga", 2, 0x1, bool, None, ""),
        TmcRegField("ot", 1, 0x1, bool, None, ""),
        TmcRegField("otpw", 0, 0x1, bool, None, ""),
    )
