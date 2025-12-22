#pylint: disable=too-many-instance-attributes
#pylint: disable=too-many-arguments
#pylint: disable=too-many-positional-arguments
"""
TmcComSpiPico - SPI communication for MicroPython

Uses the machine.SPI interface available on RP2040 and similar boards.
"""

# Detect if we're running on MicroPython
from machine import SPI, Pin  # pylint: disable=import-error
from ._tmc_com_spi_base import TmcComSpiBase



class TmcComSpiMicroPython(TmcComSpiBase):
    """SPI Communication class for MicroPython

    RP2040 SPI Pins (default):
    - SPI0: SCK=GP18, MOSI=GP19, MISO=GP16
    - SPI1: SCK=GP10, MOSI=GP11, MISO=GP8

    TMC2240 uses SPI Mode 3: CPOL=1, CPHA=1
    """

    def __init__(self,
                 spi_id=0,
                 cs_pin=17,
                 sck_pin=18,
                 mosi_pin=19,
                 miso_pin=16,
                 baudrate=1000000,
                 mtr_id=0
                 ):
        """Initialize SPI communication

        Args:
            spi_id: SPI bus ID (0 or 1)
            cs_pin: Chip select GPIO pin
            sck_pin: SPI clock GPIO pin
            mosi_pin: MOSI GPIO pin
            miso_pin: MISO GPIO pin
            baudrate: SPI clock frequency (default 1MHz)
            mtr_id: Motor/driver ID (default 0)
            tmc_logger: Logger instance (optional)
        """
        super().__init__(mtr_id)

        self._spi_id = spi_id
        self._cs_pin = cs_pin
        self._sck_pin = sck_pin
        self._mosi_pin = mosi_pin
        self._miso_pin = miso_pin
        self._baudrate = baudrate

        self._spi = None
        self._cs = None


    def init(self):
        """Initialize SPI hardware"""
        # TMC2240 uses SPI Mode 3: CPOL=1, CPHA=1
        self._spi = SPI(self._spi_id, baudrate=self._baudrate, polarity=1, phase=1,
                        sck=Pin(self._sck_pin), mosi=Pin(self._mosi_pin), miso=Pin(self._miso_pin))

        # Setup CS pin (active low)
        self._cs = Pin(self._cs_pin, Pin.OUT, value=1)


    def deinit(self):
        """Deinitialize SPI hardware"""
        if self._spi is not None:
            self._spi.deinit()
            self._spi = None
        self._cs = None


    def _spi_transfer(self, data):
        """Perform SPI transfer

        Args:
            data: List of bytes to send

        Returns:
            List of received bytes
        """
        tx_data = bytes(data)
        rx_data = bytearray(len(data))

        self._cs.value(0)  # CS low
        self._spi.write_readinto(tx_data, rx_data)
        self._cs.value(1)  # CS high

        return list(rx_data)
