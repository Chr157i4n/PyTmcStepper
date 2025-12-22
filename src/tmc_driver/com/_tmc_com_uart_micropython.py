#pylint: disable=too-many-instance-attributes
#pylint: disable=too-many-arguments
#pylint: disable=too-many-positional-arguments
#pylint: disable=too-few-public-methods
"""
TmcComUartPico - UART communication for MicroPython

Uses the machine.UART interface for single-wire UART communication.
"""

# Detect if we're running on MicroPython
import sys
import time
from machine import UART, Pin  # pylint: disable=import-error
from ._tmc_com_uart_base import TmcComUartBase

MICROPYTHON = sys.implementation.name == "micropython"


class TmcComUartMicroPython(TmcComUartBase):
    """UART Communication class for MicroPython

    RP2040 UART Pins (default):
    - UART0: TX=GP0, RX=GP1
    - UART1: TX=GP4, RX=GP5

    For single-wire UART, connect TX to the TMC UART pin through a 1k resistor.
    """

    def __init__(self,
                 uart_id=0,
                 tx_pin=0,
                 rx_pin=1,
                 baudrate=115200,
                 mtr_id=0
                 ):
        """Initialize UART communication

        Args:
            uart_id: UART bus ID (0 or 1)
            tx_pin: TX GPIO pin
            rx_pin: RX GPIO pin
            baudrate: UART baudrate
            mtr_id: Motor/slave address (0-3)
            tmc_logger: Logger instance (optional)
        """
        super().__init__(mtr_id)

        self._uart_id = uart_id
        self._tx_pin = tx_pin
        self._rx_pin = rx_pin
        self._baudrate = baudrate

        self._uart = None


    def init(self):
        """Initialize UART hardware"""
        self._uart = UART(self._uart_id, baudrate=self._baudrate,
                            tx=Pin(self._tx_pin), rx=Pin(self._rx_pin))
        # Create a fake serial object for compatibility with base class
        self.ser = _FakeSerial(self._uart)


    def deinit(self):
        """Deinitialize UART hardware"""
        if self._uart is not None:
            self._uart.deinit()
            self._uart = None
        self.ser = None


    def _uart_write(self, data):
        """Write data to UART

        Args:
            data: Bytes to write

        Returns:
            Number of bytes written
        """
        return self._uart.write(bytes(data))


    def _uart_read(self, length):
        """Read data from UART

        Args:
            length: Number of bytes to read

        Returns:
            Bytes read or empty bytes if timeout
        """
        # Wait a bit for data to arrive
        time.sleep_ms(10)   # pylint: disable=no-member

        result = self._uart.read(length)
        if result is None:
            return bytes()
        return result


    def _uart_flush(self):
        """Flush UART receive buffer"""
        # Read and discard any pending data
        while self._uart.any():
            self._uart.read()


class _FakeSerial:
    """Fake serial object for compatibility with base class"""

    def __init__(self, uart):
        """Constructor for fake serial object"""
        self._uart = uart
        self.is_open = True

    def close(self):
        """Close the fake serial port"""
        self.is_open = False
