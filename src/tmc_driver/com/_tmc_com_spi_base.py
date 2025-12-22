#pylint: disable=unused-import
#pylint: disable=wildcard-import
#pylint: disable=unused-wildcard-import
"""
TmcComSpiBase - Abstract base class for SPI communication
This class contains no hardware-specific imports (no spidev, no pyftdi)
"""

from abc import abstractmethod
from ._tmc_com import *
from .._tmc_exceptions import TmcComException, TmcDriverException


class TmcComSpiBase(TmcCom):
    """TmcComSpiBase

    Abstract base class for SPI communication with TMC drivers.
    This class contains common SPI functionality without hardware-specific imports.
    Subclasses must implement the actual SPI transfer methods.
    """

    def __init__(self,
                 mtr_id: int = 0
                 ):
        """constructor

        Args:
            tmc_logger (class): TMCLogger class
            mtr_id (int, optional): driver address [0-3]. Defaults to 0.
        """
        super().__init__(mtr_id)

        self.spi = None  # To be set by subclass

        self._r_frame = [0x55, 0, 0, 0, 0]
        self._w_frame = [0x55, 0, 0, 0, 0]


    @abstractmethod
    def init(self):
        """init - to be implemented by subclass"""


    @abstractmethod
    def deinit(self):
        """destructor - to be implemented by subclass"""


    @abstractmethod
    def _spi_transfer(self, data: list) -> list:
        """Perform SPI transfer - to be implemented by subclass

        Args:
            data: Data to send

        Returns:
            Received data
        """


    def read_reg(self, addr: int):
        """reads the registry on the TMC with a given address.
        returns the binary value of that register

        Args:
            addr (int): HEX, which register to read
        Returns:
            int: register value
            Dict: flags
        """
        self._w_frame = [addr, 0x00, 0x00, 0x00, 0x00]
        dummy_data = [0x00, 0x00, 0x00, 0x00, 0x00]

        self._spi_transfer(self._w_frame)
        rtn = self._spi_transfer(dummy_data)

        flags = {
            "reset_flag":      rtn[0] >> 0 & 0x01,
            "driver_error":    rtn[0] >> 1 & 0x01,
            "sg2":             rtn[0] >> 2 & 0x01,
            "standstill":      rtn[0] >> 3 & 0x01
        }

        if flags["reset_flag"]:
            raise TmcDriverException("TMC224X: reset detected")
        if flags["driver_error"]:
            raise TmcDriverException("TMC224X: driver error detected")
        if flags["sg2"]:
            self._tmc_logger.log("TMC stallguard2 flag is set", Loglevel.MOVEMENT)
        if flags["standstill"]:
            self._tmc_logger.log("TMC standstill flag is set", Loglevel.MOVEMENT)

        return rtn[1:], flags


    def read_int(self, addr: int, tries: int = 10):
        """this function tries to read the registry of the TMC 10 times
        if a valid answer is returned, this function returns it as an integer

        Args:
            addr (int): HEX, which register to read
            tries (int): how many tries, before error is raised (Default value = 10)
        Returns:
            int: register value
            Dict: flags
        """
        data, flags = self.read_reg(addr)
        return int.from_bytes(bytes(data), 'big'), flags


    def write_reg(self, addr: int, val: int):
        """this function can write a value to the register of the tmc
        1. use read_int to get the current setting of the TMC
        2. then modify the settings as wished
        3. write them back to the driver with this function

        Args:
            addr (int): HEX, which register to write
            val (int): value for that register
        """
        self._w_frame[0] = addr | 0x80  # set write bit

        self._w_frame[1] = 0xFF & (val >> 24)
        self._w_frame[2] = 0xFF & (val >> 16)
        self._w_frame[3] = 0xFF & (val >> 8)
        self._w_frame[4] = 0xFF & val

        self._spi_transfer(self._w_frame)


    def write_reg_check(self, addr: int, val: int, tries: int = 10):
        """IFCNT is disabled in SPI mode. Therefore, no check is possible.
        This only calls the write_reg function

        Args:
            addr: HEX, which register to write
            val: value for that register
            tries: how many tries, before error is raised (Default value = 10)
        """
        self.write_reg(addr, val)

    def flush_serial_buffer(self):
        """this function clear the communication buffers of the Raspberry Pi"""


    def handle_error(self):
        """error handling"""
        if self.error_handler_running:
            return
        self.error_handler_running = True
        self._tmc_registers["gstat"].read()
        self._tmc_registers["gstat"].log(self.tmc_logger)
        self._tmc_registers["gstat"].check()
        raise TmcDriverException("TMC220X: unknown error detected")


    def test_com(self, addr):
        """test com connection

        Args:
            addr (int):  HEX, which register to test
        """
        del addr  # addr is not used here
        self._tmc_registers["ioin"].read()
        self._tmc_registers["ioin"].log(self.tmc_logger)
        if self._tmc_registers["ioin"].data_int == 0:
            self._tmc_logger.log("No answer from TMC received", Loglevel.ERROR)
            return False
        if self._tmc_registers["ioin"].version < 0x40:
            self._tmc_logger.log("No correct Version from TMC received", Loglevel.ERROR)
            return False
        return True
