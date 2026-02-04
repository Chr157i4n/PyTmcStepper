# pylint: disable=too-many-instance-attributes
"""Register module."""

import math
from ._tmc_reg import TmcRegField
from . import _tmc_shared_regs as shared
from .._tmc_exceptions import TmcDriverException


class GConf(shared.GConf):
    """GCONF register class."""

    ADDR = 0x0

    direct_mode: bool
    stop_enable: bool
    small_hysteresis: bool
    diag1_pushpull: bool
    diag0_pushpull: bool
    diag1_steps_skipped: bool
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
    recalibrate: bool
    _REG_MAP = (
        TmcRegField("direct_mode", 16, 0x1, bool, None, ""),
        TmcRegField("stop_enable", 15, 0x1, bool, None, ""),
        TmcRegField("small_hysteresis", 14, 0x1, bool, None, ""),
        TmcRegField("diag1_pushpull", 13, 0x1, bool, None, ""),
        TmcRegField("diag0_pushpull", 12, 0x1, bool, None, ""),
        TmcRegField("diag1_steps_skipped", 11, 0x1, bool, None, ""),
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
        TmcRegField("recalibrate", 0, 0x1, bool, None, ""),
    )


class GStat(shared.GStat):
    """GSTAT register class."""

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
        """Check if the driver is ok."""
        self.read()
        if self.uv_cp:
            raise TmcDriverException("TMC224X: Charge Pump undervoltage detected")
        if self.drv_err:
            raise TmcDriverException("TMC224X: driver error detected")
        if self.reset:
            raise TmcDriverException("TMC224X: reset detected")


class IfCnt(shared.IfCnt):
    """IFCNT register class."""

    ADDR = 0x2

    ifcnt: int
    _REG_MAP = (TmcRegField("ifcnt", 0, 0xFF, int, None, ""),)


class Ioin(shared.Ioin):
    """IOIN register class."""

    ADDR = 0x4
    DRIVER_NAME = "TMC5160"

    version: int
    sw_comp_in: bool
    sd_mode: bool
    encn: bool
    enn: bool
    enca: bool
    encb: bool
    dir: bool
    step: bool
    _REG_MAP = (
        TmcRegField("version", 24, 0xFF, int, None, ""),
        TmcRegField("sw_comp_in", 7, 0x1, bool, None, ""),
        TmcRegField("sd_mode", 6, 0x1, bool, None, ""),
        TmcRegField("encn", 5, 0x1, bool, None, ""),
        TmcRegField("enn", 4, 0x1, bool, None, ""),
        TmcRegField("enca", 3, 0x1, bool, None, ""),
        TmcRegField("encb", 2, 0x1, bool, None, ""),
        TmcRegField("dir", 1, 0x1, bool, None, ""),
        TmcRegField("step", 0, 0x1, bool, None, ""),
    )


class DrvConf(shared.DrvConf):
    """DRV_CONF register class."""

    ADDR = 0xA

    filt_isense: int
    drvstrength: int
    otselect: int
    bbmclks: int
    bbmtime: int
    _REG_MAP = (
        TmcRegField("filt_isense", 20, 0x3, int, None, ""),
        TmcRegField("drvstrength", 18, 0x3, int, None, ""),
        TmcRegField("otselect", 16, 0x3, int, None, ""),
        TmcRegField("bbmclks", 8, 0xF, int, None, ""),
        TmcRegField("bbmtime", 0, 0x1F, int, None, ""),
    )


class GlobalScaler(shared.GlobalScaler):
    """GLOBAL_SCALER register class."""

    ADDR = 0xB

    global_scaler: int
    _REG_MAP = (TmcRegField("global_scaler", 0, 0xFF, int, None, ""),)


class IHoldIRun(shared.IHoldIRun):
    """IHOLD_IRUN register class."""

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
    """TPOWERDOWN register class."""

    ADDR = 0x11

    tpowerdown: int
    _REG_MAP = (TmcRegField("tpowerdown", 0, 0xFF, int, None, ""),)


class TStep(shared.TStep):
    """TSTEP register class."""

    ADDR = 0x12

    tstep: int
    _REG_MAP = (TmcRegField("tstep", 0, 0xFFFFF, int, None, ""),)


class TPwmThrs(shared.TPwmThrs):
    """TCOOLTHRS register class."""

    ADDR = 0x13

    tpwmthrs: int
    _REG_MAP = (TmcRegField("tpwmthrs", 0, 0xFFFFF, int, None, ""),)


class TCoolThrs(shared.TCoolThrs):
    """TCOOLTHRS register class."""

    ADDR = 0x14

    tcoolthrs: int
    _REG_MAP = (TmcRegField("tcoolthrs", 0, 0xFFFFF, int, None, ""),)


class THigh(shared.THigh):
    """THIGH register class."""

    ADDR = 0x15

    thigh: int
    _REG_MAP = (TmcRegField("thigh", 0, 0xFFFFF, int, None, ""),)


class VDcMin(shared.VDcMin):
    """VDCMIN register class."""

    ADDR = 0x33

    vdcmin: int
    _REG_MAP = (TmcRegField("vdcmin", 0, 0xFFFFF, int, None, ""),)


class RampMode(shared.RampMode):
    """RAMPMODE register class."""

    ADDR = 0x20

    rampmode: int
    _REG_MAP = (TmcRegField("rampmode", 0, 0xFFFFF, int, None, ""),)


class XActual(shared.XActual):
    """XACTUAL register class - Actual motor position (signed)."""

    ADDR = 0x21

    xactual: int
    _REG_MAP = (TmcRegField("xactual", 0, 0xFFFFFFFF, int, None, "", signed=True),)


class VActual(shared.VActual):
    """VACTUAL register class - Actual motor velocity (signed)."""

    ADDR = 0x22

    vactual: int
    _REG_MAP = (TmcRegField("vactual", 0, 0xFFFFFF, int, None, "", signed=True),)


class VStart(shared.VStart):
    """VSTART register class."""

    ADDR = 0x23

    vstart: int
    _REG_MAP = (TmcRegField("vstart", 0, 0xFFFFF, int, None, ""),)


class A1(shared.A1):
    """A1 register class."""

    ADDR = 0x24

    a1: int
    _REG_MAP = (TmcRegField("a1", 0, 0xFFFFF, int, None, ""),)


class V1(shared.V1):
    """V1 register class."""

    ADDR = 0x25

    v1: int
    _REG_MAP = (TmcRegField("v1", 0, 0xFFFFF, int, None, ""),)


class AMax(shared.AMax):
    """AMAX register class."""

    ADDR = 0x26

    amax: int
    _REG_MAP = (TmcRegField("amax", 0, 0xFFFFF, int, None, ""),)


class VMax(shared.VMax):
    """VMAX register class."""

    ADDR = 0x27

    vmax: int
    _REG_MAP = (TmcRegField("vmax", 0, 0xFFFFF, int, None, ""),)


class DMax(shared.DMax):
    """DMAX register class."""

    ADDR = 0x28

    dmax: int
    _REG_MAP = (TmcRegField("dmax", 0, 0xFFFFF, int, None, ""),)


class D1(shared.D1):
    """D1 register class."""

    ADDR = 0x2A

    d1: int
    _REG_MAP = (TmcRegField("d1", 0, 0xFFFFF, int, None, ""),)


class VStop(shared.VStop):
    """VSTOP register class."""

    ADDR = 0x2B

    vstop: int
    _REG_MAP = (TmcRegField("vstop", 0, 0xFFFFF, int, None, ""),)


class TZeroWait(shared.TZeroWait):
    """TZEROWAIT register class."""

    ADDR = 0x2C

    tzerowait: int
    _REG_MAP = (TmcRegField("tzerowait", 0, 0xFFFFF, int, None, ""),)


class XTarget(shared.XTarget):
    """XTARGET register class - Target position for ramp mode (signed)."""

    ADDR = 0x2D

    xtarget: int
    _REG_MAP = (TmcRegField("xtarget", 0, 0xFFFFFFFF, int, None, "", signed=True),)


class SWMode(shared.SWMode):
    """SW_MODE register class."""

    ADDR = 0x34

    en_softstop: bool
    sg_stop: bool
    en_latch_encoder: bool
    latch_r_inactive: bool
    latch_r_active: bool
    latch_l_inactive: bool
    latch_l_active: bool
    swap_lr: bool
    pol_stop_r: bool
    pol_stop_l: bool
    stop_r_enable: bool
    stop_l_enable: bool
    _REG_MAP = (
        TmcRegField("en_softstop", 11, 0x1, bool, None, ""),
        TmcRegField("sg_stop", 10, 0x1, bool, None, ""),
        TmcRegField("en_latch_encoder", 9, 0x1, bool, None, ""),
        TmcRegField("latch_r_inactive", 8, 0x1, bool, None, ""),
        TmcRegField("latch_r_active", 7, 0x1, bool, None, ""),
        TmcRegField("latch_l_inactive", 6, 0x1, bool, None, ""),
        TmcRegField("latch_l_active", 5, 0x1, bool, None, ""),
        TmcRegField("swap_lr", 4, 0x1, bool, None, ""),
        TmcRegField("pol_stop_r", 3, 0x1, bool, None, ""),
        TmcRegField("pol_stop_l", 2, 0x1, bool, None, ""),
        TmcRegField("stop_r_enable", 1, 0x1, bool, None, ""),
        TmcRegField("stop_l_enable", 0, 0x1, bool, None, ""),
    )


class RampStat(shared.RampStat):
    """RAMP_STAT register class."""

    ADDR = 0x35

    status_sg: bool
    second_move: bool
    t_zerowait_active: bool
    vzero: bool
    position_reached: bool
    velocity_reached: bool
    event_stop_sg: bool
    event_stop_r: bool
    event_stop_l: bool
    status_latch_r: bool
    status_latch_l: bool
    status_stop_r: bool
    status_stop_l: bool
    _REG_MAP = (
        TmcRegField("status_sg", 13, 0x1, bool, None, ""),
        TmcRegField("second_move", 12, 0x1, bool, None, "", 1),
        TmcRegField("t_zerowait_active", 11, 0x1, bool, None, ""),
        TmcRegField("vzero", 10, 0x1, bool, None, ""),
        TmcRegField("position_reached", 9, 0x1, bool, None, ""),
        TmcRegField("velocity_reached", 8, 0x1, bool, None, ""),
        TmcRegField("event_pos_reached", 7, 0x1, bool, None, "", 1),
        TmcRegField("event_stop_sg", 6, 0x1, bool, None, "", 1),
        TmcRegField("event_stop_r", 5, 0x1, bool, None, ""),
        TmcRegField("event_stop_l", 4, 0x1, bool, None, ""),
        TmcRegField("status_latch_r", 3, 0x1, bool, None, "", 1),
        TmcRegField("status_latch_l", 2, 0x1, bool, None, "", 1),
        TmcRegField("status_stop_r", 1, 0x1, bool, None, ""),
        TmcRegField("status_stop_l", 0, 0x1, bool, None, ""),
    )


class MsCnt(shared.MsCnt):
    """MSCNT register class."""

    ADDR = 0x6A

    mscnt: int
    _REG_MAP = (TmcRegField("mscnt", 0, 0xFF, int, None, ""),)


class ChopConf(shared.ChopConf):
    """CHOPCONF register class."""

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
        """Return µstep resolution."""
        return int(math.pow(2, 8 - self.mres))

    @mres_ms.setter
    def mres_ms(self, mres: int):
        """Set µstep resolution."""
        mres_to_bit = {1: 8, 2: 7, 4: 6, 8: 5, 16: 4, 32: 3, 64: 2, 128: 1, 256: 0}
        if mres not in mres_to_bit:
            raise ValueError(
                f"Invalid mres value: {mres}. Must be power of 2 from 1 to 256"
            )
        self.mres = mres_to_bit[mres]


class CoolConf(shared.CoolConf):
    """COOLCONF register class."""

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
        TmcRegField("sgt", 16, 0x7F, int, None, "", signed=True),
        TmcRegField("seimin", 15, 0x1, bool, None, ""),
        TmcRegField("sedn", 13, 0x3, int, None, ""),
        TmcRegField("semax", 8, 0xF, int, None, ""),
        TmcRegField("seup", 5, 0x3, int, None, ""),
        TmcRegField("semin", 0, 0xF, int, None, ""),
    )


class DrvStatus(shared.DrvStatus):
    """DRVSTATUS register class."""

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


class LostSteps(shared.LostSteps):
    """LOST_STEPS register class."""

    ADDR = 0x73

    lost_steps: int
    _REG_MAP = (TmcRegField("lost_steps", 0, 0xFFFFF, int, None, ""),)
