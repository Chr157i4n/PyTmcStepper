# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-public-methods
"""Tmc220X stepper driver module

this module has two different functions:
1. access register via tmc_com (UART, SPI)
2. Enable motor control via tmc_ec (TOFF, PIN)
3. move the motor via tmc_mc (STEP/DIR, STEP/REG, VACTUAL)
"""

from ._tmc_xxxx import *
from .com._tmc_com import TmcCom
from .com._tmc_com_spi_base import TmcComSpiBase
from .com._tmc_com_uart_base import TmcComUartBase
from .motion_control._tmc_mc_step_reg import TmcMotionControlStepDir
from .motion_control._tmc_mc_step_reg import TmcMotionControlStepReg
from .motion_control._tmc_mc_step_pwm_dir import TmcMotionControlStepPwmDir
from .enable_control._tmc_ec_toff import TmcEnableControlToff
from .enable_control._tmc_ec_pin import TmcEnableControlPin
from ._tmc_stallguard import StallGuard
from .tmc_logger import *
from .reg._tmc224x_reg import *


class Tmc2240(TmcXXXX, StallGuard):
    """Tmc2240"""

    SUPPORTED_COM_TYPES = (TmcComSpiBase, TmcComUartBase)
    SUPPORTED_EC_TYPES = (TmcEnableControlToff, TmcEnableControlPin)
    SUPPORTED_MC_TYPES = (
        TmcMotionControlStepDir,
        TmcMotionControlStepReg,
        TmcMotionControlStepPwmDir,
    )
    DRIVER_FAMILY = "TMC2240"

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
            self.adcv_supply_ain: ADCVSupplyAIN = ADCVSupplyAIN(self.tmc_com)
            self.adc_temp: ADCTemp = ADCTemp(self.tmc_com)
            self.mscnt: MsCnt = MsCnt(self.tmc_com)
            self.chopconf: ChopConf = ChopConf(self.tmc_com)
            self.coolconf: CoolConf = CoolConf(self.tmc_com)
            self.drvstatus: DrvStatus = DrvStatus(self.tmc_com)
            self.tcoolthrs: TCoolThrs = TCoolThrs(self.tmc_com)
            self.sgthrs: SgThrs = SgThrs(self.tmc_com)
            self.sgresult: SgResult = SgResult(self.tmc_com)
            self.sgind: SgInd = SgInd(self.tmc_com)

        super()._init()

    def deinit(self):
        """destructor"""
        super().deinit()
        StallGuard.deinit(self)

    # Register Access
    # ----------------------------
    def _set_irun_ihold(self, ihold: int, irun: int, iholddelay: int, irundelay: int):
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
        self.ihold_irun.irundelay = irundelay

        self.ihold_irun.write_check()

    def _set_global_scaler(self, scaler: int):
        """sets the global scaler

        Args:
            scaler (int): global scaler value
        """
        self.global_scaler.global_scaler = scaler
        self.global_scaler.write_check()

    def _set_current_range(self, current_range: int):
        """sets the current range

        0 = 1 A
        1 = 2 A
        2 = 3 A
        3 = 3 A (maximum of driver)

        Args:
            current_range (int): current range in A
        """
        self.drv_conf.current_range = current_range
        self.drv_conf.modify("current_range", current_range)

    def set_current_peak(
        self,
        run_current: int,
        hold_current_multiplier: float = 0.5,
        hold_current_delay: int = 10,
        run_current_delay: int = 0,
        rref: int = 12,
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

        K_IFS_TABLE = [11.75, 24, 36, 36]  # A*kOhm
        current_fs_table = [k_ifs / rref * 1000 for k_ifs in K_IFS_TABLE]

        current_range_reg_value = 3
        for i, current_fs in enumerate(current_fs_table):
            if run_current < current_fs:
                current_range_reg_value = i
                break

        current_fs = current_fs_table[current_range_reg_value]

        self.tmc_logger.log(
            f"current_fs: {current_fs:.0f} mA | {current_fs/1000:.1f} A", Loglevel.DEBUG
        )
        self._set_current_range(current_range_reg_value)

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
        run_current_delay = round(run_current_delay)

        self.tmc_logger.log(f"CS_IRun: {cs_irun}", Loglevel.DEBUG)
        self.tmc_logger.log(f"CS_IHold: {cs_ihold}", Loglevel.DEBUG)
        self.tmc_logger.log(f"IHold_Delay: {hold_current_delay}", Loglevel.DEBUG)
        self.tmc_logger.log(f"IRun_Delay: {run_current_delay}", Loglevel.DEBUG)

        self._set_irun_ihold(cs_ihold, cs_irun, hold_current_delay, run_current_delay)

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
        run_current_delay: int = 0,
        rref: int = 12,
    ) -> int:
        """sets the RMS current for the motor.

        Args:
            run_current (int): current during movement in mA
            hold_current_multiplier (int):current multiplier during standstill (Default value = 0.5)
            hold_current_delay (int): delay after standstill after which cur drops (Default value = 10)
            run_current_delay (int): delay after movement start after which cur rises (Default value = 0)
            rref (int): reference resistor in kOhm (Default value = 12)

        Returns:
            int: theoretical final current in mA
        """
        peak_current = self.set_current_peak(
            round(run_current * 1.41421),
            hold_current_multiplier,
            hold_current_delay,
            run_current_delay,
            rref,
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

    def get_vsupply(self) -> float:
        """reads the ADC_VSUPPLY_AIN register

        Returns:
            int: ADC_VSUPPLY_AIN register value
        """
        self.adcv_supply_ain.read()
        return self.adcv_supply_ain.adc_vsupply_v

    def get_temperature(self) -> float:
        """reads the ADC_TEMP register and returns the temperature

        Returns:
            float: temperature in °C
        """
        self.adc_temp.read()
        return self.adc_temp.adc_temp_c

    # TMC224x methods
    # ----------------------------
    def stallguard_setup(
        self,
        threshold: int,
        min_speed: int,
        enable: bool = True,
    ):
        """internal setup for stallguard
        Args:
            threshold (int): value for SGTHRS
            min_speed (int): min speed [steps/s] for StallGuard
        """
        super().stallguard_setup(threshold, min_speed)
        self.gconf.modify("diag0_stall", enable)
        self.gconf.modify("diag0_pushpull", enable)
