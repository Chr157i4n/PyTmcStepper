# pylint: disable=too-many-arguments
# pylint: disable=too-many-public-methods
# pylint: disable=too-many-branches
# pylint: disable=too-many-positional-arguments
# pylint: disable=import-outside-toplevel
# pylint: disable=bare-except
# pylint: disable=unused-import
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
"""TmcStepperDriver module

this module has the function to move the motor via STEP/DIR pins
"""

try:
    from typing import TYPE_CHECKING
except ImportError:
    TYPE_CHECKING = False
from .tmc_gpio import Board
from . import tmc_gpio
from .motion_control._tmc_mc import (
    TmcMotionControl,
    MovementAbsRel,
    MovementPhase,
    StopMode,
    Direction,
)
from .enable_control._tmc_ec import TmcEnableControl
from .enable_control._tmc_ec_pin import TmcEnableControlPin
from .motion_control._tmc_mc_step_dir import TmcMotionControlStepDir
from .motion_control._tmc_mc_step_pwm_dir import TmcMotionControlStepPwmDir
from .tmc_logger import *
from . import _tmc_math as tmc_math


class TmcStepperDriver:
    """TmcStepperDriver

    this class has two different functions:
    1. change setting in the TMC-driver via UART
    2. move the motor via STEP/DIR pins

    Attributes forwarded to tmc_mc (motion control):
        current_pos, current_pos_fullstep, mres, steps_per_rev, fullsteps_per_rev,
        movement_abs_rel, movement_phase, speed, max_speed, max_speed_fullstep,
        acceleration, acceleration_fullstep
    """

    # Attributes that are automatically forwarded to tmc_mc submodule
    _MC_FORWARDED_ATTRS = {
        "current_pos",
        "current_pos_fullstep",
        "mres",
        "steps_per_rev",
        "fullsteps_per_rev",
        "movement_abs_rel",
        "movement_phase",
        "speed",
        "max_speed",
        "max_speed_fullstep",
        "acceleration",
        "acceleration_fullstep",
    }

    if TYPE_CHECKING:
        # Type hints for IDE/type checkers - these attributes are forwarded via __getattr__
        current_pos: int
        current_pos_fullstep: int
        mres: int
        steps_per_rev: int
        fullsteps_per_rev: int
        movement_abs_rel: MovementAbsRel
        movement_phase: MovementPhase
        speed: float
        max_speed: int
        max_speed_fullstep: int
        acceleration: int
        acceleration_fullstep: int

    # Constructor/Destructor
    # ----------------------------
    def __init__(
        self,
        tmc_ec: TmcEnableControl,
        tmc_mc: TmcMotionControl,
        gpio_mode=None,
        loglevel: Loglevel = Loglevel.INFO,
        logprefix: str | None = None,
        log_handlers: list | None = None,
        log_formatter: logging.Formatter | None = None,
    ):
        """constructor

        Args:
            pin_en (int): EN pin number
            pin_step (int, optional): STEP pin number. Defaults to -1.
            pin_dir (int, optional): DIR pin number. Defaults to -1.
            tmc_com (TmcUart, optional): TMC UART object. Defaults to None.
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
        self.BOARD: Board = tmc_gpio.BOARD
        self.tmc_ec = tmc_ec
        self.tmc_mc = tmc_mc
        self.tmc_logger: TmcLogger

        if logprefix is None:
            logprefix = "StepperDriver"
        self.tmc_logger = TmcLogger(loglevel, logprefix, log_handlers, log_formatter)

        self.tmc_logger.log("Init", Loglevel.INFO)

        tmc_gpio.tmc_gpio.init(gpio_mode)

        if self.tmc_mc is not None:
            self.tmc_mc.init(self.tmc_logger)

        if self.tmc_ec is not None:
            self.tmc_ec.init(self.tmc_logger)

    def __del__(self):
        self.deinit()

    def deinit(self):
        """destructor"""
        if hasattr(self, "tmc_ec") and self.tmc_ec is not None:
            self.tmc_ec.deinit()
            self.tmc_ec = None
        if hasattr(self, "tmc_mc") and self.tmc_mc is not None:
            self.tmc_mc.deinit()
            self.tmc_mc = None
        if hasattr(self, "tmc_logger") and self.tmc_logger is not None:
            self.tmc_logger.deinit()
            del self.tmc_logger

    # Attribute Forwarding
    # ----------------------------
    def __getattr__(self, name):
        """Forward attribute access to tmc_mc submodule dynamically"""
        if name in self._MC_FORWARDED_ATTRS:
            if not hasattr(self, "tmc_mc") or self.tmc_mc is None:
                raise AttributeError(
                    f"Cannot access '{name}': TmcMotionControl is not set"
                )
            return getattr(self.tmc_mc, name)

        raise AttributeError(
            f"'{type(self).__name__}' object has no attribute '{name}'"
        )

    def __setattr__(self, name, value):
        """Forward attribute setting to tmc_mc submodule dynamically"""
        # Forward to tmc_mc if it's a forwarded attribute and tmc_mc exists
        if name in self._MC_FORWARDED_ATTRS:
            # Only forward if tmc_mc is already initialized (not during __init__)
            if hasattr(self, "tmc_mc") and self.tmc_mc is not None:
                setattr(self.tmc_mc, name, value)
                return
            # During __init__, tmc_mc doesn't exist yet, so fall through

        # Normal attribute assignment (self.tmc_mc, self.tmc_ec, etc.)
        super().__setattr__(name, value)

    # TmcEnableControl Wrapper
    # ----------------------------
    def set_motor_enabled(self, en: bool):
        """enable control wrapper"""
        if self.tmc_ec is not None:
            self.tmc_ec.set_motor_enabled(en)

    # TmcMotionControl Wrapper
    # ----------------------------
    def run_to_position_steps(
        self, steps, movement_abs_rel: MovementAbsRel | None = None
    ) -> StopMode:
        """motioncontrol wrapper"""
        if not hasattr(self, "tmc_mc") or self.tmc_mc is None:
            raise AttributeError("TmcMotionControl is not set")
        return self.tmc_mc.run_to_position_steps(steps, movement_abs_rel)

    def run_to_position_fullsteps(
        self, steps, movement_abs_rel: MovementAbsRel | None = None
    ) -> StopMode:
        """motioncontrol wrapper"""
        return self.run_to_position_steps(steps * self.mres, movement_abs_rel)

    def run_to_position_revolutions(
        self, revs, movement_abs_rel: MovementAbsRel | None = None
    ) -> StopMode:
        """motioncontrol wrapper"""
        return self.run_to_position_steps(revs * self.steps_per_rev, movement_abs_rel)

    def reset_position(self):
        """resets the current position to 0"""
        self.current_pos_fullstep = 0

    # Test Methods
    # ----------------------------
    def test_step(self):
        """test method"""
        if not hasattr(self, "tmc_mc") or self.tmc_mc is None:
            raise AttributeError("TmcMotionControl is not set")
        for _ in range(100):
            self.tmc_mc.set_direction(Direction.CW)
            self.tmc_mc.make_a_step()
