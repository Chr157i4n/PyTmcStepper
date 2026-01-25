# pylint: disable=import-outside-toplevel
"""Motion control module for TMC stepper drivers

Provides various motion control strategies:
- TmcMotionControlStepDir: STEP/DIR pin-based control
- TmcMotionControlStepReg: STEP/DIR with register-based direction
- TmcMotionControlStepPwmDir: STEP/DIR with PWM for step pin
- TmcMotionControlVActual: Velocity control via VACTUAL register
- TmcMotionControlIntRampGenerator: Internal ramp generator (TMC5160)

Enums:
- Direction: Motor rotation direction (CW/CCW)
- MovementAbsRel: Absolute or relative positioning
- MovementPhase: Current movement phase
- StopMode: How to stop motor movement

Example:
    >>> from tmc_driver.motion_control import TmcMotionControlStepDir, Direction
    >>> mc = TmcMotionControlStepDir(step_pin=16, dir_pin=20)
    >>> mc.set_direction_pin(Direction.CW)

Note: Uses lazy imports to avoid circular import issues.
"""

try:
    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        # Import for type checkers/IDE only - not executed at runtime
        from ._tmc_mc import (
            TmcMotionControl,
            Direction,
            MovementAbsRel,
            MovementPhase,
            StopMode,
        )
        from ._tmc_mc_step_dir import TmcMotionControlStepDir
        from ._tmc_mc_step_reg import TmcMotionControlStepReg
        from ._tmc_mc_step_pwm_dir import TmcMotionControlStepPwmDir
        from ._tmc_mc_step_pio import TmcMotionControlStepPio
        from ._tmc_mc_vactual import TmcMotionControlVActual
        from ._tmc_mc_int_ramp_generator import (
            TmcMotionControlIntRampGenerator,
            RampMode,
        )
except ImportError:
    pass


def __getattr__(name):
    # pylint: disable=too-many-return-statements
    """Lazy import of motion control classes to avoid circular imports"""
    if name == "TmcMotionControl":
        from ._tmc_mc import TmcMotionControl

        return TmcMotionControl
    if name == "Direction":
        from ._tmc_mc import Direction

        return Direction
    if name == "MovementAbsRel":
        from ._tmc_mc import MovementAbsRel

        return MovementAbsRel
    if name == "MovementPhase":
        from ._tmc_mc import MovementPhase

        return MovementPhase
    if name == "StopMode":
        from ._tmc_mc import StopMode

        return StopMode
    if name == "TmcMotionControlStepDir":
        from ._tmc_mc_step_dir import TmcMotionControlStepDir

        return TmcMotionControlStepDir
    if name == "TmcMotionControlStepReg":
        from ._tmc_mc_step_reg import TmcMotionControlStepReg

        return TmcMotionControlStepReg
    if name == "TmcMotionControlStepPwmDir":
        from ._tmc_mc_step_pwm_dir import TmcMotionControlStepPwmDir

        return TmcMotionControlStepPwmDir
    if name == "TmcMotionControlStepPio":
        from ._tmc_mc_step_pio import TmcMotionControlStepPio

        return TmcMotionControlStepPio
    if name == "TmcMotionControlVActual":
        from ._tmc_mc_vactual import TmcMotionControlVActual

        return TmcMotionControlVActual
    if name == "TmcMotionControlIntRampGenerator":
        from ._tmc_mc_int_ramp_generator import TmcMotionControlIntRampGenerator

        return TmcMotionControlIntRampGenerator
    if name == "RampMode":
        from ._tmc_mc_int_ramp_generator import RampMode

        return RampMode
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "TmcMotionControl",
    "Direction",
    "MovementAbsRel",
    "MovementPhase",
    "StopMode",
    "RampMode",
    "TmcMotionControlStepDir",
    "TmcMotionControlStepReg",
    "TmcMotionControlStepPwmDir",
    "TmcMotionControlStepPio",
    "TmcMotionControlVActual",
    "TmcMotionControlIntRampGenerator",
]
