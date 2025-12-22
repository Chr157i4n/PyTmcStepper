#pylint: skip-file
"""
MicroPython GPIO module
"""

from machine import Pin, PWM
from ._tmc_gpio_board_base import *


class MicroPythonGPIOWrapper(BaseGPIOWrapper):
    """MicroPython GPIO wrapper for Raspberry Pi Pico (RP2040) and similar boards.

    Uses machine.Pin and machine.PWM for GPIO control.
    Only available when running under MicroPython.
    """

    def __init__(self):
        """constructor"""
        self._pins = {}  # pin_num -> Pin object
        self._pwms = {}  # pin_num -> PWM object

    def init(self, gpio_mode=None):
        """initialize GPIO library - not needed for MicroPython"""

    def deinit(self):
        """deinitialize GPIO library"""
        for pin_num in list(self._pwms.keys()):
            self.gpio_cleanup(pin_num)
        for pin_num in list(self._pins.keys()):
            self.gpio_cleanup(pin_num)

    def gpio_setup(self, pin, mode, initial=0, pull_up_down=0):
        """setup GPIO pin

        Args:
            pin: GPIO pin number
            mode: GpioMode.OUT or GpioMode.IN
            initial: Initial value for output pins
            pull_up_down: Pull-up/down configuration
        """
        if mode == GpioMode.OUT:
            self._pins[pin] = Pin(pin, Pin.OUT, value=initial)
        else:
            # Configure pull-up/down
            if pull_up_down == GpioPUD.PUD_UP:
                self._pins[pin] = Pin(pin, Pin.IN, Pin.PULL_UP)
            elif pull_up_down == GpioPUD.PUD_DOWN:
                self._pins[pin] = Pin(pin, Pin.IN, Pin.PULL_DOWN)
            else:
                self._pins[pin] = Pin(pin, Pin.IN)

    def gpio_cleanup(self, pin):
        """cleanup GPIO pin"""
        if pin in self._pwms:
            self._pwms[pin].deinit()
            del self._pwms[pin]
        if pin in self._pins:
            del self._pins[pin]

    def gpio_input(self, pin):
        """read GPIO pin"""
        if pin in self._pins:
            return self._pins[pin].value()
        return 0

    def gpio_output(self, pin, value):
        """write GPIO pin"""
        if pin in self._pins:
            self._pins[pin].value(value)

    def gpio_pwm_setup(self, pin, frequency=10, duty_cycle=0):
        """setup PWM

        Args:
            pin: GPIO pin number
            frequency: PWM frequency in Hz
            duty_cycle: Duty cycle in percent (0-100)
        """
        self._pwms[pin] = PWM(Pin(pin))
        self._pwms[pin].freq(frequency)
        # MicroPython uses 0-65535 for duty, convert from percent
        self._pwms[pin].duty_u16(int(duty_cycle /100 *65535))

    def gpio_pwm_set_frequency(self, pin, frequency):
        """set PWM frequency"""
        if pin in self._pwms:
            self._pwms[pin].freq(frequency)

    def gpio_pwm_set_duty_cycle(self, pin, duty_cycle):
        """set PWM duty cycle

        Args:
            pin: GPIO pin number
            duty_cycle: Duty cycle in percent (0-100)
        """
        if pin in self._pwms:
            # Convert percent to 0-65535
            self._pwms[pin].duty_u16(int(duty_cycle * 655.35))

    def gpio_add_event_detect(self, pin, callback):
        """add event detect (rising edge interrupt)"""
        if pin in self._pins:
            self._pins[pin].irq(trigger=Pin.IRQ_RISING, handler=callback)

    def gpio_remove_event_detect(self, pin):
        """remove event detect"""
        if pin in self._pins:
            self._pins[pin].irq(handler=None)
