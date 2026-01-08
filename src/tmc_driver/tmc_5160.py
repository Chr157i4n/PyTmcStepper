# pylint: disable=unused-import
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-public-methods
"""Tmc5160 stepper driver module

this module has two different functions:
1. access register via tmc_com (UART, SPI)
2. Enable motor control via tmc_ec (TOFF, PIN)
3. move the motor via tmc_mc (STEP/DIR, STEP/REG, VACTUAL)
"""

from ._tmc_xxxx import *
from .com._tmc_com import TmcCom
from .com._tmc_com_spi_base import TmcComSpiBase
from .com._tmc_com_uart_base import TmcComUartBase
from . import tmc_gpio
from .motion_control._tmc_mc_step_reg import TmcMotionControlStepDir
from .motion_control._tmc_mc_step_reg import TmcMotionControlStepReg
from .motion_control._tmc_mc_step_pwm_dir import TmcMotionControlStepPwmDir
from .motion_control._tmc_mc_int_ramp_generator import TmcMotionControlIntRampGenerator
from .enable_control._tmc_ec_toff import TmcEnableControlToff
from .enable_control._tmc_ec_pin import TmcEnableControlPin
from ._tmc_stallguard import StallGuard
from .tmc_logger import *
from .reg._tmc5160_reg import *
from ._tmc_exceptions import (
    TmcException,
    TmcComException,
    TmcMotionControlException,
    TmcEnableControlException,
    TmcDriverException,
)


class Tmc5160(TmcXXXX, StallGuard):
    """Tmc5160"""

    SUPPORTED_COM_TYPES = (TmcComSpiBase, TmcComUartBase)
    SUPPORTED_EC_TYPES = (TmcEnableControlToff, TmcEnableControlPin)
    SUPPORTED_MC_TYPES = (
        TmcMotionControlStepDir,
        TmcMotionControlStepReg,
        TmcMotionControlStepPwmDir,
        TmcMotionControlIntRampGenerator,
    )
    DRIVER_FAMILY = "TMC5160"

    # Constructor/Destructor
    # ----------------------------
    def __init__(
        self,
        tmc_ec: TmcEnableControl,
        tmc_mc: TmcMotionControl,
        tmc_com: TmcCom | None = None,
        driver_address: int = 0,
        gpio_mode=None,
        loglevel: Loglevel = Loglevel.INFO,
        logprefix: str | None = None,
        log_handlers: list | None = None,
        log_formatter: logging.Formatter | None = None,
    ):
        """constructor

        Args:
            tmc_ec (TmcEnableControl): enable control object
            tmc_mc (TmcMotionControl): motion control object
            tmc_com (TmcCom, optional): communication object. Defaults to None.
            driver_address (int, optional): driver address [0-3]. Defaults to 0.
            gpio_mode (enum, optional): gpio mode. Defaults to None.
            loglevel (enum, optional): loglevel. Defaults to None.
            logprefix (str, optional): log prefix (name of the logger).
                Defaults to None (standard TMC prefix).
            log_handlers (list, optional): list of logging handlers.
                Defaults to None (log to console).
            log_formatter (logging.Formatter, optional): formatter for the log messages.
                Defaults to None (messages are logged in the format
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s').
        """
        super().__init__(
            tmc_ec,
            tmc_mc,
            tmc_com,
            driver_address,
            gpio_mode,
            loglevel,
            logprefix,
            log_handlers,
            log_formatter,
        )
        StallGuard.__init__(self)

        if self.tmc_com is not None:

            self.gconf: GConf = GConf(self.tmc_com)
            self.gstat: GStat = GStat(self.tmc_com)
            self.ifcnt: IfCnt = IfCnt(self.tmc_com)
            self.ioin: Ioin = Ioin(self.tmc_com)
            self.drv_conf: DrvConf = DrvConf(self.tmc_com)
            self.global_scaler: GlobalScaler = GlobalScaler(self.tmc_com)
            self.ihold_irun: IHoldIRun = IHoldIRun(self.tmc_com)
            self.tpowerdown: TPowerDown = TPowerDown(self.tmc_com)
            self.tstep: TStep = TStep(self.tmc_com)
            self.tpwmthrs: TPwmThrs = TPwmThrs(self.tmc_com)
            self.thigh: THigh = THigh(self.tmc_com)
            self.rampmode: RampMode = RampMode(self.tmc_com)
            self.xactual: XActual = XActual(self.tmc_com)
            self.vactual: VActual = VActual(self.tmc_com)
            self.vstart: VStart = VStart(self.tmc_com)
            self.a1: A1 = A1(self.tmc_com)
            self.v1: V1 = V1(self.tmc_com)
            self.amax: AMax = AMax(self.tmc_com)
            self.vmax: VMax = VMax(self.tmc_com)
            self.dmax: DMax = DMax(self.tmc_com)
            self.d1: D1 = D1(self.tmc_com)
            self.vstop: VStop = VStop(self.tmc_com)
            self.tzerowait: TZeroWait = TZeroWait(self.tmc_com)
            self.xtarget: XTarget = XTarget(self.tmc_com)
            self.vdcmin: VDcMin = VDcMin(self.tmc_com)
            self.swmode: SWMode = SWMode(self.tmc_com)
            self.rampstat: RampStat = RampStat(self.tmc_com)
            self.mscnt: MsCnt = MsCnt(self.tmc_com)
            self.chopconf: ChopConf = ChopConf(self.tmc_com)
            self.coolconf: CoolConf = CoolConf(self.tmc_com)
            self.drvstatus: DrvStatus = DrvStatus(self.tmc_com)
            self.tcoolthrs: TCoolThrs = TCoolThrs(self.tmc_com)
            self.loststeps: LostSteps = LostSteps(self.tmc_com)

        super()._init()

    def deinit(self):
        """destructor"""
        super().deinit()
        StallGuard.deinit(self)

    # Register Access
    # ----------------------------
    def _set_irun_ihold(self, ihold: int, irun: int, iholddelay: int):
        """sets the current scale (CS) for Running and Holding
        and the delay, when to be switched to Holding current

        Args:
        ihold (int): multiplicator for current while standstill [0-31]
        irun (int): current while running [0-31]
        iholddelay (int): delay after standstill for switching to ihold [0-15]

        """
        self.ihold_irun.read()

        self.ihold_irun.ihold = ihold
        self.ihold_irun.irun = irun
        self.ihold_irun.iholddelay = iholddelay

        self.ihold_irun.write_check()

    def _set_global_scaler(self, scaler: int):
        """sets the global scaler

        Args:
            scaler (int): global scaler value
        """
        self.global_scaler.global_scaler = scaler
        self.global_scaler.write_check()

    def set_current_peak(
        self,
        run_current: int,
        hold_current_multiplier: float = 0.5,
        hold_current_delay: int = 10,
    ) -> int:
        """sets the Peak current for the motor.

        Args:
            run_current (int): current during movement in mA
            hold_current_multiplier (int):current multiplier during standstill (Default value = 0.5)
            hold_current_delay (int): delay after standstill after which cur drops (Default value = 10)
            run_current_delay (int): delay after movement start after which cur rises (Default value = 0)
            rref (int): reference resistor in kOhm (Default value = 12)

        Returns:
            int: theoretical final current in mA
        """
        self.tmc_logger.log(f"Desired peak current: {run_current} mA", Loglevel.DEBUG)

        rsense = 0.075  # ohm
        vfs = 0.325  # V

        current_fs = vfs / (rsense) * 1000  # in mA

        self.tmc_logger.log(
            f"current_fs: {current_fs:.0f} mA | {current_fs/1000:.1f} A", Loglevel.DEBUG
        )

        # 256 == 0  -> max current
        global_scaler = round(run_current / current_fs * 256)

        global_scaler = min(global_scaler, 256)
        global_scaler = max(global_scaler, 0)

        self.tmc_logger.log(f"global_scaler: {global_scaler}", Loglevel.DEBUG)
        self._set_global_scaler(global_scaler)

        ct_current_ma = round(current_fs * global_scaler / 256)
        self.tmc_logger.log(
            f"Calculated theoretical peak current after gscaler: {ct_current_ma} mA",
            Loglevel.DEBUG,
        )

        cs_irun = round(run_current / ct_current_ma * 31)

        cs_irun = min(cs_irun, 31)
        cs_irun = max(cs_irun, 0)

        cs_ihold = hold_current_multiplier * cs_irun

        cs_irun = round(cs_irun)
        cs_ihold = round(cs_ihold)
        hold_current_delay = round(hold_current_delay)

        self.tmc_logger.log(f"CS_IRun: {cs_irun}", Loglevel.DEBUG)
        self.tmc_logger.log(f"CS_IHold: {cs_ihold}", Loglevel.DEBUG)
        self.tmc_logger.log(f"IHold_Delay: {hold_current_delay}", Loglevel.DEBUG)

        self._set_irun_ihold(cs_ihold, cs_irun, hold_current_delay)

        ct_current_ma = round(ct_current_ma * cs_irun / 31)
        self.tmc_logger.log(
            f"Calculated theoretical final current: {ct_current_ma} mA", Loglevel.INFO
        )
        return ct_current_ma

    def set_current_rms(
        self,
        run_current: int,
        hold_current_multiplier: float = 0.5,
        hold_current_delay: int = 10,
    ) -> int:
        """sets the RMS current for the motor.

        Args:
            run_current (int): current during movement in mA
            hold_current_multiplier (int):current multiplier during standstill (Default value = 0.5)
            hold_current_delay (int): delay after standstill after which cur drops (Default value = 10)

        Returns:
            int: theoretical final current in mA
        """
        peak_current = self.set_current_peak(
            round(run_current * 1.41421),
            hold_current_multiplier,
            hold_current_delay,
        )
        return round(peak_current / 1.41421)

    def get_spreadcycle(self) -> bool:
        """reads spreadcycle

        Returns:
            bool: True = spreadcycle; False = stealthchop
        """
        self.gconf.read()
        return not self.gconf.en_pwm_mode

    def set_spreadcycle(self, en: bool):
        """enables spreadcycle (1) or stealthchop (0)

        Args:
        en (bool): true to enable spreadcycle; false to enable stealthchop

        """
        self.gconf.modify("en_pwm_mode", not en)

    def set_microstepping_resolution(self, mres: int):
        """sets the current native microstep resolution (1,2,4,8,16,32,64,128,256)

        Args:
            mres (int): µstep resolution; has to be a power of 2 or 1 for fullstep
        """
        if self.tmc_mc is not None:
            self.tmc_mc.mres = mres

        self.chopconf.read()
        self.chopconf.mres_ms = mres
        self.chopconf.write_check()

    def get_interface_transmission_counter(self) -> int:
        """reads the interface transmission counter from the tmc register
        this value is increased on every succesfull write access
        can be used to verify a write access

        Returns:
            int: 8bit IFCNT Register
        """
        self.ifcnt.read()
        ifcnt = self.ifcnt.ifcnt
        self.tmc_logger.log(f"Interface Transmission Counter: {ifcnt}", Loglevel.INFO)
        return ifcnt

    def get_tstep(self) -> int:
        """reads the current tstep from the driver register

        Returns:
            int: TStep time
        """
        self.tstep.read()
        return self.tstep.tstep

    # TMC5160 methods
    # ----------------------------
    def stallguard_setup(
        self,
        threshold: int,
        min_speed: int,
        enable: bool = True,
    ):
        """internal setup for stallguard
        Args:
            threshold (int): value for SGT [0 to 63] 10 worked well for my motor
            min_speed (int): min speed [steps/s] for StallGuard
            enable (bool): enable stallguard (True) or disable (False)
        """
        self.set_spreadcycle(False)

        self._set_coolstep_threshold(
            tmc_math.steps_to_tstep(min_speed, self.get_microstepping_resolution())
        )

        self.coolconf.read()
        self.coolconf.sgt = threshold
        self.coolconf.write_check()

        self.swmode.read()
        self.swmode.sg_stop = enable
        self.swmode.write_check()

        self.gconf.modify("diag0_stall", enable)
        self.gconf.modify("diag0_pushpull", enable)

    def clear_rampstat(self):
        """clears the rampstat register
        use after a stallguard stop to clear the flag
        If the flag is not cleared, further movements are not possible
        """
        time.sleep(0.1)
        self.rampstat.clear()
        time.sleep(0.1)

    def reset_positions(self):
        """resets the position counters to the given value"""
        self.xactual.xactual = 0
        self.xactual.write_check()

        self.xtarget.xtarget = 0
        self.xtarget.write_check()
