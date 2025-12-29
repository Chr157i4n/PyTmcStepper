# pylint: disable=unused-import
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-public-methods
"""Tmc220X stepper driver module

this module has two different functions:
1. change setting in the TMC-driver via UART
2. move the motor via STEP/DIR pins
"""

import time
import types
from .tmc_xxxx import *
from .com._tmc_com import TmcCom
from .com._tmc_com_spi_base import TmcComSpiBase
from .com._tmc_com_uart_base import TmcComUartBase
from .tmc_gpio import GpioPUD
from . import tmc_gpio
from .motion_control._tmc_mc_step_reg import TmcMotionControlStepDir
from .motion_control._tmc_mc_step_reg import TmcMotionControlStepReg
from .motion_control._tmc_mc_step_pwm_dir import TmcMotionControlStepPwmDir
from .enable_control._tmc_ec_toff import TmcEnableControlToff
from .enable_control._tmc_ec_pin import TmcEnableControlPin
from ._tmc_stallguard import StallGuard
from ._tmc_logger import *
from .reg._tmc224x_reg import *
from . import _tmc_math as tmc_math
from ._tmc_exceptions import (
    TmcException,
    TmcComException,
    TmcMotionControlException,
    TmcEnableControlException,
    TmcDriverException,
)
from ._tmc_validation import validate_submodule


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

            self.gconf = GConf(self.tmc_com)
            self.gstat = GStat(self.tmc_com)
            self.ifcnt = IfCnt(self.tmc_com)
            self.ioin = Ioin(self.tmc_com)
            self.drv_conf = DrvConf(self.tmc_com)
            self.global_scaler = GlobalScaler(self.tmc_com)
            self.ihold_irun = IHoldIRun(self.tmc_com)
            self.tpowerdown = TPowerDown(self.tmc_com)
            self.tstep = TStep(self.tmc_com)
            self.thigh = THigh(self.tmc_com)
            self.adcv_supply_ain = ADCVSupplyAIN(self.tmc_com)
            self.adc_temp = ADCTemp(self.tmc_com)
            self.mscnt = MsCnt(self.tmc_com)
            self.chopconf = ChopConf(self.tmc_com)
            self.coolconf = CoolConf(self.tmc_com)
            self.drvstatus = DrvStatus(self.tmc_com)
            self.tcoolthrs = TCoolThrs(self.tmc_com)
            self.sgthrs = SgThrs(self.tmc_com)
            self.sgresult = SgResult(self.tmc_com)
            self.sgind = SgInd(self.tmc_com)

            self.clear_gstat()
            if self.tmc_mc is not None:
                self.read_steps_per_rev()
            self.tmc_com.flush_com_buffer()

    def deinit(self):
        """destructor"""
        super().deinit()
        StallGuard.deinit(self)

    # Tmc224x methods
    # ----------------------------
    def read_steps_per_rev(self) -> int:
        """returns how many steps are needed for one revolution.
        this reads the value from the tmc driver.

        Returns:
            int: Steps per revolution
        """
        self.read_microstepping_resolution()
        return self.tmc_mc.steps_per_rev

    def read_drv_status(self) -> DrvStatus:
        """read the register Adress "DRV_STATUS" and logs the reg valuess

        Returns:
            DRV_STATUS Register instance
        """
        self.drvstatus.read()
        self.drvstatus.log(self.tmc_logger)
        return self.drvstatus

    def read_gconf(self) -> GConf:
        """read the register Adress "GCONF" and logs the reg values

        Returns:
            GCONF Register instance
        """
        self.gconf.read()
        self.gconf.log(self.tmc_logger)
        return self.gconf

    def read_gstat(self) -> GStat:
        """read the register Adress "GSTAT" and logs the reg values

        Returns:
            GSTAT Register instance
        """
        self.gstat.read()
        self.gstat.log(self.tmc_logger)
        return self.gstat

    def read_ioin(self) -> Ioin:
        """read the register Adress "IOIN" and logs the reg values

        Returns:
            IOIN Register instance
        """
        self.ioin.read()
        self.ioin.log(self.tmc_logger)
        return self.ioin

    def read_chopconf(self) -> ChopConf:
        """read the register Adress "CHOPCONF" and logs the reg values

        Returns:
            CHOPCONF Register instance
        """
        self.chopconf.read()
        self.chopconf.log(self.tmc_logger)
        return self.chopconf

    def get_direction_reg(self) -> bool:
        """returns the motor shaft direction: False = CCW; True = CW

        Returns:
            bool: motor shaft direction: False = CCW; True = CW
        """
        self.gconf.read()
        return self.gconf.shaft

    def set_direction_reg(self, direction: bool):
        """sets the motor shaft direction to the given value: False = CCW; True = CW

        Args:
            direction (bool): direction of the motor False = CCW; True = CW
        """
        self.gconf.modify("shaft", direction)

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

    def set_current(
        self,
        run_current: int,
        hold_current_multiplier: float = 0.5,
        hold_current_delay: int = 10,
        run_current_delay: int = 0,
        rref: int = 12,
    ):
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
        self.tmc_logger.log(f"Desired current: {run_current} mA", Loglevel.DEBUG)

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
            f"Calculated theoretical current after gscaler: {ct_current_ma} mA",
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

    def get_interpolation(self) -> bool:
        """return whether the tmc inbuilt interpolation is active

        Returns:
            en (bool): true if internal µstep interpolation is enabled
        """
        self.chopconf.read()
        return self.chopconf.intpol

    def set_interpolation(self, en: bool):
        """enables the tmc inbuilt interpolation of the steps to 256 µsteps

        Args:
            en (bool): true to enable internal µstep interpolation
        """
        self.chopconf.modify("intpol", en)

    def get_toff(self) -> int:
        """returns the TOFF register value

        Returns:
            int: TOFF register value
        """
        self.chopconf.read()
        return self.chopconf.toff

    def set_toff(self, toff: int):
        """Sets TOFF register to value

        Args:
            toff (uint8_t): value of toff (must be a four-bit value)
        """
        self.chopconf.modify("toff", toff)

    def read_microstepping_resolution(self) -> int:
        """returns the current native microstep resolution (1-256)
        this reads the value from the driver register

        Returns:
            int: µstep resolution
        """
        self.chopconf.read()

        mres = self.chopconf.mres_ms
        if self.tmc_mc is not None:
            self.tmc_mc.mres = mres

        return mres

    def get_microstepping_resolution(self) -> int:
        """returns the current native microstep resolution (1-256)
        this returns the cached value from this module

        Returns:
            int: µstep resolution
        """
        return self.tmc_mc.mres

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

    def get_microstep_counter(self) -> int:
        """returns the current Microstep counter.
        Indicates actual position in the microstep table for CUR_A

        Returns:
            int: current Microstep counter
        """
        self.mscnt.read()
        return self.mscnt.mscnt

    def get_microstep_counter_in_steps(self, offset: int = 0) -> int:
        """returns the current Microstep counter.
        Indicates actual position in the microstep table for CUR_A

        Args:
            offset (int): offset in steps (Default value = 0)

        Returns:
            step (int): current Microstep counter convertet to steps
        """
        step = (self.get_microstep_counter() - 64) * (self.tmc_mc.mres * 4) / 1024
        step = (4 * self.tmc_mc.mres) - step - 1
        step = round(step)
        return step + offset

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

    def set_stallguard_callback(
        self, pin_stallguard, threshold, callback, min_speed=100
    ):
        """set a function to call back, when the driver detects a stall
        via stallguard
        high value on the diag pin can also mean a driver error

        Args:
            pin_stallguard (int): pin needs to be connected to DIAG
            threshold (int): value for SGTHRS
            callback (func): will be called on StallGuard trigger
            min_speed (int): min speed [steps/s] for StallGuard (Default value = 100)
        """
        super().set_stallguard_callback(pin_stallguard, threshold, callback, min_speed)
        self.gconf.modify("diag0_stall", 1)
        self.gconf.modify("diag0_pushpull", 1)

    # Test methods
    # ----------------------------
    def test_stallguard_threshold(self, steps):
        """test method for tuning stallguard threshold

        run this function with your motor settings and your motor load
        the function will determine the minimum stallguard results for each movement phase

        Args:
            steps (int):
        """
        if not isinstance(self.tmc_mc, TmcMotionControlStepDir):
            raise TmcMotionControlException(
                "tmc_mc is not of type TmcMotionControlStepDir; cannot test stallguard threshold"
            )

        self.tmc_logger.log("---", Loglevel.INFO)
        self.tmc_logger.log("test_stallguard_threshold", Loglevel.INFO)

        self.set_spreadcycle(False)

        min_stallguard_result_accel = 512
        min_stallguard_result_maxspeed = 512
        min_stallguard_result_decel = 512

        self.tmc_mc.run_to_position_steps_threaded(steps, MovementAbsRel.RELATIVE)

        while self.tmc_mc.movement_phase != MovementPhase.STANDSTILL:
            self.drvstatus.read()
            stallguard_result = self.drvstatus.sgresult
            stallguard_triggered = self.drvstatus.stallguard
            cs_actual = self.drvstatus.cs_actual

            self.tmc_logger.log(
                f"{self.tmc_mc.movement_phase} | {stallguard_result} | {stallguard_triggered} | {cs_actual}",
                Loglevel.INFO,
            )

            if (
                self.tmc_mc.movement_phase == MovementPhase.ACCELERATING
                and stallguard_result < min_stallguard_result_accel
            ):
                min_stallguard_result_accel = stallguard_result
            if (
                self.tmc_mc.movement_phase == MovementPhase.MAXSPEED
                and stallguard_result < min_stallguard_result_maxspeed
            ):
                min_stallguard_result_maxspeed = stallguard_result
            if (
                self.tmc_mc.movement_phase == MovementPhase.DECELERATING
                and stallguard_result < min_stallguard_result_decel
            ):
                min_stallguard_result_decel = stallguard_result

        self.tmc_mc.wait_for_movement_finished_threaded()

        self.tmc_logger.log("---", Loglevel.INFO)
        self.tmc_logger.log(
            f"min StallGuard result during accel: {min_stallguard_result_accel}",
            Loglevel.INFO,
        )
        self.tmc_logger.log(
            f"min StallGuard result during maxspeed: {min_stallguard_result_maxspeed}",
            Loglevel.INFO,
        )
        self.tmc_logger.log(
            f"min StallGuard result during decel: {min_stallguard_result_decel}",
            Loglevel.INFO,
        )
        self.tmc_logger.log("---", Loglevel.INFO)

    def test_dir_step_en(self):
        """tests the EN, DIR and STEP pin

        this sets the EN, DIR and STEP pin to HIGH, LOW and HIGH
        and checks the IOIN Register of the TMC meanwhile
        """
        if self.tmc_mc is None or self.tmc_ec is None:
            raise TmcDriverException("tmc_mc or tmc_ec is None; cannot test pins")
        if not isinstance(self.tmc_mc, TmcMotionControlStepDir) or not isinstance(
            self.tmc_ec, TmcEnableControlPin
        ):
            raise TmcDriverException(
                "tmc_mc or tmc_ec is not of correct type; cannot test pins"
            )

        # test each pin on their own
        pin_dir_ok = self.test_pin(self.tmc_mc.pin_dir, 1)
        pin_step_ok = self.test_pin(self.tmc_mc.pin_step, 0)
        pin_en_ok = self.test_pin(self.tmc_ec.pin_en, 4)

        self.set_motor_enabled(False)

        self.tmc_logger.log("---")
        self.tmc_logger.log(f"Pin DIR: \t{'OK' if pin_dir_ok else 'not OK'}")
        self.tmc_logger.log(f"Pin STEP: \t{'OK' if pin_step_ok else 'not OK'}")
        self.tmc_logger.log(f"Pin EN: \t{'OK' if pin_en_ok else 'not OK'}")
        self.tmc_logger.log("---")
