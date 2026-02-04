"""STEP/REG Motion Control module."""

from ._tmc_mc import Direction
from ._tmc_mc_step_dir import TmcMotionControlStepDir
from ..tmc_logger import Loglevel
from .. import tmc_gpio
from ..reg import _tmc_shared_regs as tmc_shared_reg


class TmcMotionControlStepReg(TmcMotionControlStepDir):
    """STEP/REG Motion Control class."""

    def __init__(self, pin_step: int):
        """constructor."""
        super().__init__(pin_step, None)

    def deinit(self):
        """destructor."""
        if self._pin_step is not None:
            tmc_gpio.tmc_gpio.gpio_cleanup(self._pin_step)
            self._pin_step = None

    def set_direction(self, direction: Direction):
        """Sets the motor shaft direction to the given value: 0 = CCW; 1 = CW.

        Args:
            direction (bool): motor shaft direction: False = CCW; True = CW
        """
        self._direction = direction
        self._tmc_logger.log(f"New Direction is: {direction}", Loglevel.MOVEMENT)

        gconf: tmc_shared_reg.GConf = self.get_register("gconf")

        gconf.modify("shaft", bool(int(direction)))
