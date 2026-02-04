# pylint: disable=broad-exception-caught
# pylint: disable=unused-import
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
"""TmcComSpi stepper driver spi module."""

import spidev
from ._tmc_com_spi_base import TmcComSpiBase, TmcLogger, Loglevel
from .._tmc_exceptions import TmcComException, TmcDriverException


class TmcComSpi(TmcComSpiBase):
    """TmcComSpi.

    this class is used to communicate with the TMC via SPI it can be
    used to change the settings of the TMC. like the current or the
    microsteppingmode
    """

    def __init__(
        self,
        spi_bus: int,
        spi_dev: int,
        spi_speed: int = 8000000,
    ):
        """constructor.

        Args:
            spi_bus (int): SPI bus number
            spi_dev (int): SPI device number
            spi_speed (int, optional): SPI speed in Hz. Defaults to 8000000.
        """
        super().__init__()

        self.spi = spidev.SpiDev()

        self._spi_bus = spi_bus
        self._spi_dev = spi_dev
        self._spi_speed = spi_speed

    def init(self):
        """init."""
        try:
            self.spi.open(self._spi_bus, self._spi_dev)
        except Exception as e:
            self._tmc_logger.log(f"Error opening SPI: {e}", Loglevel.ERROR)
            errnum = e.args[0]
            if errnum == 2:
                self._tmc_logger.log(
                    f"SPI Device {self._spi_dev} on Bus {self._spi_bus} does not exist.",
                    Loglevel.ERROR,
                )
                self._tmc_logger.log(
                    'You need to activate the SPI interface with "sudo raspi-config"',
                    Loglevel.ERROR,
                )
            raise SystemExit from e

        self.spi.max_speed_hz = self._spi_speed
        self.spi.mode = 0b11
        self.spi.lsbfirst = False

    def __del__(self):
        """Destructor."""
        self.deinit()

    def deinit(self):
        """Destructor."""

    def _spi_transfer(self, data: list) -> list:
        """Perform SPI transfer using spidev.

        Args:
            data: Data to send

        Returns:
            Received data
        """
        return self.spi.xfer2(data)
