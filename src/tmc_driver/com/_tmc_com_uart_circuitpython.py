# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
# pylint: disable=too-few-public-methods
"""
TmcComUartCircuitPython - UART communication for CircuitPython

Uses the busio.UART interface for single-wire UART communication.
"""

import time
import busio  # pylint: disable=import-error
from ._tmc_com_uart_base import TmcComUartBase
from .._tmc_exceptions import TmcComException


class TmcComUartCircuitPython(TmcComUartBase):
    """UART Communication class for CircuitPython

    Example usage:
        import board
        from tmc_driver.com import TmcComUartCircuitPython

        uart_com = TmcComUartCircuitPython(
            tx=board.TX,
            rx=board.RX,
            baudrate=115200
        )

    For single-wire UART, connect TX to the TMC UART pin through a 1k resistor.
    """

    def __init__(self, tx, rx, baudrate=115200, timeout=1.0):
        """Initialize UART communication

        Args:
            tx: TX board pin (e.g., board.TX or board.GP0)
            rx: RX board pin (e.g., board.RX or board.GP1)
            baudrate: UART baudrate (default 115200)
            timeout: Read timeout in seconds (default 1.0)
        """
        super().__init__()

        self._tx_pin = tx
        self._rx_pin = rx
        self._baudrate = baudrate
        self._timeout = timeout

        self._uart = None

    def init(self):
        """Initialize UART hardware"""
        self._uart = busio.UART(
            tx=self._tx_pin,
            rx=self._rx_pin,
            baudrate=self._baudrate,
            timeout=self._timeout,
        )
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
        if self._uart is None:
            raise TmcComException("UART not initialized")

        data_bytes = bytes(data)
        self._uart.write(data_bytes)

        time.sleep(0.01)  # Small delay to ensure data is sent

        return len(data_bytes)

    def _uart_read(self, length):
        """Read data from UART

        Args:
            length: Number of bytes to read

        Returns:
            Bytes read or empty bytes if timeout
        """
        if self._uart is None:
            raise TmcComException("UART not initialized")

        # Wait a bit for data to arrive
        time.sleep(0.01)  # 10ms in seconds (CircuitPython uses seconds)

        result = self._uart.read(length)
        if result is None:
            return bytes()
        return bytes(result)

    def _uart_flush(self):
        """Flush UART receive buffer"""
        if self._uart is None:
            raise TmcComException("UART not initialized")

        # Reset input buffer
        self._uart.reset_input_buffer()


class _FakeSerial:
    """Fake serial object for compatibility with base class"""

    def __init__(self, uart):
        """Constructor for fake serial object"""
        self._uart = uart
        self.is_open = True

    def close(self):
        """Close the fake serial port"""
        self.is_open = False
