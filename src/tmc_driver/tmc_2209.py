# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
"""Tmc2209 stepper driver module"""

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

        if tmc_com is not None:
            self.tcoolthrs = TCoolThrs(self.tmc_com)
            self.sgthrs = SGThrs(self.tmc_com)
            self.sgresult = SGResult(self.tmc_com)

    def deinit(self):
        """destructor"""
        super().deinit()
        StallGuard.deinit(self)

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
            stallguard_result = self.get_stallguard_result()
            self.drvstatus.read()
            cs_actual = self.drvstatus.cs_actual

            self.tmc_logger.log(
                f"{self.tmc_mc.movement_phase} | {stallguard_result} | {cs_actual}",
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
