#pylint: disable=wildcard-import
#pylint: disable=unused-wildcard-import
#pylint: disable=no-member
"""
Many boards have RaspberryPI-compatible PinOut,
but require to import special GPIO module instead RPI.GPIO

This module determines the type of board
and import the corresponding GPIO module

Can be extended to support BeagleBone or other boards
Supports MicroPython
"""

from importlib import import_module
from typing import Protocol, Any, runtime_checkable
from ._tmc_gpio_board_base import *


@runtime_checkable
class GPIOModuleProtocol(Protocol):
    """Protocol defining the interface for GPIO modules like RPi.GPIO, Jetson.GPIO, etc."""
    # pylint: disable=missing-function-docstring

    BCM: int
    BOARD: int
    IN: int
    OUT: int
    HIGH: int
    LOW: int
    PUD_OFF: int
    PUD_UP: int
    PUD_DOWN: int
    RISING: int

    def setwarnings(self, value: bool) -> None: ...
    def setmode(self, mode: int) -> None: ...
    def cleanup(self, pin: int | None = None) -> None: ...
    def setup(self, pin: int, mode: int, initial: int = 0, pull_up_down: int = 0) -> None: ...
    def input(self, pin: int) -> int: ...
    def output(self, pin: int, value: int) -> None: ...
    def PWM(self, pin: int, frequency: int) -> Any: ...  # Returns PWM object
    def add_event_detect(self, pin: int, edge: int, callback: Any = None, bouncetime: int = 0) -> None: ...
    def remove_event_detect(self, pin: int) -> None: ...


class BaseRPiGPIOWrapper(BaseGPIOWrapper):
    """RPI.GPIO base wrapper"""

    def __init__(self, gpio_module: GPIOModuleProtocol):
        """constructor

        Args:
            gpio_module: GPIO module conforming to GPIOModuleProtocol (e.g., RPi.GPIO, Jetson.GPIO)
        """
        self.GPIO: GPIOModuleProtocol = gpio_module
        self._gpios_pwm: list[Any] = [None] * 200

    def init(self, gpio_mode=None):
        """initialize GPIO library"""
        self.GPIO.setwarnings(False)
        if gpio_mode is None:
            gpio_mode = self.GPIO.BCM
        self.GPIO.setmode(gpio_mode)

    def deinit(self):
        """deinitialize GPIO library"""
        self.GPIO.cleanup()

    def gpio_setup(self, pin:int, mode:GpioMode, initial:Gpio=Gpio.LOW, pull_up_down:GpioPUD=GpioPUD.PUD_OFF):
        """setup GPIO pin"""
        initial = int(initial)
        pull_up_down = int(pull_up_down)
        mode = int(mode)
        if mode == GpioMode.OUT:
            self.GPIO.setup(pin, mode, initial=initial)
        else:
            self.GPIO.setup(pin, mode, pull_up_down=pull_up_down)

    def gpio_cleanup(self, pin:int):
        """cleanup GPIO pin"""
        self.GPIO.cleanup(pin)

    def gpio_input(self, pin:int) -> int:
        """read GPIO pin"""
        return self.GPIO.input(pin)

    def gpio_output(self, pin:int, value:int):
        """write GPIO pin"""
        self.GPIO.output(pin, value)

    def gpio_pwm_setup(self, pin:int, frequency:int = 10, duty_cycle:int = 0):
        """setup PWM"""
        self.GPIO.setup(pin, int(GpioMode.OUT), initial=int(Gpio.LOW))
        self._gpios_pwm[pin] = self.GPIO.PWM(pin, frequency)
        self._gpios_pwm[pin].start(duty_cycle)

    def gpio_pwm_set_frequency(self, pin:int, frequency:int):
        """set PWM frequency"""
        self._gpios_pwm[pin].ChangeFrequency(frequency)

    def gpio_pwm_set_duty_cycle(self, pin:int, duty_cycle:int):
        """set PWM duty cycle

        Args:
            pin (int): pin number
            duty_cycle (int): duty cycle in percent (0-100)
        """
        self._gpios_pwm[pin].ChangeDutyCycle(duty_cycle)

    def gpio_add_event_detect(self, pin:int, callback:types.FunctionType):
        """add event detect"""
        self.GPIO.add_event_detect(pin, self.GPIO.RISING, callback=callback, bouncetime=300)

    def gpio_remove_event_detect(self, pin:int):
        """remove event detect"""
        self.GPIO.remove_event_detect(pin)


def create_gpio_wrapper(module_name: str, description: str) -> BaseRPiGPIOWrapper:
    """Factory function to create a GPIO wrapper with the specified module.

    Args:
        module_name: Name of the GPIO module to import (e.g., 'RPi.GPIO', 'Jetson.GPIO')
        description: Description for logging (e.g., 'GPIO control', 'GPIO mocking')

    Returns:
        Configured BaseRPiGPIOWrapper instance
    """
    gpio_module = import_module(module_name)
    dependencies_logger.log(f"using {module_name} for {description}", Loglevel.INFO)
    return BaseRPiGPIOWrapper(gpio_module)


# Convenience factory functions for each GPIO type
def MockGPIOWrapper() -> BaseRPiGPIOWrapper:
    """Create Mock.GPIO wrapper"""
    return create_gpio_wrapper('Mock.GPIO', 'GPIO mocking')


def RPiGPIOWrapper() -> BaseRPiGPIOWrapper:
    """Create RPi.GPIO wrapper"""
    return create_gpio_wrapper('RPi.GPIO', 'GPIO control')


def JetsonGPIOWrapper() -> BaseRPiGPIOWrapper:
    """Create Jetson.GPIO wrapper"""
    return create_gpio_wrapper('Jetson.GPIO', 'GPIO control')


def OPiGPIOWrapper() -> BaseRPiGPIOWrapper:
    """Create OPi.GPIO wrapper"""
    return create_gpio_wrapper('OPi.GPIO', 'GPIO control')
