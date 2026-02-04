"""PyTmcStepper - Python library for Trinamic TMC stepper motor drivers.

This package provides a high-level interface for controlling TMC stepper motor drivers
via UART or SPI communication on various platforms including Raspberry Pi, Jetson, and MicroPython.

Main Components:
    - Driver Classes: Tmc2208, Tmc2209, Tmc2240, Tmc5160
    - Communication: TmcCom and subclasses for UART/SPI
    - Motion Control: Various strategies for motor movement
    - Enable Control: Motor enable/disable functionality
    - GPIO Abstraction: Platform-independent GPIO access
    - Logging: Configurable logging support

Example:
    >>> from tmc_driver import Tmc2209, Loglevel
    >>> from tmc_driver.com import TmcComUart
    >>> from tmc_driver.motion_control import TmcMotionControlStepDir
    >>> from tmc_driver.enable_control import TmcEnableControlPin
    >>>
    >>> tmc = Tmc2209(
    ...     TmcEnableControlPin(21),
    ...     TmcMotionControlStepDir(16, 20),
    ...     TmcComUart("/dev/serial0"),
    ...     loglevel=Loglevel.INFO
    ... )
"""

# Driver classes
from .tmc_2208 import Tmc2208
from .tmc_2209 import Tmc2209
from .tmc_2240 import Tmc2240
from .tmc_5160 import Tmc5160

# Exceptions
from ._tmc_exceptions import (
    TmcException,
    TmcDriverException,
    TmcComException,
    TmcMotionControlException,
    TmcEnableControlException,
)

# Logger
from .tmc_logger import TmcLogger, Loglevel

# GPIO
from . import tmc_gpio
from .tmc_gpio import Board

# Enable Control
from .enable_control._tmc_ec_pin import TmcEnableControlPin
from .enable_control._tmc_ec_toff import TmcEnableControlToff

# Motion Control
from .motion_control._tmc_mc import StopMode, MovementAbsRel, MovementPhase, Direction
from .motion_control._tmc_mc_step_dir import TmcMotionControlStepDir
from .motion_control._tmc_mc_step_pwm_dir import TmcMotionControlStepPwmDir
from .motion_control._tmc_mc_step_reg import TmcMotionControlStepReg
from .motion_control._tmc_mc_vactual import TmcMotionControlVActual
from .motion_control._tmc_mc_int_ramp_generator import TmcMotionControlIntRampGenerator

__all__ = [
    # Driver classes
    "Tmc2208",
    "Tmc2209",
    "Tmc2240",
    "Tmc5160",
    # Exceptions
    "TmcException",
    "TmcDriverException",
    "TmcComException",
    "TmcMotionControlException",
    "TmcEnableControlException",
    # Logger
    "TmcLogger",
    "Loglevel",
    # GPIO
    "tmc_gpio",
    "Board",
    # Enable Control
    "TmcEnableControlPin",
    "TmcEnableControlToff",
    # Motion Control
    "StopMode",
    "MovementAbsRel",
    "MovementPhase",
    "Direction",
    "TmcMotionControlStepDir",
    "TmcMotionControlStepPwmDir",
    "TmcMotionControlStepReg",
    "TmcMotionControlVActual",
    "TmcMotionControlIntRampGenerator",
]
