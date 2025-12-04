#pylint: disable=import-error
#pylint: disable=broad-exception-caught
#pylint: disable=unused-import
#pylint: disable=wildcard-import
#pylint: disable=unused-wildcard-import
#pylint: disable=too-few-public-methods
#pylint: disable=too-many-arguments
#pylint: disable=too-many-positional-arguments
"""
TmcComSpiFtdi stepper driver spi module
"""

from pyftdi.spi import *
from ._tmc_com import *
from .._tmc_exceptions import TmcComException, TmcDriverException
from ._tmc_com_spi_base import TmcComSpiBase




class TmcComSpiFtdi(TmcComSpiBase):
    """TmcComSpiFtdi

    this class is used to communicate with the TMC via SPI via FT232H USB adapter
    it can be used to change the settings of the TMC.
    like the current or the microsteppingmode
    """

    def __init__(self,
                 spi_port:SpiPort,
                 mtr_id:int = 0,
                 tmc_logger = None
                 ):
        """constructor

        Args:
            spi_port (SpiPort): pyftdi SpiPort object
            tmc_logger (class): TMCLogger class
            mtr_id (int, optional): driver address [0-3]. Defaults to 0.
        """
        super().__init__(mtr_id, tmc_logger)

        self.spi = spi_port


    def init(self):
        """init - SPI port is already configured via pyftdi"""


    def __del__(self):
        self.deinit()


    def deinit(self):
        """destructor"""


    def _spi_transfer(self, data: list) -> list:
        """Perform SPI transfer using pyftdi

        Args:
            data: Data to send

        Returns:
            Received data
        """
        return list(self.spi.exchange(bytes(data), duplex=True))
