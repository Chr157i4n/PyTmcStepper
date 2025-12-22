"""
Enable Control base module
"""

from ._tmc_ec import TmcEnableControl
from ..tmc_gpio import Gpio, GpioMode
from .. import tmc_gpio
from .._tmc_logger import TmcLogger, Loglevel


class TmcEnableControlPin(TmcEnableControl):
    """Enable Control base class"""


    @property
    def pin_en(self):
        """pin_en property"""
        return self._pin_en


    def __init__(self, pin_en:int):
        """constructor"""
        super().__init__()
        self._pin_en = pin_en


    def init(self, tmc_logger: TmcLogger):
        """init: called by the Tmc class"""
        super().init(tmc_logger)
        self._tmc_logger.log(f"EN Pin: {self._pin_en}", Loglevel.DEBUG)
        tmc_gpio.tmc_gpio.gpio_setup(self._pin_en, GpioMode.OUT, initial=Gpio.HIGH)


    def __del__(self):
        self.deinit()


    def deinit(self):
        """destructor"""
        if self._pin_en is not None:
            tmc_gpio.tmc_gpio.gpio_cleanup(self._pin_en)
            self._pin_en = None


    def set_motor_enabled(self, en):
        """enables or disables the motor current output

        Args:
            en (bool): whether the motor current output should be enabled
        """
        if self._pin_en is not None:
            tmc_gpio.tmc_gpio.gpio_output(self._pin_en, not en)
            self._tmc_logger.log(f"Motor output active: {en}", Loglevel.INFO)
