"""
Many boards have RaspberryPI-compatible PinOut,
but require to import special GPIO module instead RPI.GPIO
"""

from enum import IntEnum
from abc import abstractmethod
import types
from .._tmc_logger import TmcLogger, Loglevel

class Board(IntEnum):
    """board"""
    UNKNOWN = 0
    RASPBERRY_PI = 1 # all except Pi 5
    RASPBERRY_PI5 = 2
    NVIDIA_JETSON = 3
    LUCKFOX_PICO = 4
    ORANGE_PI = 5
    MICROPYTHON = 6

class Gpio(IntEnum):
    """GPIO value"""
    LOW = 0
    HIGH = 1

class GpioMode(IntEnum):
    """GPIO mode"""
    OUT = 0
    IN = 1

class GpioPUD(IntEnum):
    """Pull up Down"""
    PUD_OFF = 20
    PUD_UP = 22
    PUD_DOWN = 21


BOARD = Board.UNKNOWN
dependencies_logger = TmcLogger(Loglevel.DEBUG, "DEPENDENCIES")


class BaseGPIOWrapper():
    """Base class for GPIO wrappers"""

    @abstractmethod
    def init(self, gpio_mode=None):
        """initialize GPIO library"""

    @abstractmethod
    def deinit(self):
        """deinitialize GPIO library"""

    @abstractmethod
    def gpio_setup(self, pin:int, mode:GpioMode, initial:Gpio=Gpio.LOW, pull_up_down:GpioPUD=GpioPUD.PUD_OFF):
        """setup GPIO pin"""

    @abstractmethod
    def gpio_cleanup(self, pin:int):
        """cleanup GPIO pin"""

    @abstractmethod
    def gpio_input(self, pin:int) -> int:
        """read GPIO pin"""

    @abstractmethod
    def gpio_output(self, pin:int, value):
        """write GPIO pin"""

    @abstractmethod
    def gpio_pwm_setup(self, pin:int, frequency:int = 10, duty_cycle:int = 0):
        """setup PWM"""

    @abstractmethod
    def gpio_pwm_set_frequency(self, pin:int, frequency:int):
        """set PWM frequency"""

    @abstractmethod
    def gpio_pwm_set_duty_cycle(self, pin:int, duty_cycle:int):
        """set PWM duty cycle

        Args:
            pin (int): pin number
            duty_cycle (int): duty cycle in percent (0-100)
        """

    @abstractmethod
    def gpio_add_event_detect(self, pin:int, callback:types.FunctionType):
        """add event detect"""

    @abstractmethod
    def gpio_remove_event_detect(self, pin:int):
        """remove event detect"""
