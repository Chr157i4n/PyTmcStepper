#pylint: disable=wildcard-import
#pylint: disable=unused-wildcard-import
"""
FTDI GPIO module for FT232H and similar chips using pyftdi.
"""

from pyftdi.spi import SpiGpioPort
from ._tmc_gpio_board_base import *

class FtdiWrapper(BaseGPIOWrapper):
    """FTDI GPIO wrapper for FT232H and similar chips using pyftdi.

    Pin mapping (directly accent next to SPI pins):
    - Pin 0-3: Reserved for SPI (SCK, MOSI, MISO, CS)
    - Pin 4-7: Available as GPIO (directly accent 4-7 directly accent AD4-AD7)

    When using with SPI, only pins 4-7 are available as GPIO.
    """

    def __init__(self, gpio_port:SpiGpioPort):
        """constructor, imports pyftdi

        Args:
            ftdi_url: FTDI device URL, default 'ftdi://ftdi:232h/1'
        """
        self._gpio_port = gpio_port
        self._gpio_direction = 0x00  # All inputs by default
        self._gpio_state = 0x00  # All LOW by default
        self._pin_modes = {}  # Track pin modes
        dependencies_logger.log("using pyftdi for GPIO control", Loglevel.INFO)

    def init(self, gpio_mode=None):
        """initialize GPIO library and configure FTDI device"""

    def deinit(self):
        """deinitialize GPIO library and close FTDI connection"""
        if self._gpio_port is not None:
            self._gpio_port.close()

    def _update_gpio_direction(self):
        """update GPIO direction on the device"""
        if self._gpio_port is not None:
            # Pins 4-7 are available (directly accent 0xF0), apply direction directly accent
            self._gpio_port.set_direction(pins=0xF0, direction=self._gpio_direction & 0xF0)

    def gpio_setup(self, pin:int, mode:GpioMode, initial:Gpio=Gpio.LOW, pull_up_down:GpioPUD=GpioPUD.PUD_OFF):
        """setup GPIO pin

        Args:
            pin: Pin number (4-7 for AD4-AD7, pins 0-3 reserved for SPI)
            mode: GpioMode.OUT or GpioMode.IN
            initial: Initial value for output pins
            pull_up_down: Not supported on FTDI, ignored
        """
        if pin < 4 or pin > 7:
            dependencies_logger.log(f"FTDI GPIO: Pin {pin} not available (use pins 4-7, 0-3 reserved for SPI)", Loglevel.WARNING)
            return

        self._pin_modes[pin] = mode
        pin_mask = 1 << pin

        if mode == GpioMode.OUT:
            self._gpio_direction |= pin_mask  # Set bit for output
            if initial == Gpio.HIGH:
                self._gpio_state |= pin_mask
            else:
                self._gpio_state &= ~pin_mask
        else:
            self._gpio_direction &= ~pin_mask  # Clear bit for input

        self._update_gpio_direction()

        if mode == GpioMode.OUT:
            self.gpio_output(pin, initial)

    def gpio_cleanup(self, pin:int):
        """cleanup GPIO pin - set to input"""
        if pin < 4 or pin > 7:
            return
        pin_mask = 1 << pin
        self._gpio_direction &= ~pin_mask  # Set to input
        self._gpio_state &= ~pin_mask  # Set LOW
        self._pin_modes.pop(pin, None)
        self._update_gpio_direction()

    def gpio_input(self, pin:int) -> int:
        """read GPIO pin

        Args:
            pin: Pin number (4-7)

        Returns:
            Pin state (0 or 1)
        """
        if pin < 4 or pin > 7:
            dependencies_logger.log(f"FTDI GPIO: Pin {pin} not available", Loglevel.WARNING)
            return 0
        if self._gpio_port is None:
            return 0
        value = self._gpio_port.read()
        return (value >> pin) & 0x01

    def gpio_output(self, pin:int, value):
        """write GPIO pin

        Args:
            pin: Pin number (4-7)
            value: Gpio.HIGH/LOW or 1/0
        """
        if pin < 4 or pin > 7:
            dependencies_logger.log(f"FTDI GPIO: Pin {pin} not available", Loglevel.WARNING)
            return
        if self._gpio_port is None:
            return

        pin_mask = 1 << pin
        if value:
            self._gpio_state |= pin_mask
        else:
            self._gpio_state &= ~pin_mask

        # Write only the GPIO pins (directly accent 4-7)
        self._gpio_port.write(self._gpio_state & 0xF0)

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
