# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
"""GPIO wrapper using python-periphery for RaspberryPi-compatible boards.

Many boards require importing a special GPIO module instead of RPi.GPIO.
This module determines the type of board and imports the corresponding
GPIO module.

Can be extended to support BeagleBone or other boards.
Supports MicroPython.
"""

from periphery import GPIO
from ._tmc_gpio_board_base import *


class peripheryWrapper(BaseGPIOWrapper):
    """Periphery GPIO wrapper."""

    def __init__(self):
        """Constructor, imports periphery."""
        dependencies_logger.log("using periphery for GPIO control", Loglevel.INFO)
        self._gpios: list[GPIO | None] = [None] * 200

    def init(self, gpio_mode=None):
        """Initialize GPIO library.

        pass on periphery
        """

    def deinit(self):
        """Deinitialize GPIO library.

        pass on periphery
        """

    def gpio_setup(
        self,
        pin: int,
        mode: GpioMode,
        initial: Gpio = Gpio.LOW,
        pull_up_down: GpioPUD = GpioPUD.PUD_OFF,
    ):
        """Setup GPIO pin."""
        mode_str = "out" if (mode == GpioMode.OUT) else "in"
        self._gpios[pin] = GPIO(pin, mode_str)

    def gpio_cleanup(self, pin: int):
        """Cleanup GPIO pin."""
        gpio = self._gpios[pin]
        if isinstance(gpio, GPIO):
            gpio.close()
            self._gpios[pin] = None

    def gpio_input(self, pin: int) -> int:
        """Read GPIO pin."""
        gpio = self._gpios[pin]
        if not isinstance(gpio, GPIO):
            raise RuntimeError(f"GPIO pin {pin} not configured")
        return gpio.read()

    def gpio_output(self, pin: int, value):
        """Write GPIO pin."""
        gpio = self._gpios[pin]
        if not isinstance(gpio, GPIO):
            raise RuntimeError(f"GPIO pin {pin} not configured")
        gpio.write(bool(value))

    def gpio_pwm_setup(self, pin: int, frequency: int = 10, duty_cycle: int = 0):
        """Setup PWM."""
        raise NotImplementedError

    def gpio_pwm_set_frequency(self, pin: int, frequency: int):
        """Set PWM frequency."""
        raise NotImplementedError

    def gpio_pwm_set_duty_cycle(self, pin: int, duty_cycle: int):
        """Set PWM duty cycle.

        Args:
            pin (int): pin number
            duty_cycle (int): duty cycle in percent (0-100)
        """
        raise NotImplementedError

    def gpio_add_event_detect(self, pin: int, callback: types.FunctionType):
        """Add event detect."""
        raise NotImplementedError

    def gpio_remove_event_detect(self, pin: int):
        """Remove event detect."""
        raise NotImplementedError
