# pylint: disable=too-many-instance-attributes
"""
Register module
"""

import math
from ._tmc_reg import TmcReg, TmcRegField
from .._tmc_exceptions import TmcDriverException


class GConf(TmcReg):
    """GCONF register class"""

    ADDR = 0x0

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
    shaft: bool
    multistep_filt: bool
    en_pwm_mode: bool
    fast_standstill: bool
    _REG_MAP = (
        TmcRegField("direct_mode", 16, 0x1, bool, None, ""),
        TmcRegField("stop_enable", 15, 0x1, bool, None, ""),
        TmcRegField("small_hysteresis", 14, 0x1, bool, None, ""),
        TmcRegField("diag1_pushpull", 13, 0x1, bool, None, ""),
        TmcRegField("diag0_pushpull", 12, 0x1, bool, None, ""),
        TmcRegField("diag1_onstate", 10, 0x1, bool, None, ""),
        TmcRegField("diag1_index", 9, 0x1, bool, None, ""),
        TmcRegField("diag1_stall", 8, 0x1, bool, None, ""),
        TmcRegField("diag0_stall", 7, 0x1, bool, None, ""),
        TmcRegField("diag0_otpw", 6, 0x1, bool, None, ""),
        TmcRegField("diag0_error", 5, 0x1, bool, None, ""),
        TmcRegField("shaft", 4, 0x1, bool, None, ""),
        TmcRegField("multistep_filt", 3, 0x1, bool, None, ""),
        TmcRegField("en_pwm_mode", 2, 0x1, bool, None, ""),
        TmcRegField("fast_standstill", 1, 0x1, bool, None, ""),
    )


class GStat(TmcReg):
    """GSTAT register class"""

    ADDR = 0x1

    vm_uvlo: bool
    register_reset: bool
    uv_cp: bool
    drv_err: bool
    reset: bool
    _REG_MAP = (
        TmcRegField("vm_uvlo", 4, 0x1, bool, None, "", 1),
        TmcRegField("register_reset", 3, 0x1, bool, None, "", 1),
        TmcRegField("uv_cp", 2, 0x1, bool, None, "", 1),
        TmcRegField("drv_err", 1, 0x1, bool, None, "", 1),
        TmcRegField("reset", 0, 0x1, bool, None, "", 1),
    )

    def check(self):
        """check if the driver is ok"""
        self.read()
        if self.vm_uvlo:
            raise TmcDriverException("TMC224X: Vmotor undervoltage detected")
        if self.register_reset:
            raise TmcDriverException("TMC224X: register reset detected")
        if self.uv_cp:
            raise TmcDriverException("TMC224X: Charge Pump undervoltage detected")
        if self.drv_err:
            raise TmcDriverException("TMC224X: driver error detected")
        if self.reset:
            raise TmcDriverException("TMC224X: reset detected")


class IfCnt(TmcReg):
    """IFCNT register class"""

    ADDR = 0x2

    ifcnt: int
    _REG_MAP = (TmcRegField("ifcnt", 0, 0xFF, int, None, ""),)


class Ioin(TmcReg):
    """IOIN register class"""

    ADDR = 0x4

    version: int
    silicon_rv: int
    adc_err: bool
    ext_clk: bool
    ext_res_det: bool
    output: bool
    comp_b1_b2: bool
    comp_a1_a2: bool
    comp_b: bool
    comp_a: bool
    uart_en: bool
    encn: bool
    enn: bool
    enca: bool
    encb: bool
    dir: bool
    step: bool
    _REG_MAP = (
        TmcRegField("version", 24, 0xFF, int, None, ""),
        TmcRegField("silicon_rv", 24, 0xFF, int, None, ""),
        TmcRegField("adc_err", 15, 0x1, bool, None, ""),
        TmcRegField("ext_clk", 14, 0x1, bool, None, ""),
        TmcRegField("ext_res_det", 13, 0x1, bool, None, ""),
        TmcRegField("output", 12, 0x1, bool, None, ""),
        TmcRegField("comp_b1_b2", 11, 0x1, bool, None, ""),
        TmcRegField("comp_a1_a2", 10, 0x1, bool, None, ""),
        TmcRegField("comp_b", 9, 0x1, bool, None, ""),
        TmcRegField("comp_a", 8, 0x1, bool, None, ""),
        TmcRegField("uart_en", 6, 0x1, bool, None, ""),
        TmcRegField("encn", 5, 0x1, bool, None, ""),
        TmcRegField("enn", 4, 0x1, bool, None, ""),
        TmcRegField("enca", 3, 0x1, bool, None, ""),
        TmcRegField("encb", 2, 0x1, bool, None, ""),
        TmcRegField("dir", 1, 0x1, bool, None, ""),
        TmcRegField("step", 0, 0x1, bool, None, ""),
    )


class DrvConf(TmcReg):
    """DRV_CONF register class"""

    ADDR = 0x6

    slope_control: int
    current_range: int
    _REG_MAP = (
        TmcRegField("slope_control", 4, 0x3, int, None, ""),
        TmcRegField("current_range", 0, 0x3, int, None, ""),
    )


class GlobalScaler(TmcReg):
    """GLOBAL_SCALER register class"""

    ADDR = 0xB

    global_scaler: int
    _REG_MAP = (TmcRegField("global_scaler", 0, 0xFF, int, None, ""),)


class IHoldIRun(TmcReg):
    """IHOLD_IRUN register class"""

    ADDR = 0x10

    irundelay: int
    iholddelay: int
    irun: int
    ihold: int
    _REG_MAP = (
        TmcRegField("irundelay", 24, 0xF, int, None, ""),
        TmcRegField("iholddelay", 16, 0xF, int, None, ""),
        TmcRegField("irun", 8, 0x1F, int, None, ""),
        TmcRegField("ihold", 0, 0x1F, int, None, ""),
    )


class TPowerDown(TmcReg):
    """TPOWERDOWN register class"""

    ADDR = 0x11

    tpowerdown: int
    _REG_MAP = (TmcRegField("tpowerdown", 0, 0xFF, int, None, ""),)


class TStep(TmcReg):
    """TSTEP register class"""

    ADDR = 0x12

    tstep: int
    _REG_MAP = (TmcRegField("tstep", 0, 0xFFFFF, int, None, ""),)


class TPwmThrs(TmcReg):
    """TCOOLTHRS register class"""

    ADDR = 0x13

    tpwmthrs: int
    _REG_MAP = (TmcRegField("tpwmthrs", 0, 0xFFFFF, int, None, ""),)


class TCoolThrs(TmcReg):
    """TCOOLTHRS register class"""

    ADDR = 0x14

    tcoolthrs: int
    _REG_MAP = (TmcRegField("tcoolthrs", 0, 0xFFFFF, int, None, ""),)


class THigh(TmcReg):
    """THIGH register class"""

    ADDR = 0x15

    thigh: int
    _REG_MAP = (TmcRegField("thigh", 0, 0xFFFFF, int, None, ""),)


class ADCVSupplyAIN(TmcReg):
    """ADCV_SUPPLY_AIN register class"""

    ADDR = 0x50

    adc_ain: int
    adc_vsupply: int
    _REG_MAP = (
        TmcRegField("adc_ain", 16, 0xFFFF, int, "adc_ain_v", "V"),
        TmcRegField("adc_vsupply", 0, 0xFFFF, int, "adc_vsupply_v", "V"),
    )

    @property
    def adc_vsupply_v(self) -> float:
        """return Supplyvoltage in V"""
        return round(self.adc_vsupply * 9.732 / 1000, 2)

    @property
    def adc_ain_v(self) -> float:
        """return voltage on AIN in V"""
        return round(self.adc_ain * 305.2 / 1000 / 1000, 2)


class ADCTemp(TmcReg):
    """ADC_TEMP register class"""

    ADDR = 0x51

    adc_temp: int
    _REG_MAP = (TmcRegField("adc_temp", 0, 0xFFFF, int, "adc_temp_c", "°C"),)

    @property
    def adc_temp_c(self) -> float:
        """return temperature in °C"""
        return round((self.adc_temp - 2038) / 7.7, 1)


class MsCnt(TmcReg):
    """MSCNT register class"""

    ADDR = 0x6A

    mscnt: int
    _REG_MAP = (TmcRegField("mscnt", 0, 0xFF, int, None, ""),)


class ChopConf(TmcReg):
    """CHOPCONF register class"""

    ADDR = 0x6C

    diss2vs: bool
    diss2g: bool
    dedge: bool
    intpol: bool
    mres: int
    tpfd: int
    vhighchm: bool
    vhighfs: bool
    tbl: int
    chm: int
    disfdcc: bool
    fd3: bool
    hend_offset: int
    hstrt_tfd210: int
    toff: int
    _REG_MAP = (
        TmcRegField("diss2vs", 31, 0x1, bool, None, ""),
        TmcRegField("diss2g", 30, 0x1, bool, None, ""),
        TmcRegField("dedge", 29, 0x1, bool, None, ""),
        TmcRegField("intpol", 28, 0x1, bool, None, ""),
        TmcRegField("mres", 24, 0xF, int, "mres_ms", "mStep"),
        TmcRegField("tpfd", 20, 0xF, int, None, ""),
        TmcRegField("vhighchm", 19, 0x1, bool, None, ""),
        TmcRegField("vhighfs", 18, 0x1, bool, None, ""),
        TmcRegField("tbl", 15, 0x3, int, None, ""),
        TmcRegField("chm", 14, 0x3, int, None, ""),
        TmcRegField("disfdcc", 12, 0x1, bool, None, ""),
        TmcRegField("fd3", 11, 0x1, bool, None, ""),
        TmcRegField("hend_offset", 7, 0xF, int, None, ""),
        TmcRegField("hstrt_tfd210", 4, 0x7, int, None, ""),
        TmcRegField("toff", 0, 0xF, int, None, ""),
    )

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


class CoolConf(TmcReg):
    """COOLCONF register class"""

    ADDR = 0x6D

    sfilt: bool
    sgt: int
    seimin: bool
    sedn: int
    semax: int
    seup: int
    semin: int
    _REG_MAP = (
        TmcRegField("sfilt", 24, 0x1, bool, None, ""),
        TmcRegField("sgt", 16, 0x7F, int, None, ""),
        TmcRegField("seimin", 15, 0x1, bool, None, ""),
        TmcRegField("sedn", 13, 0x3, int, None, ""),
        TmcRegField("semax", 8, 0xF, int, None, ""),
        TmcRegField("seup", 5, 0x3, int, None, ""),
        TmcRegField("semin", 0, 0xF, int, None, ""),
    )


class DrvStatus(TmcReg):
    """DRVSTATUS register class"""

    ADDR = 0x6F

    stst: bool
    olb: bool
    ola: bool
    s2gb: bool
    s2ga: bool
    otpw: bool
    ot: bool
    stallguard: bool
    cs_actual: int
    fsactive: bool
    stealth: bool
    s2vsb: bool
    s2vsa: bool
    sgresult: int
    _REG_MAP = (
        TmcRegField("stst", 31, 0x1, bool, None, ""),
        TmcRegField("olb", 30, 0x1, bool, None, ""),
        TmcRegField("ola", 29, 0x1, bool, None, ""),
        TmcRegField("s2gb", 28, 0x1, bool, None, ""),
        TmcRegField("s2ga", 27, 0x1, bool, None, ""),
        TmcRegField("otpw", 26, 0x1, bool, None, ""),
        TmcRegField("ot", 25, 0x1, bool, None, ""),
        TmcRegField("stallguard", 24, 0x1, bool, None, ""),
        TmcRegField("cs_actual", 16, 0x1F, int, None, ""),
        TmcRegField("fsactive", 15, 0x1, bool, None, ""),
        TmcRegField("stealth", 14, 0x1, bool, None, ""),
        TmcRegField("s2vsb", 13, 0x1, bool, None, ""),
        TmcRegField("s2vsa", 12, 0x1, bool, None, ""),
        TmcRegField("sgresult", 0, 0x3FF, int, None, ""),
    )


class SgThrs(TmcReg):
    """SGTHRS register class"""

    ADDR = 0x74

    sg_angle_offset: bool
    sg4_filt_en: bool
    sgthrs: int
    _REG_MAP = (
        TmcRegField("sg_angle_offset", 9, 0x1, bool, None, ""),
        TmcRegField("sg4_filt_en", 8, 0x1, bool, None, ""),
        TmcRegField("sgthrs", 0, 0xFFF, int, None, ""),
    )


class SgResult(TmcReg):
    """SGRESULT register class"""

    ADDR = 0x75

    sgresult: int
    _REG_MAP = (TmcRegField("sgresult", 0, 0xFFFFF, int, None, ""),)


class SgInd(TmcReg):
    """SGIND register class"""

    ADDR = 0x76

    sg_ind_2: int
    sg_ind_1: int
    sg_ind_0: int
    _REG_MAP = (
        TmcRegField("sg_ind_2", 16, 0xFF, int, None, ""),
        TmcRegField("sg_ind_1", 8, 0xFF, int, None, ""),
        TmcRegField("sg_ind_0", 0, 0xFF, int, None, ""),
    )
