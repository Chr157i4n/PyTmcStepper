# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
"""
TmcComSpiCircuitPython - SPI communication for CircuitPython

Uses the busio.SPI interface available on CircuitPython boards.
"""

import busio  # pylint: disable=import-error
import digitalio  # pylint: disable=import-error
from ._tmc_com_spi_base import TmcComSpiBase
from .._tmc_exceptions import TmcComException


class TmcComSpiCircuitPython(TmcComSpiBase):
    """SPI Communication class for CircuitPython

    Example usage:
        import board
        from tmc_driver.com import TmcComSpiCircuitPython
        
        spi_com = TmcComSpiCircuitPython(
            cs=board.D17,
            clock=board.SCK,
            mosi=board.MOSI,
            miso=board.MISO,
            baudrate=1000000
        )

    TMC2240/TMC5160 uses SPI Mode 3: CPOL=1, CPHA=1
    """

    def __init__(
        self,
        cs,
        clock,
        mosi,
        miso,
        baudrate=1000000,
    ):
        """Initialize SPI communication

        Args:
            cs: Chip select board pin (e.g., board.D17)
            clock: SPI clock board pin (e.g., board.SCK)
            mosi: MOSI board pin (e.g., board.MOSI)
            miso: MISO board pin (e.g., board.MISO)
            baudrate: SPI clock frequency in Hz (default 1MHz)
        """
        super().__init__()

        self._cs_pin = cs
        self._clock_pin = clock
        self._mosi_pin = mosi
        self._miso_pin = miso
        self._baudrate = baudrate

        self._spi = None
        self._cs = None

    def init(self):
        """Initialize SPI hardware"""
        # Create SPI bus
        self._spi = busio.SPI(
            clock=self._clock_pin,
            MOSI=self._mosi_pin,
            MISO=self._miso_pin
        )

        # Setup CS pin (active low)
        self._cs = digitalio.DigitalInOut(self._cs_pin)
        self._cs.direction = digitalio.Direction.OUTPUT
        self._cs.value = True  # CS high (inactive)

    def deinit(self):
        """Deinitialize SPI hardware"""
        if self._spi is not None:
            self._spi.deinit()
            self._spi = None
        if self._cs is not None:
            self._cs.deinit()
            self._cs = None

    def _spi_transfer(self, data):
        """Perform SPI transfer

        Args:
            data: List of bytes to send

        Returns:
            List of received bytes
        """
        if self._spi is None or self._cs is None:
            raise TmcComException("SPI not initialized")

        tx_data = bytes(data)
        rx_data = bytearray(len(data))

        # Lock the SPI bus and perform transfer
        while not self._spi.try_lock():
            pass
        
        try:
            # Configure SPI for TMC (Mode 3: CPOL=1, CPHA=1)
            self._spi.configure(
                baudrate=self._baudrate,
                polarity=1,
                phase=1,
                bits=8
            )
            
            # Perform transfer with CS control
            self._cs.value = False  # CS low (active)
            self._spi.write_readinto(tx_data, rx_data)
            self._cs.value = True  # CS high (inactive)
        finally:
            self._spi.unlock()

        return list(rx_data)
