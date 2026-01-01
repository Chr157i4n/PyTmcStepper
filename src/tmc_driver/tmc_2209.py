# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
"""Tmc2209 stepper driver module

this module has two different functions:
1. access register via tmc_com (UART, SPI)
2. Enable motor control via tmc_ec (TOFF, PIN)
3. move the motor via tmc_mc (STEP/DIR, STEP/REG, VACTUAL)
"""

from .tmc_220x import *
from ._tmc_stallguard import StallGuard
from .reg._tmc2209_reg import *


class Tmc2209(Tmc220x, StallGuard):
    """Tmc2209"""

    DRIVER_FAMILY = "TMC2209"

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
            self.tcoolthrs: TCoolThrs = TCoolThrs(self.tmc_com)
            self.sgthrs: SgThrs = SgThrs(self.tmc_com)
            self.sgresult: SgResult = SgResult(self.tmc_com)

    def deinit(self):
        """destructor"""
        super().deinit()
        StallGuard.deinit(self)
