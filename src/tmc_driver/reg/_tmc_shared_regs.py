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


class IfCnt(TmcReg):
    """IFCNT register class stub"""

    ifcnt: int


class Ioin(TmcReg):
    """IOIN register class stub"""

    version: int
    dir: bool
    step: bool
    enn: bool


class MsCnt(TmcReg):
    """MSCNT register class stub"""

    mscnt: int


class ChopConf(TmcReg):
    """CHOPCONF register class stub"""

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


class GConf(TmcReg):
    """GCONF register class stub

    has all fields of the GCONF register from all TMC chips
    combined into one class. actual chips will only use a subset of these
    fields.
    """

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
    direct_mode: bool
    stop_enable: bool
    small_hysteresis: bool
    diag1_pushpull: bool
    diag0_pushpull: bool
    diag1_onstate: bool
    diag1_index: bool
    diag1_stall: bool
    diag0_stall: bool
    diag0_otpw: bool
    diag0_error: bool
    en_pwm_mode: bool
    fast_standstill: bool


class VActual(TmcReg):
    """VACTUAL register class stub"""

    vactual: int
