# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments
# pylint: disable=too-many-public-methods
# pylint: disable=too-many-branches
# pylint: disable=too-many-positional-arguments
"""
TMC internal Ramp Generator Motion Control module
"""

import sys
import time
from ._tmc_mc import TmcMotionControl, MovementAbsRel, StopMode
from ..com._tmc_com import TmcCom
from .._tmc_logger import Loglevel

# from .. import _tmc_math as tmc_math


# MicroPython compatibility for time functions
MICROPYTHON = sys.implementation.name == "micropython"


def _get_time_ms():
    """Get current time in milliseconds, compatible with both CPython and MicroPython"""
    if MICROPYTHON:
        return time.ticks_ms()  # pylint: disable=no-member
    return time.time_ns() // 1_000_000


class TmcMotionControlIntRampGenerator(TmcMotionControl):
    """TMC internal Ramp Generator Motion Control class"""

    @property
    def tmc_com(self):
        """get the tmc_logger"""
        return self._tmc_com

    @tmc_com.setter
    def tmc_com(self, tmc_com):
        """set the tmc_logger"""
        self._tmc_com = tmc_com

    def __init__(self):
        """constructor"""
        super().__init__()
        self._tmc_com: TmcCom | None = None
        self._starttime: int = 0

    def make_a_step(self):
        """method that makes on step"""
        raise NotImplementedError

    def stop(self, stop_mode=StopMode.HARDSTOP):
        """stop the current movement

        Args:
            stop_mode (enum): whether the movement should be stopped immediately or softly
                (Default value = StopMode.HARDSTOP)
        """
        super().stop(stop_mode)

    def run_to_position_steps(
        self, steps, movement_abs_rel: MovementAbsRel | None = None
    ) -> StopMode:
        """runs the motor to the given position.
        with acceleration and deceleration
        blocks the code until finished or stopped from a different thread!
        returns true when the movement if finished normally and false,
        when the movement was stopped

        Args:
            steps (int): amount of steps; can be negative
            movement_abs_rel (enum): whether the movement should be absolut or relative
                (Default value = None)

        Returns:
            stop (enum): how the movement was finished
        """
        gconf = self.get_register("gconf")
        gconf.read()
        gconf.en_pwm_mode = 1
        gconf.write()

        xactual = self.get_register("xactual")
        xactual.read()
        self._current_pos = xactual.xactual
        xactual.write()

        rampmode = self.get_register("rampmode")
        rampmode.rampmode = 0  # Positioning mode
        rampmode.write()

        vstart = self.get_register("vstart")
        vstart.vstart = 5
        vstart.write()

        vstop = self.get_register("vstop")
        vstop.vstop = 10
        vstop.write()

        a1 = self.get_register("a1")
        a1.a1 = self._acceleration
        a1.write()

        v1 = self.get_register("v1")
        v1.v1 = self._max_speed
        v1.write()

        vmax = self.get_register("vmax")
        vmax.vmax = self._max_speed
        vmax.write()

        amax = self.get_register("amax")
        amax.amax = self._acceleration
        amax.write()

        d1 = self.get_register("d1")
        d1.d1 = self._acceleration
        d1.write()

        dmax = self.get_register("dmax")
        dmax.dmax = self._acceleration
        dmax.write()

        if movement_abs_rel == MovementAbsRel.ABSOLUTE or (
            movement_abs_rel is None
            and self._movement_abs_rel == MovementAbsRel.ABSOLUTE
        ):
            self._target_pos = steps
        else:
            self._target_pos = self._current_pos + steps

        self._tmc_logger.log(
            f"cur: {self._current_pos} | tar: {self._target_pos}", Loglevel.MOVEMENT
        )

        xtarget = self.get_register("xtarget")
        xtarget.xtarget = self._target_pos
        xtarget.write()
