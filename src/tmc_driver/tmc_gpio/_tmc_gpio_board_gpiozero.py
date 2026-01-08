# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
"""
Many boards have RaspberryPI-compatible PinOut,
but require to import special GPIO module instead RPI.GPIO

This module determines the type of board
and import the corresponding GPIO module

Can be extended to support BeagleBone or other boards
Supports MicroPython
"""

from gpiozero import (
    DigitalInputDevice,
    DigitalOutputDevice,
    PWMOutputDevice,
    GPIODevice,
)
from ._tmc_gpio_board_base import *


class GpiozeroWrapper(BaseGPIOWrapper):
    """gpiozero GPIO wrapper"""

    def __init__(self):
        """constructor, imports gpiozero"""
        self._gpios: list[GPIODevice | None] = [None] * 200
        self._gpios_pwm: list[PWMOutputDevice | None] = [None] * 200
        dependencies_logger.log("using gpiozero for GPIO control", Loglevel.INFO)

    def init(self, gpio_mode=None):
        """initialize GPIO library. pass on gpiozero"""

    def deinit(self):
        """deinitialize GPIO library. pass on gpiozero"""

    def gpio_setup(
        self,
        pin: int,
        mode: GpioMode,
        initial: Gpio = Gpio.LOW,
        pull_up_down: GpioPUD = GpioPUD.PUD_OFF,
    ):
        """setup GPIO pin"""
        if mode == GpioMode.OUT:
            gpio = self._gpios[pin]
            if gpio is None or gpio.closed:
                self._gpios[pin] = DigitalOutputDevice(pin, initial_value=bool(initial))
        else:
            gpio = self._gpios[pin]
            if gpio is None or gpio.closed:
                self._gpios[pin] = DigitalInputDevice(pin)

    def gpio_cleanup(self, pin: int):
        """cleanup GPIO pin"""
        gpio = self._gpios[pin]
        if gpio is not None:
            gpio.close()
            self._gpios[pin] = None
        gpio_pwm = self._gpios_pwm[pin]
        if gpio_pwm is not None:
            gpio_pwm.close()
            self._gpios_pwm[pin] = None

    def gpio_input(self, pin: int) -> int:
        """read GPIO pin"""
        gpio = self._gpios[pin]
        if not isinstance(gpio, DigitalInputDevice):
            raise RuntimeError(f"GPIO pin {pin} not configured as input")
        return gpio.value

    def gpio_output(self, pin: int, value):
        """write GPIO pin"""
        gpio = self._gpios[pin]
        if not isinstance(gpio, DigitalOutputDevice):
            raise RuntimeError(f"GPIO pin {pin} not configured as output")
        gpio.value = value

    def gpio_pwm_enable(self, pin: int, enable: bool):
        """switch to PWM"""
        if enable:
            if self._gpios[pin] is not None:
                self._gpios[pin] = None
                self._gpios_pwm[pin] = PWMOutputDevice(pin)
        else:
            if self._gpios_pwm[pin] is not None:
                self._gpios_pwm[pin] = None
                self._gpios[pin] = DigitalOutputDevice(pin)

    def gpio_pwm_setup(self, pin: int, frequency: int = 10, duty_cycle: int = 0):
        """setup PWM"""
        # self._gpios_pwm[pin] = PWMOutputDevice(pin)

    def gpio_pwm_set_frequency(self, pin: int, frequency: int):
        """set PWM frequency"""
        gpio = self._gpios_pwm[pin]
        if not isinstance(gpio, PWMOutputDevice):
            raise RuntimeError(f"GPIO pin {pin} not configured as PWM")
        gpio.frequency = frequency

    def gpio_pwm_set_duty_cycle(self, pin: int, duty_cycle: int):
        """set PWM duty cycle

        Args:
            pin (int): pin number
            duty_cycle (int): duty cycle in percent (0-100)
        """
        gpio = self._gpios_pwm[pin]
        if not isinstance(gpio, PWMOutputDevice):
            raise RuntimeError(f"GPIO pin {pin} not configured as PWM")
        gpio.value = duty_cycle / 100

    def gpio_add_event_detect(self, pin: int, callback: types.FunctionType):
        """add event detect"""
        gpio = self._gpios_pwm[pin]
        if not isinstance(gpio, DigitalInputDevice):
            raise RuntimeError(f"GPIO pin {pin} not configured as input")
        gpio.when_activated = callback

    def gpio_remove_event_detect(self, pin: int):
        """remove event detect"""
        gpio = self._gpios_pwm[pin]
        if not isinstance(gpio, DigitalInputDevice):
            raise RuntimeError(f"GPIO pin {pin} not configured as input")
        gpio.when_activated = None
