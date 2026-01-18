# pylint: skip-file
"""
CircuitPython GPIO module
"""

import digitalio
import pwmio
from ._tmc_gpio_board_base import *


class CircuitPythonGPIOWrapper(BaseGPIOWrapper):
    """CircuitPython GPIO wrapper for boards supporting CircuitPython.

    Uses digitalio.DigitalInOut and pwmio.PWMOut for GPIO control.
    Only available when running under CircuitPython.

    Note: Pins should be board pin objects (e.g., board.D17) or
    microcontroller pin objects, not integers.
    """

    def __init__(self):
        """constructor"""
        self._pins = {}  # pin -> DigitalInOut object
        self._pwms = {}  # pin -> PWMOut object

    def init(self, gpio_mode=None):
        """initialize GPIO library - not needed for CircuitPython"""

    def deinit(self):
        """deinitialize GPIO library"""
        for pin in list(self._pwms.keys()):
            self.gpio_cleanup(pin)
        for pin in list(self._pins.keys()):
            self.gpio_cleanup(pin)

    def gpio_setup(self, pin, mode, initial=0, pull_up_down=0):
        """setup GPIO pin

        Args:
            pin: Board pin object (e.g., board.D17) or microcontroller pin
            mode: GpioMode.OUT or GpioMode.IN
            initial: Initial value for output pins
            pull_up_down: Pull-up/down configuration
        """
        pin_obj = digitalio.DigitalInOut(pin)

        if mode == GpioMode.OUT:
            pin_obj.direction = digitalio.Direction.OUTPUT
            pin_obj.value = bool(initial)
        else:
            pin_obj.direction = digitalio.Direction.INPUT
            # Configure pull-up/down
            if pull_up_down == GpioPUD.PUD_UP:
                pin_obj.pull = digitalio.Pull.UP
            elif pull_up_down == GpioPUD.PUD_DOWN:
                pin_obj.pull = digitalio.Pull.DOWN
            else:
                pin_obj.pull = None

        self._pins[pin] = pin_obj

    def gpio_cleanup(self, pin):
        """cleanup GPIO pin"""
        if pin in self._pwms:
            self._pwms[pin].deinit()
            del self._pwms[pin]
        if pin in self._pins:
            self._pins[pin].deinit()
            del self._pins[pin]

    def gpio_input(self, pin):
        """read GPIO pin

        Returns:
            1 if HIGH, 0 if LOW
        """
        if pin in self._pins:
            return 1 if self._pins[pin].value else 0
        return 0

    def gpio_output(self, pin, value):
        """write GPIO pin"""
        if pin in self._pins:
            self._pins[pin].value = bool(value)

    def gpio_pwm_setup(self, pin, frequency=10, duty_cycle=0):
        """setup PWM

        Args:
            pin: Board pin object (e.g., board.D17)
            frequency: PWM frequency in Hz
            duty_cycle: Duty cycle in percent (0-100)
        """
        # CircuitPython PWM uses 0-65535 for duty_cycle
        duty_u16 = int(duty_cycle / 100 * 65535)
        self._pwms[pin] = pwmio.PWMOut(pin, frequency=frequency, duty_cycle=duty_u16)

    def gpio_pwm_set_frequency(self, pin, frequency):
        """set PWM frequency"""
        if pin in self._pwms:
            self._pwms[pin].frequency = frequency

    def gpio_pwm_set_duty_cycle(self, pin, duty_cycle):
        """set PWM duty cycle

        Args:
            pin: Board pin object
            duty_cycle: Duty cycle in percent (0-100)
        """
        if pin in self._pwms:
            # Convert percent to 0-65535
            self._pwms[pin].duty_cycle = int(duty_cycle * 655.35)

    def gpio_add_event_detect(self, pin, callback):
        """add event detect (rising edge interrupt)"""
        # CircuitPython doesn't have Pin.irq() - would need asyncio
        raise NotImplementedError(
            "GPIO interrupts not directly supported in CircuitPython."
        )

    def gpio_remove_event_detect(self, pin):
        """remove event detect"""
        # Not implemented - see gpio_add_event_detect
        pass
