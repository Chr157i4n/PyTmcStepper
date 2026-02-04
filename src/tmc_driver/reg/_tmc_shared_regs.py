# pylint: disable=too-many-instance-attributes
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# pylint: disable=too-few-public-methods
"""Register module with shared registers without implementation.

Registers only contain the register fields shared between all TMC chips.
"""

from ._tmc_reg import TmcReg


class GStat(TmcReg):
    """GSTAT register class stub."""

    uv_cp: bool
    drv_err: bool
    reset: bool


class IfCnt(TmcReg):
    """IFCNT register class stub."""

    ifcnt: int


class Ioin(TmcReg):
    """IOIN register class stub."""

    version: int
    enn: bool
    dir: bool
    step: bool


class DrvConf(TmcReg):
    """DRV_CONF register class stub."""

    slope_control: int
    current_range: int


class GlobalScaler(TmcReg):
    """GLOBAL_SCALER register class stub."""

    global_scaler: int


class IHoldIRun(TmcReg):
    """IHOLD_IRUN register class stub."""

    iholddelay: int
    irun: int
    ihold: int


class TPowerDown(TmcReg):
    """TPowerDown register class stub."""

    tpowerdown: int


class TStep(TmcReg):
    """TSTEP register class stub."""

    tstep: int


class TPwmThrs(TmcReg):
    """TPWMTHRS register class stub."""

    tpwmthrs: int


class TCoolThrs(TmcReg):
    """TCOOLTHRS register class stub."""

    tcoolthrs: int


class THigh(TmcReg):
    """THIGH register class stub."""

    thigh: int


class ADCVSupplyAIN(TmcReg):
    """ADCV_SUPPLY_AIN register class stub."""

    adc_ain: int
    adc_vsupply: int


class ADCTemp(TmcReg):
    """ADC_TEMP register class stub."""

    adc_temp: int


class MsCnt(TmcReg):
    """MSCNT register class stub."""

    mscnt: int


class ChopConf(TmcReg):
    """CHOPCONF register class stub."""

    diss2vs: bool
    diss2g: bool
    dedge: bool
    intpol: bool
    mres: int
    mres_ms: int
    tbl: int
    hend: int
    hstrt: int
    toff: int


class GConf(TmcReg):
    """GCONF register class stub.

    has all fields of the GCONF register from all TMC chips combined
    into one class. actual chips will only use a subset of these fields.
    """

    multistep_filt: bool
    shaft: bool


class VDcMin(TmcReg):
    """THIGH register class stub."""

    vdcmin: int


class RampMode(TmcReg):
    """THIGH register class stub."""

    rampmode: int


class XActual(TmcReg):
    """THIGH register class stub."""

    xactual: int


class VActual(TmcReg):
    """VACTUAL register class stub."""

    vactual: int


class VStart(TmcReg):
    """THIGH register class stub."""

    vstart: int


class A1(TmcReg):
    """THIGH register class stub."""

    a1: int


class V1(TmcReg):
    """THIGH register class stub."""

    v1: int


class AMax(TmcReg):
    """THIGH register class stub."""

    amax: int


class VMax(TmcReg):
    """THIGH register class stub."""

    vmax: int


class DMax(TmcReg):
    """THIGH register class stub."""

    dmax: int


class D1(TmcReg):
    """THIGH register class stub."""

    d1: int


class VStop(TmcReg):
    """THIGH register class stub."""

    vstop: int


class TZeroWait(TmcReg):
    """THIGH register class stub."""

    tzerowait: int


class XTarget(TmcReg):
    """THIGH register class stub."""

    xtarget: int


class SWMode(TmcReg):
    """THIGH register class stub."""

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


class RampStat(TmcReg):
    """THIGH register class stub."""

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


class PwmConf(TmcReg):
    """PWMCONF register class stub."""

    pwm_lim: int
    pwm_reg: int
    freewheel: int
    pwm_autograd: bool
    pwm_autoscale: bool
    pwm_freq: int
    pwm_grad: int
    pwm_ofs: int


class CoolConf(TmcReg):
    """COOLCONF register class stub."""

    seimin: bool
    sedn: int
    semax: int
    seup: int
    semin: int


class DrvStatus(TmcReg):
    """DRVSTATUS register class stub."""

    stst: bool
    stealth: bool
    cs_actual: int
    olb: bool
    ola: bool
    s2vsb: bool
    s2vsa: bool
    s2gb: bool
    s2ga: bool
    ot: bool
    otpw: bool


class SgThrs(TmcReg):
    """SGTHRS register class stub."""

    sgthrs: int


class SgResult(TmcReg):
    """SGRESULT register class stub."""

    sgresult: int


class SgInd(TmcReg):
    """SGIND register class stub."""

    sg_ind_2: int
    sg_ind_1: int
    sg_ind_0: int


class LostSteps(TmcReg):
    """LOST_STEPS register class stub."""

    lost_steps: int
