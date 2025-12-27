# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# pylint: disable=too-many-instance-attributes
"""
Register module
"""

import math
from ._tmc_reg import *
from .._tmc_exceptions import TmcDriverException


class GConf(TmcReg):
    """GCONF register class"""

    def __init__(self, tmc_com: TmcCom):
        """constructor"""
        self.test_mode: bool
        self.multistep_filt: bool
        self.mstep_reg_select: bool
        self.pdn_disable: bool
        self.index_step: bool
        self.index_otpw: bool
        self.shaft: bool
        self.en_spreadcycle: bool
        self.internal_rsense: bool
        self.i_scale_analog: bool

        reg_map = [
            ["test_mode", 9, 0x1, bool, None, ""],
            ["multistep_filt", 8, 0x1, bool, None, ""],
            ["mstep_reg_select", 7, 0x1, bool, None, ""],
            ["pdn_disable", 6, 0x1, bool, None, ""],
            ["index_step", 5, 0x1, bool, None, ""],
            ["index_otpw", 4, 0x1, bool, None, ""],
            ["shaft", 3, 0x1, bool, None, ""],
            ["en_spreadcycle", 2, 0x1, bool, None, ""],
            ["internal_rsense", 1, 0x1, bool, None, ""],
            ["i_scale_analog", 0, 0x1, bool, None, ""],
        ]
        super().__init__(0x0, "GCONF", tmc_com, reg_map)


class GStat(TmcReg):
    """GSTAT register class"""

    def __init__(self, tmc_com: TmcCom):
        """constructor"""
        self.uv_cp: bool
        self.drv_err: bool
        self.reset: bool

        reg_map = [
            ["uv_cp", 2, 0x1, bool, None, ""],
            ["drv_err", 1, 0x1, bool, None, ""],
            ["reset", 0, 0x1, bool, None, ""],
        ]
        super().__init__(0x1, "GSTAT", tmc_com, reg_map)

    def check(self):
        """check if the driver is ok"""
        self.read()
        if self.reset:
            raise TmcDriverException("TMC220X: reset detected")
        if self.uv_cp:
            raise TmcDriverException("TMC220X: undervoltage detected")
        if self.drv_err:
            raise TmcDriverException("TMC220X: driver error detected")


class IfCnt(TmcReg):
    """IFCNT register class"""

    def __init__(self, tmc_com: TmcCom):
        """constructor"""
        self.ifcnt: int

        reg_map = [["ifcnt", 0, 0xFF, int, None, ""]]
        super().__init__(0x2, "IFCNT", tmc_com, reg_map)


class Ioin(TmcReg):
    """IOIN register class"""

    def __init__(self, tmc_com: TmcCom):
        """constructor"""
        self.version: int
        self.dir: bool
        self.spread: bool
        self.step: bool
        self.ms2: bool
        self.ms1: bool
        self.enn: bool

        reg_map = [
            ["version", 24, 0xFF, int, None, ""],
            ["dir", 9, 0x1, bool, None, ""],
            ["spread", 8, 0x1, bool, None, ""],
            ["step", 7, 0x1, bool, None, ""],
            ["ms2", 3, 0x1, bool, None, ""],
            ["ms1", 2, 0x1, bool, None, ""],
            ["enn", 0, 0x1, bool, None, ""],
        ]
        super().__init__(0x6, "IOIN", tmc_com, reg_map)


class IHoldIRun(TmcReg):
    """IHOLD_IRUN register class"""

    def __init__(self, tmc_com: TmcCom):
        """constructor"""
        self.iholddelay: int
        self.irun: int
        self.ihold: int

        reg_map = [
            ["iholddelay", 16, 0xF, int, None, ""],
            ["irun", 8, 0x1F, int, None, ""],
            ["ihold", 0, 0x1F, int, None, ""],
        ]
        super().__init__(0x10, "IHOLD_IRUN", tmc_com, reg_map)


class TPowerDown(TmcReg):
    """TPowerDown register class"""

    def __init__(self, tmc_com: TmcCom):
        """constructor"""
        self.tpowerdown: int

        reg_map = [["tpowerdown", 0, 0xFF, int, None, ""]]
        super().__init__(0x11, "TPowerDown", tmc_com, reg_map)


class TStep(TmcReg):
    """TSTEP register class"""

    def __init__(self, tmc_com: TmcCom):
        """constructor"""
        self.tstep: int

        reg_map = [["tstep", 0, 0xFFFFF, int, None, ""]]
        super().__init__(0x12, "TSTEP", tmc_com, reg_map)


class TPwmThrs(TmcReg):
    """TPWMTHRS register class"""

    def __init__(self, tmc_com: TmcCom):
        """constructor"""
        self.tpwmthrs: int

        reg_map = [["tpwmthrs", 0, 0xFFFFF, int, None, ""]]
        super().__init__(0x13, "TPWMTHRS", tmc_com, reg_map)


class VActual(TmcReg):
    """VACTUAL register class"""

    def __init__(self, tmc_com: TmcCom):
        """constructor"""
        self.vactual: int

        reg_map = [["vactual", 0, 0xFFFFFF, int, None, ""]]
        super().__init__(0x22, "VACTUAL", tmc_com, reg_map)


class MsCnt(TmcReg):
    """MSCNT register class"""

    def __init__(self, tmc_com: TmcCom):
        """constructor"""
        self.mscnt: int

        reg_map = [["mscnt", 0, 0xFF, int, None, ""]]
        super().__init__(0x6A, "MSCNT", tmc_com, reg_map)


class ChopConf(TmcReg):
    """CHOPCONF register class"""

    def __init__(self, tmc_com: TmcCom):
        """constructor"""
        self.diss2vs: bool
        self.diss2g: bool
        self.dedge: bool
        self.intpol: bool
        self.mres: int
        self.vsense: bool
        self.tbl: int
        self.hend: int
        self.hstrt: int
        self.toff: int

        reg_map = [
            ["diss2vs", 31, 0x1, bool, None, ""],
            ["diss2g", 30, 0x1, bool, None, ""],
            ["dedge", 29, 0x1, bool, None, ""],
            ["intpol", 28, 0x1, bool, None, ""],
            ["mres", 24, 0xF, int, lambda: self.mres_ms, "mStep"],
            ["vsense", 17, 0x1, bool, None, ""],
            ["tbl", 15, 0x3, int, None, ""],
            ["hend", 7, 0xF, int, None, ""],
            ["hstrt", 4, 0x7, int, None, ""],
            ["toff", 0, 0xF, int, None, ""],
        ]
        super().__init__(0x6C, "CHOPCONF", tmc_com, reg_map)

    @property
    def mres_ms(self) -> int:
        """return µstep resolution"""
        return int(math.pow(2, 8 - self.mres))

    @mres_ms.setter
    def mres_ms(self, mres: int):
        """set µstep resolution"""
        mres_bit = int(math.log2(mres))
        mres_bit = 8 - mres_bit
        self.mres = mres_bit


class PwmConf(TmcReg):
    """PWMCONF register class"""

    def __init__(self, tmc_com: TmcCom):
        """constructor"""
        self.pwm_lim: int
        self.pwm_reg: int
        self.freewheel: int
        self.pwm_autograd: bool
        self.pwm_autoscale: bool
        self.pwm_freq: int
        self.pwm_grad: int
        self.pwm_ofs: int

        reg_map = [
            ["pwm_lim", 28, 0xF, int, None, ""],
            ["pwm_reg", 24, 0xF, int, None, ""],
            ["freewheel", 20, 0x3, int, None, ""],
            ["pwm_autograd", 19, 0x1, bool, None, ""],
            ["pwm_autoscale", 18, 0x1, bool, None, ""],
            ["pwm_freq", 16, 0x3, int, None, ""],
            ["pwm_grad", 8, 0xFF, int, None, ""],
            ["pwm_ofs", 0, 0xFF, int, None, ""],
        ]
        super().__init__(0x70, "PWMCONF", tmc_com, reg_map)


class DrvStatus(TmcReg):
    """DRVSTATUS register class"""

    def __init__(self, tmc_com: TmcCom):
        """constructor"""
        self.stst: bool
        self.stealth: bool
        self.cs_actual: int
        self.t157: bool
        self.t150: bool
        self.t143: bool
        self.t120: bool
        self.olb: bool
        self.ola: bool
        self.s2vsb: bool
        self.s2vsa: bool
        self.s2gb: bool
        self.s2ga: bool
        self.ot: bool
        self.otpw: bool

        reg_map = [
            ["stst", 31, 0x1, bool, None, ""],
            ["stealth", 30, 0x1, bool, None, ""],
            ["cs_actual", 16, 0x1F, int, None, ""],
            ["t157", 11, 0x1, bool, None, ""],
            ["t150", 10, 0x1, bool, None, ""],
            ["t143", 9, 0x1, bool, None, ""],
            ["t120", 8, 0x1, bool, None, ""],
            ["olb", 7, 0x1, bool, None, ""],
            ["ola", 6, 0x1, bool, None, ""],
            ["s2vsb", 5, 0x1, bool, None, ""],
            ["s2vsa", 4, 0x1, bool, None, ""],
            ["s2gb", 3, 0x1, bool, None, ""],
            ["s2ga", 2, 0x1, bool, None, ""],
            ["ot", 1, 0x1, bool, None, ""],
            ["otpw", 0, 0x1, bool, None, ""],
        ]
        super().__init__(0x6F, "DRVSTATUS", tmc_com, reg_map)
