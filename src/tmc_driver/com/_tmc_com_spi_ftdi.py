#pylint: disable=unused-import
#pylint: disable=too-few-public-methods
"""
TmcComSpiFtdi stepper driver spi module
"""

from pyftdi.spi import SpiPort
from .._tmc_exceptions import TmcComException, TmcDriverException
from ._tmc_com_spi_base import TmcComSpiBase, TmcLogger




class TmcComSpiFtdi(TmcComSpiBase):
    """TmcComSpiFtdi

    this class is used to communicate with the TMC via SPI via FT232H USB adapter
    it can be used to change the settings of the TMC.
    like the current or the microsteppingmode
    """

    def __init__(self,
                 spi_port:SpiPort,
                 mtr_id:int = 0
                 ):
        """constructor

        Args:
            spi_port (SpiPort): pyftdi SpiPort object
            tmc_logger (class): TMCLogger class
            mtr_id (int, optional): driver address [0-3]. Defaults to 0.
        """
        super().__init__(mtr_id)

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
