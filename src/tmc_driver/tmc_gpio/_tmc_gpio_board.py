#pylint: disable=unnecessary-pass
#pylint: disable=abstract-method
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
from ._tmc_gpio_board_base import *


class BaseRPiGPIOWrapper(BaseGPIOWrapper):
    """RPI.GPIO base wrapper"""

    def __init__(self):
        """constructor"""
        self._gpios_pwm = [None] * 200

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


class MockGPIOWrapper(BaseRPiGPIOWrapper):
    """Mock.GPIO wrapper"""

    def __init__(self):
        """constructor, imports Mock.GPIO"""
        super().__init__()
        self.GPIO = import_module('Mock.GPIO')
        dependencies_logger.log("using Mock.GPIO for GPIO mocking", Loglevel.INFO)

class RPiGPIOWrapper(BaseRPiGPIOWrapper):
    """RPi.GPIO wrapper"""

    def __init__(self):
        """constructor, imports RPi.GPIO"""
        super().__init__()
        self.GPIO = import_module('RPi.GPIO')
        dependencies_logger.log("using RPi.GPIO for GPIO control", Loglevel.INFO)

class JetsonGPIOWrapper(BaseRPiGPIOWrapper):
    """Jetson.GPIO wrapper"""

    def __init__(self):
        """constructor, imports Jetson.GPIO"""
        super().__init__()
        self.GPIO = import_module('Jetson.GPIO')
        dependencies_logger.log("using Jetson.GPIO for GPIO control", Loglevel.INFO)

class OPiGPIOWrapper(BaseRPiGPIOWrapper):
    """OPi.GPIO wrapper"""

    def __init__(self):
        """constructor, imports OPi.GPIO"""
        super().__init__()
        self.GPIO = import_module('OPi.GPIO')
        dependencies_logger.log("using OPi.GPIO for GPIO control", Loglevel.INFO)

class GpiozeroWrapper(BaseGPIOWrapper):
    """gpiozero GPIO wrapper"""

    def __init__(self):
        """constructor, imports gpiozero"""
        self._gpios = [None] * 200
        self._gpios_pwm = [None] * 200
        self.gpiozero = import_module('gpiozero')
        dependencies_logger.log("using gpiozero for GPIO control", Loglevel.INFO)

    def init(self, gpio_mode=None):
        """initialize GPIO library. pass on gpiozero"""
        pass

    def deinit(self):
        """deinitialize GPIO library. pass on gpiozero"""
        pass

    def gpio_setup(self, pin:int, mode:GpioMode, initial:Gpio=Gpio.LOW, pull_up_down:GpioPUD=GpioPUD.PUD_OFF):
        """setup GPIO pin"""
        if mode == GpioMode.OUT:
            if self._gpios[pin] is None or self._gpios[pin].closed:
                self._gpios[pin] = self.gpiozero.DigitalOutputDevice(pin, initial_value =bool(initial))
        else:
            if self._gpios[pin] is None or self._gpios[pin].closed:
                self._gpios[pin] = self.gpiozero.DigitalInputDevice(pin)

    def gpio_cleanup(self, pin:int):
        """cleanup GPIO pin"""
        if self._gpios[pin] is not None:
            self._gpios[pin].close()
            self._gpios[pin] = None
        if self._gpios_pwm[pin] is not None:
            self._gpios_pwm[pin].close()
            self._gpios_pwm[pin] = None

    def gpio_input(self, pin:int) -> int:
        """read GPIO pin"""
        return self._gpios[pin].value

    def gpio_output(self, pin:int, value):
        """write GPIO pin"""
        self._gpios[pin].value = value

    def gpio_pwm_enable(self, pin:int, enable:bool):
        """switch to PWM"""
        if enable:
            if self._gpios[pin] is not None:
                self._gpios[pin] = None
                self._gpios_pwm[pin] = self.gpiozero.PWMOutputDevice(pin)
        else:
            if self._gpios_pwm[pin] is not None:
                self._gpios_pwm[pin] = None
                self._gpios[pin] = self.gpiozero.DigitalOutputDevice(pin)

    def gpio_pwm_setup(self, pin:int, frequency:int = 10, duty_cycle:int = 0):
        """setup PWM"""
        # self._gpios_pwm[pin] = self.gpiozero.PWMOutputDevice(pin)

    def gpio_pwm_set_frequency(self, pin:int, frequency:int):
        """set PWM frequency"""
        self._gpios_pwm[pin].frequency = frequency

    def gpio_pwm_set_duty_cycle(self, pin:int, duty_cycle:int):
        """set PWM duty cycle

        Args:
            pin (int): pin number
            duty_cycle (int): duty cycle in percent (0-100)
        """
        self._gpios_pwm[pin].value = duty_cycle/100

    def gpio_add_event_detect(self, pin:int, callback:types.FunctionType):
        """add event detect"""
        self._gpios[pin].when_activated = callback

    def gpio_remove_event_detect(self, pin:int):
        """remove event detect"""
        if self._gpios[pin].when_activated is not None:
            self._gpios[pin].when_activated = None

class peripheryWrapper(BaseGPIOWrapper):
    """periphery GPIO wrapper"""

    def __init__(self):
        """constructor, imports periphery"""
        self.periphery = import_module('periphery')
        dependencies_logger.log("using periphery for GPIO control", Loglevel.INFO)
        self._gpios = [None] * 200

    def init(self, gpio_mode=None):
        """initialize GPIO library. pass on periphery"""
        pass

    def deinit(self):
        """deinitialize GPIO library. pass on periphery"""
        pass

    def gpio_setup(self, pin:int, mode:GpioMode, initial:Gpio=Gpio.LOW, pull_up_down:GpioPUD=GpioPUD.PUD_OFF):
        """setup GPIO pin"""
        mode = 'out' if (mode == GpioMode.OUT) else 'in'
        self._gpios[pin] = self.periphery.GPIO(pin, mode)

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

class FtdiWrapper(BaseGPIOWrapper):
    """FTDI GPIO wrapper for FT232H and similar chips using pyftdi.

    Pin mapping (directly accent next to SPI pins):
    - Pin 0-3: Reserved for SPI (SCK, MOSI, MISO, CS)
    - Pin 4-7: Available as GPIO (directly accent 4-7 directly accent AD4-AD7)

    When using with SPI, only pins 4-7 are available as GPIO.
    """

    def __init__(self, gpio_port):
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
        pass


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
        """setup PWM - not natively supported on FTDI GPIO"""
        dependencies_logger.log("FTDI GPIO: Hardware PWM not supported", Loglevel.WARNING)

    def gpio_pwm_set_frequency(self, pin:int, frequency:int):
        """set PWM frequency - not supported"""
        dependencies_logger.log("FTDI GPIO: Hardware PWM not supported", Loglevel.WARNING)

    def gpio_pwm_set_duty_cycle(self, pin:int, duty_cycle:int):
        """set PWM duty cycle - not supported"""
        dependencies_logger.log("FTDI GPIO: Hardware PWM not supported", Loglevel.WARNING)

    def gpio_add_event_detect(self, pin:int, callback:types.FunctionType):
        """add event detect - not supported on FTDI"""
        dependencies_logger.log("FTDI GPIO: Event detection not supported", Loglevel.WARNING)

    def gpio_remove_event_detect(self, pin:int):
        """remove event detect - not supported"""
        pass
