"""Base GPIO wrapper for boards with RaspberryPi-compatible PinOut.

Many boards require importing a special GPIO module instead of RPi.GPIO.
"""

from enum import IntEnum
from abc import abstractmethod
import types
from ..tmc_logger import TmcLogger, Loglevel


class Board(IntEnum):
    """board."""

    UNKNOWN = 0
    RASPBERRY_PI = 1  # all except Pi 5
    RASPBERRY_PI5 = 2
    NVIDIA_JETSON = 3
    LUCKFOX_PICO = 4
    ORANGE_PI = 5
    MICROPYTHON = 6
    CIRCUITPYTHON = 7


class Gpio(IntEnum):
    """GPIO value."""

    LOW = 0
    HIGH = 1


class GpioMode(IntEnum):
    """GPIO mode."""

    OUT = 0
    IN = 1


class GpioPUD(IntEnum):
    """Pull up Down."""

    PUD_OFF = 20
    PUD_UP = 22
    PUD_DOWN = 21


BOARD = Board.UNKNOWN
dependencies_logger = TmcLogger(Loglevel.DEBUG, "DEPENDENCIES")


class BaseGPIOWrapper:
    """Base class for GPIO wrappers."""

    @abstractmethod
    def init(self, gpio_mode=None):
        """Initialize GPIO library."""

    @abstractmethod
    def deinit(self):
        """Deinitialize GPIO library."""

    @abstractmethod
    def gpio_setup(
        self,
        pin: int,
        mode: GpioMode,
        initial: Gpio = Gpio.LOW,
        pull_up_down: GpioPUD = GpioPUD.PUD_OFF,
    ):
        """Setup GPIO pin."""

    @abstractmethod
    def gpio_cleanup(self, pin: int):
        """Cleanup GPIO pin."""

    @abstractmethod
    def gpio_input(self, pin: int) -> int:
        """Read GPIO pin."""

    @abstractmethod
    def gpio_output(self, pin: int, value):
        """Write GPIO pin."""

    @abstractmethod
    def gpio_pwm_setup(self, pin: int, frequency: int = 10, duty_cycle: int = 0):
        """Setup PWM."""

    @abstractmethod
    def gpio_pwm_set_frequency(self, pin: int, frequency: int):
        """Set PWM frequency."""

    @abstractmethod
    def gpio_pwm_set_duty_cycle(self, pin: int, duty_cycle: int):
        """Set PWM duty cycle.

        Args:
            pin (int): pin number
            duty_cycle (int): duty cycle in percent (0-100)
        """

    @abstractmethod
    def gpio_add_event_detect(self, pin: int, callback: types.FunctionType):
        """Add event detect."""

    @abstractmethod
    def gpio_remove_event_detect(self, pin: int):
        """Remove event detect."""
