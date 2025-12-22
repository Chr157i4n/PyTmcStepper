#pylint: disable=wildcard-import
#pylint: disable=unused-wildcard-import
"""
Many boards have RaspberryPI-compatible PinOut,
but require to import special GPIO module instead RPI.GPIO

This module determines the type of board
and import the corresponding GPIO module

Can be extended to support BeagleBone or other boards
Supports MicroPython
"""

from periphery import GPIO
from ._tmc_gpio_board_base import *

class peripheryWrapper(BaseGPIOWrapper):
    """periphery GPIO wrapper"""

    def __init__(self):
        """constructor, imports periphery"""
        dependencies_logger.log("using periphery for GPIO control", Loglevel.INFO)
        self._gpios:list[GPIO] = [None] * 200

    def init(self, gpio_mode=None):
        """initialize GPIO library. pass on periphery"""

    def deinit(self):
        """deinitialize GPIO library. pass on periphery"""

    def gpio_setup(self, pin:int, mode:GpioMode, initial:Gpio=Gpio.LOW, pull_up_down:GpioPUD=GpioPUD.PUD_OFF):
        """setup GPIO pin"""
        mode = 'out' if (mode == GpioMode.OUT) else 'in'
        self._gpios[pin] = GPIO(pin, mode)

    def gpio_cleanup(self, pin:int):
        """cleanup GPIO pin"""
        if self._gpios[pin] is not None:
            self._gpios[pin].close()
            self._gpios[pin] = None

    def gpio_input(self, pin:int) -> int:
        """read GPIO pin"""
        return self._gpios[pin].read()

    def gpio_output(self, pin:int, value):
        """write GPIO pin"""
        self._gpios[pin].write(bool(value))

    def gpio_pwm_setup(self, pin:int, frequency:int = 10, duty_cycle:int = 0):
        """setup PWM"""
        raise NotImplementedError

    def gpio_pwm_set_frequency(self, pin:int, frequency:int):
        """set PWM frequency"""
        raise NotImplementedError

    def gpio_pwm_set_duty_cycle(self, pin:int, duty_cycle:int):
        """set PWM duty cycle

        Args:
            pin (int): pin number
            duty_cycle (int): duty cycle in percent (0-100)
        """
        raise NotImplementedError

    def gpio_add_event_detect(self, pin:int, callback:types.FunctionType):
        """add event detect"""
        raise NotImplementedError

    def gpio_remove_event_detect(self, pin:int):
        """remove event detect"""
        raise NotImplementedError
