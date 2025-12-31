# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments
# pylint: disable=too-many-public-methods
# pylint: disable=too-many-branches
# pylint: disable=too-many-positional-arguments
"""
TMC internal Ramp Generator Motion Control module
"""

import time
from enum import IntEnum
from ._tmc_mc import TmcMotionControl, MovementAbsRel, StopMode
from ..com._tmc_com import TmcCom
from .._tmc_logger import Loglevel

# from .. import _tmc_math as tmc_math


class RampMode(IntEnum):
    """Ramp modes of the TMC internal ramp generator"""

    POSITIONING_MODE = 0
    VELOCITY_MODE_POS = 1
    VELOCITY_MODE_NEG = 1
    HOLD_MODE = 2


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

    def set_ramp_mode(self, ramp_mode: RampMode):
        """sets the ramp mode of the internal ramp generator

        Args:
            ramp_mode (enum): the ramp mode to set
        """
        rampmode = self.get_register("rampmode")
        rampmode.rampmode = int(ramp_mode)
        rampmode.write()

    def set_motion_profile(self, max_speed: int, acceleration: int, deceleration: int):
        """sets the motion profile of the internal ramp generator
        Args:
            max_speed (int): maximum speed in µsteps/s
            acceleration (int): acceleration in µsteps/s²
            deceleration (int): deceleration in µsteps/s²
        """
        vstart = self.get_register("vstart")
        vstart.vstart = 5  # Motor start velocity (unsigned)
        vstart.write()

        vstop = self.get_register("vstop")
        vstop.vstop = 10  # Motor stop velocity (unsigned)
        vstop.write()

        v1 = self.get_register("v1")
        v1.v1 = 0  # disables A1/D1 phase
        v1.write()

        vmax = self.get_register("vmax")
        vmax.vmax = max_speed
        vmax.write()

        amax = self.get_register("amax")
        amax.amax = acceleration
        amax.write()

        dmax = self.get_register("dmax")
        dmax.dmax = deceleration
        dmax.write()

    def make_a_step(self):
        """method that makes on step"""
        raise NotImplementedError

    def stop(self, stop_mode=StopMode.HARDSTOP):
        """stop the current movement

        Args:
            stop_mode (enum): whether the movement should be stopped immediately or softly
                (Default value = StopMode.HARDSTOP)
        """
        self.set_ramp_mode(RampMode.VELOCITY_MODE_POS)

        vmax = self.get_register("vmax")
        vmax.vmax = 0
        vmax.write()

        if stop_mode == StopMode.HARDSTOP:
            amax = self.get_register("amax")
            amax.amax = 65535  # max deceleration (amax is used in velocity mode for deceleration)
            amax.write()

    def wait_until_stop(self):
        """blocks the code until the movement is finished or stopped from a different thread!"""
        ramp_stat = self.get_register("ramp_stat")
        while True:
            ramp_stat.read()
            if ramp_stat.position_reached:
                self._tmc_logger.log("position reached", Loglevel.MOVEMENT)
                return
            time.sleep(0.01)  # sleep 10ms to reduce CPU load

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
        # pylint: disable=too-many-locals
        if movement_abs_rel is None:
            movement_abs_rel = self._movement_abs_rel

        if movement_abs_rel == MovementAbsRel.RELATIVE:
            self._target_pos = self._current_pos + steps
        else:
            self._target_pos = steps

        self.set_ramp_mode(RampMode.POSITIONING_MODE)
        self.set_motion_profile(self._max_speed, self._acceleration, self._acceleration)

        self._tmc_logger.log(
            f"cur: {self._current_pos} | tar: {self._target_pos}", Loglevel.MOVEMENT
        )

        xtarget = self.get_register("xtarget")
        xtarget.xtarget = self._target_pos
        xtarget.write()

        self.wait_until_stop()
