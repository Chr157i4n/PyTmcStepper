#pylint: disable=too-many-instance-attributes
#pylint: disable=too-many-arguments
#pylint: disable=too-many-branches
#pylint: disable=too-many-positional-arguments
"""
STEP_PWM/DIR Motion Control module
"""

from ._tmc_mc import MovementAbsRel, Direction, StopMode
from ._tmc_mc_step_dir import TmcMotionControlStepDir
from .._tmc_logger import TmcLogger, Loglevel
from .. import tmc_gpio


class TmcMotionControlStepPwmDir(TmcMotionControlStepDir):
    """STEP_PWM/DIR Motion Control class"""

    @property
    def speed(self):
        """_speed property"""
        return self._speed

    @speed.setter
    def speed(self, speed:int):
        """_speed setter"""
        self._speed = speed
        tmc_gpio.tmc_gpio.gpio_pwm_set_frequency(self._pin_step, self._speed)
        self._tmc_logger.log(f"Speed: {self._speed} msteps/s", Loglevel.DEBUG)


    def init(self, tmc_logger:TmcLogger):
        """init: called by the Tmc class"""
        super().init(tmc_logger)
        tmc_gpio.tmc_gpio.gpio_pwm_setup(self._pin_step, 1, 0)


    def stop(self, stop_mode = StopMode.HARDSTOP):
        """stop the current movement

        Args:
            stop_mode (enum): whether the movement should be stopped immediately or softly
                (Default value = StopMode.HARDSTOP)
        """
        super().stop(stop_mode)
        tmc_gpio.tmc_gpio.gpio_pwm_set_duty_cycle(self._pin_step, 0)


    def run_to_position_steps(self, steps, movement_abs_rel:MovementAbsRel = None) -> StopMode:
        """runs the motor to a specific position

        Args:
            steps (int): position in µsteps
            movement_abs_rel (enum, optional): whether the movement is absolute or relative
                (Default value = None)

        Returns:
            StopMode: the stop mode
        """
        if tmc_gpio.tmc_gpio.__class__.__name__ == "GpiozeroWrapper":
            tmc_gpio.tmc_gpio.gpio_pwm_enable(self._pin_step, False)

        return super().run_to_position_steps(steps, movement_abs_rel)


    def run_speed_pwm(self, speed:int = None):
        """runs the motor
        does not block the code
        """
        if speed is None:
            speed = self.max_speed

        if tmc_gpio.tmc_gpio.__class__.__name__ == "GpiozeroWrapper":
            tmc_gpio.tmc_gpio.gpio_pwm_enable(self._pin_step, True)

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


    def run_speed_pwm_fullstep(self, speed:int = None):
        """runs the motor
        does not block the code
        """
        if speed is None:
            speed = self.max_speed_fullstep
        self.run_speed_pwm(speed * self.mres)
