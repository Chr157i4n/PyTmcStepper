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
from ..tmc_logger import Loglevel
from ..reg import _tmc5160_reg as tmc5160_reg

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

    @property
    def current_pos(self):
        """_current_pos property"""
        xactual: tmc5160_reg.XActual = self.get_register("xactual")
        xactual.read()
        self._current_pos = xactual.xactual
        return self._current_pos

    @current_pos.setter
    def current_pos(self, current_pos: int):
        """_current_pos setter"""
        super().current_pos = current_pos
        xactual: tmc5160_reg.XActual = self.get_register("xactual")
        xactual.xactual = current_pos
        xactual.write()

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
        rampmode: tmc5160_reg.RampMode = self.get_register("rampmode")
        rampmode.rampmode = int(ramp_mode)
        rampmode.write()

    def set_motion_profile(self, max_speed: int, acceleration: int, deceleration: int):
        """sets the motion profile of the internal ramp generator
        Args:
            max_speed (int): maximum speed in µsteps/s
            acceleration (int): acceleration in µsteps/s²
            deceleration (int): deceleration in µsteps/s²
        """
        vstart: tmc5160_reg.VStart = self.get_register("vstart")
        vstart.vstart = 5  # Motor start velocity (unsigned)
        vstart.write()

        vstop: tmc5160_reg.VStop = self.get_register("vstop")
        vstop.vstop = 10  # Motor stop velocity (unsigned)
        vstop.write()

        # Datasheet says:
        # 0: Disables A1 and D1 phase, use AMAX, DMAX only
        # but that did not work in my tests, so we set them to the same as VMAX/AMAX/DMAX
        v1: tmc5160_reg.V1 = self.get_register("v1")
        v1.v1 = max_speed
        v1.write()

        a1: tmc5160_reg.A1 = self.get_register("a1")
        a1.a1 = acceleration
        a1.write()

        d1: tmc5160_reg.D1 = self.get_register("d1")
        d1.d1 = deceleration
        d1.write()

        vmax: tmc5160_reg.VMax = self.get_register("vmax")
        vmax.vmax = max_speed
        vmax.write()

        amax: tmc5160_reg.AMax = self.get_register("amax")
        amax.amax = acceleration
        amax.write()

        dmax: tmc5160_reg.DMax = self.get_register("dmax")
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
        super().stop(stop_mode)
        self.set_ramp_mode(RampMode.VELOCITY_MODE_POS)

        vmax: tmc5160_reg.VMax = self.get_register("vmax")
        vmax.vmax = 0
        vmax.write()

        if stop_mode == StopMode.HARDSTOP:
            amax: tmc5160_reg.AMax = self.get_register("amax")
            amax.amax = 65535  # max deceleration (amax is used in velocity mode for deceleration)
            amax.write()

    def wait_until_stop(self):
        """blocks the code until the movement is finished or stopped from a different thread!"""
        rampstat: tmc5160_reg.RampStat = self.get_register("rampstat")
        while True:
            # self._tmc_logger.log(f"current pos: {self.current_pos}", Loglevel.MOVEMENT)
            rampstat.read()
            if rampstat.position_reached:
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
        self._current_pos = self.current_pos  # sync current pos with register

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

        xtarget: tmc5160_reg.XTarget = self.get_register("xtarget")
        xtarget.xtarget = self._target_pos
        xtarget.write()

        self.wait_until_stop()

        loststeps: tmc5160_reg.LostSteps = self.get_register("loststeps")
        loststeps.read()
        if loststeps.lost_steps != 0:
            self._tmc_logger.log(
                f"Lost steps detected: {loststeps.lost_steps}", Loglevel.MOVEMENT
            )

        return self._stop
