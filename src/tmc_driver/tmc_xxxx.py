# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
"""
TmcXXXX driver module
"""

import time
from ._tmc_stepperdriver import *
from ._tmc_logger import Loglevel
from .enable_control._tmc_ec import TmcEnableControl
from .motion_control._tmc_mc import TmcMotionControl
from .com._tmc_com import TmcCom
from .reg._tmc_reg import TmcReg
from .reg import _tmc220x_reg as tmc_shared_regs
from ._tmc_validation import validate_submodule
from ._tmc_exceptions import TmcDriverException


class TmcXXXX(TmcStepperDriver):
    """TmcXXXX"""

    SUPPORTED_COM_TYPES = ()
    SUPPORTED_EC_TYPES = ()
    SUPPORTED_MC_TYPES = ()
    DRIVER_FAMILY = "TMCXXXX"

    gstat: tmc_shared_regs.GStat
    ioin: tmc_shared_regs.Ioin

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

            if self.tmc_mc is not None:
                setattr(self.tmc_mc, "tmc_com", self.tmc_com)
            if self.tmc_ec is not None:
                setattr(self.tmc_ec, "tmc_com", self.tmc_com)

            # Register callback for submodules to access registers
            self.tmc_com.set_get_register_callback(self._get_register)
            if self.tmc_mc is not None:
                self.tmc_mc.set_get_register_callback(self._get_register)
            if self.tmc_ec is not None:
                self.tmc_ec.set_get_register_callback(self._get_register)

        self.max_speed_fullstep = 100
        self.acceleration_fullstep = 100

    def __del__(self):
        self.deinit()

    def deinit(self):
        """destructor"""
        super().deinit()
        if self.tmc_com is not None:
            self.tmc_com.deinit()
            self.tmc_com = None

    def _get_register(self, name: str) -> TmcReg | None:
        """Get register by name - callback for submodules

        Args:
            name: Register name (e.g. 'gconf', 'chopconf')

        Returns:
            Register object or None if not found
        """
        return getattr(self, name, None)

    def clear_gstat(self):
        """clears the "GSTAT" register"""
        self.tmc_logger.log("clearing GSTAT", Loglevel.INFO)

        for reg in self.gstat.reg_map:
            setattr(self.gstat, reg.name, True)

        self.gstat.write_check()

    def test_pin(self, pin, ioin_reg_bp):
        """tests one pin

        this function checks the connection to a pin
        by toggling it and reading the IOIN register
        """
        if self.tmc_mc is None or self.tmc_ec is None:
            raise TmcDriverException("tmc_mc or tmc_ec is None; cannot test pins")
        if not isinstance(self.tmc_mc, TmcMotionControlStepDir) or not isinstance(
            self.tmc_ec, TmcEnableControlPin
        ):
            raise TmcDriverException(
                "tmc_mc or tmc_ec is not of correct type; cannot test pins"
            )

        pin_ok = True

        # turn on all pins
        tmc_gpio.tmc_gpio.gpio_output(self.tmc_mc.pin_dir, Gpio.HIGH)
        tmc_gpio.tmc_gpio.gpio_output(self.tmc_mc.pin_step, Gpio.HIGH)
        tmc_gpio.tmc_gpio.gpio_output(self.tmc_ec.pin_en, Gpio.HIGH)

        # check that the selected pin is on
        self.ioin.read()
        if not self.ioin.data_int >> ioin_reg_bp & 0x1:
            pin_ok = False

        # turn off only the selected pin
        tmc_gpio.tmc_gpio.gpio_output(pin, Gpio.LOW)
        time.sleep(0.1)

        # check that the selected pin is off
        self.ioin.read()
        if self.ioin.data_int >> ioin_reg_bp & 0x1:
            pin_ok = False

        return pin_ok

    def test_com(self):
        """test method"""
        if self.tmc_com is None:
            raise TmcDriverException("tmc_com is None; cannot test communication")

        self.tmc_logger.log("---")
        self.tmc_logger.log("TEST COM")

        return self.tmc_com.test_com()
