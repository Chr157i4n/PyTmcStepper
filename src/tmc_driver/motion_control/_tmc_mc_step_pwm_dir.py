# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments
# pylint: disable=too-many-branches
# pylint: disable=too-many-positional-arguments
"""STEP_PWM/DIR Motion Control module."""

from ._tmc_mc import Direction, StopMode
from ._tmc_mc_step_dir import TmcMotionControlStepDir
from ..tmc_logger import TmcLogger, Loglevel
from .. import tmc_gpio
from .._tmc_exceptions import TmcMotionControlException


class TmcMotionControlStepPwmDir(TmcMotionControlStepDir):
    """STEP_PWM/DIR Motion Control class."""

    @property
    def speed(self):
        """_speed property."""
        return self._speed

    @speed.setter
    def speed(self, speed: int):
        """_speed setter."""
        self._speed = speed
        tmc_gpio.tmc_gpio.gpio_pwm_set_frequency(self._pin_step, self._speed)
        self._tmc_logger.log(f"Speed: {self._speed} msteps/s", Loglevel.DEBUG)

    def init(self, tmc_logger: TmcLogger):
        """Init: called by the Tmc class."""
        super().init(tmc_logger)
        tmc_gpio.tmc_gpio.gpio_pwm_setup(self._pin_step, 1, 0)

    def stop(self, stop_mode=StopMode.HARDSTOP):
        """Stop the current movement.

        Args:
            stop_mode (enum): whether the movement should be stopped immediately or softly
                (Default value = StopMode.HARDSTOP)
        """
        super().stop(stop_mode)
        tmc_gpio.tmc_gpio.gpio_pwm_set_duty_cycle(self._pin_step, 0)

    def run_speed_pwm(self, speed: int | None = None):
        """Runs the motor at a given speed using PWM."""
        if self._pin_step is None:
            raise TmcMotionControlException(
                "Step pin not set for STEP_PWM/DIR motion control"
            )

        if speed is None:
            speed = self.max_speed

        if speed == 0:
            # stop movement
            tmc_gpio.tmc_gpio.gpio_pwm_set_duty_cycle(self._pin_step, 0)
        else:
            if speed < 0:
                self.set_direction(Direction.CCW)
                speed = -speed
            else:
                self.set_direction(Direction.CW)

            # change pwm frequency
            self.speed = speed
            tmc_gpio.tmc_gpio.gpio_pwm_set_duty_cycle(self._pin_step, 50)

    def run_speed_pwm_fullstep(self, speed: int | None = None):
        """Runs the motor does not block the code."""
        if speed is None:
            speed = self.max_speed_fullstep
        self.run_speed_pwm(speed * self.mres)
