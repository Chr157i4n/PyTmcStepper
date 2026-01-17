# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# pylint: disable=unused-import
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
# pylint: disable=too-many-public-methods
"""TmcXXXX driver module

this module has two different functions:
1. access register via tmc_com (UART, SPI)
2. Enable motor control via tmc_ec (TOFF, PIN)
3. move the motor via tmc_mc (STEP/DIR, STEP/REG, VACTUAL)
"""

import time
from abc import abstractmethod
from ._tmc_stepperdriver import *
from .tmc_logger import Loglevel
from .enable_control._tmc_ec import TmcEnableControl
from .motion_control._tmc_mc import TmcMotionControl
from .com._tmc_com import TmcCom
from .reg._tmc_reg import TmcReg
from .reg import _tmc_shared_regs as tmc_shared_regs
from ._tmc_validation import validate_submodule
from ._tmc_exceptions import (
    TmcException,
    TmcComException,
    TmcMotionControlException,
    TmcEnableControlException,
    TmcDriverException,
)


class TmcXXXX(TmcStepperDriver):
    """TmcXXXX"""

    SUPPORTED_COM_TYPES = ()
    SUPPORTED_EC_TYPES = ()
    SUPPORTED_MC_TYPES = ()
    DRIVER_FAMILY = "TMCXXXX"

    gstat: tmc_shared_regs.GStat
    ioin: tmc_shared_regs.Ioin
    gconf: tmc_shared_regs.GConf
    chopconf: tmc_shared_regs.ChopConf
    mscnt: tmc_shared_regs.MsCnt
    tpwmthrs: tmc_shared_regs.TPwmThrs

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
        self.tmc_com = tmc_com

        if logprefix is None:
            logprefix = f"{self.DRIVER_FAMILY} {driver_address}"

        super().__init__(
            tmc_ec, tmc_mc, gpio_mode, loglevel, logprefix, log_handlers, log_formatter
        )

        validate_submodule(
            tmc_com, self.SUPPORTED_COM_TYPES, self.__class__.__name__, "tmc_com"
        )
        validate_submodule(
            tmc_ec, self.SUPPORTED_EC_TYPES, self.__class__.__name__, "tmc_ec"
        )
        validate_submodule(
            tmc_mc, self.SUPPORTED_MC_TYPES, self.__class__.__name__, "tmc_mc"
        )

        if self.tmc_com is not None:
            self.tmc_com.tmc_logger = self.tmc_logger
            self.tmc_com.driver_address = driver_address
            self.tmc_com.init()

            # Register callback for submodules to access registers
            self.tmc_com.set_get_register_callback(self._get_register)
            if self.tmc_mc is not None:
                self.tmc_mc.set_get_register_callback(self._get_register)
            if self.tmc_ec is not None:
                self.tmc_ec.set_get_register_callback(self._get_register)

        if hasattr(self, "tmc_mc") and self.tmc_mc is not None:
            self.max_speed_fullstep = 100
            self.acceleration_fullstep = 100

    def _init(self):
        """initialization after registers are created"""
        if self.tmc_com is not None:
            self.clear_gstat_verify()
            if self.tmc_mc is not None:
                self.read_steps_per_rev()
            self.tmc_com.flush_com_buffer()

    def __del__(self):
        self.deinit()

    def deinit(self):
        """destructor"""
        super().deinit()
        if self.tmc_com is not None:
            self.tmc_com.deinit()
            self.tmc_com = None

    # Register Access
    # ----------------------------
    def clear_gstat_verify(self):
        """clears the GSTAT register and verifies that it was cleared"""
        tries = 5
        while True:
            try:
                self.gstat.clear_verify()
                break
            except TmcDriverException:
                time.sleep(0.1)
            tries -= 1
            if tries <= 0:
                raise TmcDriverException("Could not clear GSTAT register")

    def read_steps_per_rev(self) -> int:
        """returns how many steps are needed for one revolution.
        this reads the value from the tmc driver.

        Returns:
            int: Steps per revolution
        """
        if self.tmc_mc is None:
            raise TmcDriverException("tmc_mc is None; cannot read steps per revolution")
        self.read_microstepping_resolution()
        return self.tmc_mc.steps_per_rev

    def _get_register(self, name: str) -> TmcReg:
        """Get register by name - callback for submodules

        Args:
            name: Register name (e.g. 'gconf', 'chopconf')

        Returns:
            Register object or None if not found
        """
        name = name.lower()
        reg = getattr(self, name, None)
        if reg is None:
            raise TmcDriverException(
                f"Register {name} not found in driver {self.DRIVER_FAMILY}"
            )
        return reg

    @abstractmethod
    def get_spreadcycle(self) -> bool:
        """reads spreadcycle

        Returns:
            bool: True = spreadcycle; False = stealthchop
        """

    @abstractmethod
    def set_spreadcycle(self, en: bool):
        """enables spreadcycle (1) or stealthchop (0)

        Args:
        en (bool): true to enable spreadcycle; false to enable stealthchop

        """

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
        this returns the cached value from the tmc_mc module

        Returns:
            int: µstep resolution
        """
        if self.tmc_mc is None:
            raise TmcDriverException(
                "tmc_mc is None; cannot get microstepping resolution"
            )
        return self.tmc_mc.mres

    @abstractmethod
    def set_microstepping_resolution(self, mres: int):
        """sets the current native microstep resolution (1,2,4,8,16,32,64,128,256)

        Args:
            mres (int): µstep resolution; has to be a power of 2 or 1 for fullstep
        """

    @abstractmethod
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
        Returns:
            int: theoretical final current in mA
        """

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
            round(run_current * 1.41421), hold_current_multiplier, hold_current_delay
        )
        return round(peak_current / 1.41421)

    def set_current(
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

        Returns:
            int: theoretical final current in mA
        """
        return self.set_current_rms(
            run_current, hold_current_multiplier, hold_current_delay
        )

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
        if self.tmc_mc is None:
            raise TmcDriverException(
                "tmc_mc is None; cannot get microstep counter in steps"
            )
        step = (self.get_microstep_counter() - 64) * (self.tmc_mc.mres * 4) / 1024
        step = (4 * self.tmc_mc.mres) - step - 1
        step = round(step)
        return step + offset

    def read_register(
        self, name: str, log: bool = True
    ) -> tuple[TmcReg, int, dict | None]:
        """reads all relevant registers of the driver"""
        if self.tmc_com is None:
            raise TmcComException("tmc_com is None; cannot read registers")

        reg = self._get_register(name)
        if reg is None:
            raise TmcDriverException(f"Register {name} not found in driver")
        data, flags = reg.read()

        if log:
            reg.log(self.tmc_logger)

        return reg, data, flags

    def set_hybrid_threshold_speed(self, speed: int):
        """sets the hybrid threshold speed

        Args:
            speed (int): speed in steps per second
        """
        tstep = tmc_math.steps_to_tstep(speed, self.get_microstepping_resolution())
        self.tpwmthrs.modify("tpwmthrs", tstep)

    # Test Methods
    # ----------------------------
    def test_pin(self, pin, ioin_reg_field_name: str) -> bool:
        """tests one pin

        this function checks the connection to a pin
        by toggling it and reading the IOIN register

        Args:
            pin: pin to be tested
            ioin_reg_field_name (str): name of the IOIN register field
                that corresponds to the pin

        Returns:
            bool: True = pin OK; False = pin not OK
        """
        if self.tmc_mc is None or self.tmc_ec is None:
            raise TmcDriverException("tmc_mc or tmc_ec is None; cannot test pins")
        if not isinstance(self.tmc_mc, TmcMotionControlStepDir) or not isinstance(
            self.tmc_ec, TmcEnableControlPin
        ):
            raise TmcDriverException(
                "tmc_mc or tmc_ec is not of correct type; cannot test pins"
            )
        if self.tmc_ec.pin_en is None:
            raise TmcDriverException("tmc_ec pin_en is None; cannot test pins")
        if self.tmc_mc.pin_dir is None:
            raise TmcDriverException("tmc_mc pin_dir is None; cannot test pins")
        if self.tmc_mc.pin_step is None:
            raise TmcDriverException("tmc_mc pin_step is None; cannot test pins")

        pin_ok = True

        # turn on all pins
        tmc_gpio.tmc_gpio.gpio_output(self.tmc_mc.pin_dir, Gpio.HIGH)
        tmc_gpio.tmc_gpio.gpio_output(self.tmc_mc.pin_step, Gpio.HIGH)
        tmc_gpio.tmc_gpio.gpio_output(self.tmc_ec.pin_en, Gpio.HIGH)

        # check that the selected pin is on
        if not self.ioin.get(ioin_reg_field_name):
            pin_ok = False

        # turn off only the selected pin
        tmc_gpio.tmc_gpio.gpio_output(pin, Gpio.LOW)
        time.sleep(0.1)

        # check that the selected pin is off
        if self.ioin.get(ioin_reg_field_name):
            pin_ok = False
            pin_ok = False

        return pin_ok

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
        pin_dir_ok = self.test_pin(self.tmc_mc.pin_dir, "dir")
        pin_step_ok = self.test_pin(self.tmc_mc.pin_step, "step")
        pin_en_ok = self.test_pin(self.tmc_ec.pin_en, "enn")

        self.set_motor_enabled(False)

        self.tmc_logger.log("---")
        self.tmc_logger.log(f"Pin DIR: \t{'OK' if pin_dir_ok else 'not OK'}")
        self.tmc_logger.log(f"Pin STEP: \t{'OK' if pin_step_ok else 'not OK'}")
        self.tmc_logger.log(f"Pin EN: \t{'OK' if pin_en_ok else 'not OK'}")
        self.tmc_logger.log("---")

    def test_com(self):
        """test method"""
        if self.tmc_com is None:
            raise TmcDriverException("tmc_com is None; cannot test communication")

        self.tmc_logger.log("---")
        self.tmc_logger.log("TEST COM")

        return self.tmc_com.test_com(self.ioin)
