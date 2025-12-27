# pylint: disable=unused-import
"""
TmcCom stepper driver communication module
"""

import time
import struct
from abc import abstractmethod
from .._tmc_logger import TmcLogger, Loglevel
from .._tmc_exceptions import TmcComException


def compute_crc8_atm(datagram, initial_value=0):
    """this function calculates the crc8 parity bit

    Args:
        datagram (list): datagram
        initial_value (int): initial value (Default value = 0)
    """
    crc = initial_value
    # Iterate bytes in data
    for byte in datagram:
        # Iterate bits in byte
        for _ in range(0, 8):
            if (crc >> 7) ^ (byte & 0x01):
                crc = ((crc << 1) ^ 0x07) & 0xFF
            else:
                crc = (crc << 1) & 0xFF
            # Shift to next bit
            byte = byte >> 1
    return crc


class IfcntRegister:
    """Interface for IFCNT register - defines only what tmc_com needs to know"""

    # pylint: disable=too-few-public-methods

    ifcnt: int

    def read(self):
        """Read the register"""


class TmcCom:
    """TmcCom"""

    @property
    def tmc_logger(self) -> TmcLogger:
        """get the tmc_logger"""
        return self._tmc_logger

    @tmc_logger.setter
    def tmc_logger(self, tmc_logger: TmcLogger):
        """set the tmc_logger"""
        self._tmc_logger = tmc_logger

    def __init__(self, driver_address: int = 0):
        """constructor

        Args:
            driver_address (int, optional): driver address. Defaults to 0.
        """
        self._tmc_logger: TmcLogger
        self.driver_address = driver_address
        self.ifcnt: IfcntRegister | None = None
        self.communication_pause: int = 0
        self.error_handler_running: bool = False

    @abstractmethod
    def init(self):
        """init communication"""

    @abstractmethod
    def deinit(self):
        """deinit communication"""

    @abstractmethod
    def read_reg(self, addr: int) -> tuple[int, dict]:
        """reads the registry on the TMC with a given address.
        returns the binary value of that register

        Args:
            addr (int): HEX, which register to read
        Returns:
            int: register value
            Dict: flags
        """

    @abstractmethod
    def read_int(self, addr: int, tries: int = 10) -> tuple[int, dict]:
        """this function tries to read the registry of the TMC 10 times
        if a valid answer is returned, this function returns it as an integer

        Args:
            addr (int): HEX, which register to read
            tries (int): how many tries, before error is raised (Default value = 10)
        Returns:
            int: register value
            Dict: flags
        """

    @abstractmethod
    def write_reg(self, addr: int, val: int):
        """this function can write a value to the register of the tmc
        1. use read_int to get the current setting of the TMC
        2. then modify the settings as wished
        3. write them back to the driver with this function

        Args:
            addr (int): HEX, which register to write
            val (int): value for that register
        """

    @abstractmethod
    def write_reg_check(self, addr: int, val: int, tries: int = 10):
        """this function als writes a value to the register of the TMC
        but it also checks if the writing process was successfully by checking
        the InterfaceTransmissionCounter before and after writing

        Args:
            addr: HEX, which register to write
            val: value for that register
            tries: how many tries, before error is raised (Default value = 10)
        """

    @abstractmethod
    def flush_serial_buffer(self):
        """this function clear the communication buffers of the Raspberry Pi"""

    @abstractmethod
    def test_com(self, addr):
        """test com connection

        Args:
            addr (int):  HEX, which register to test
        """
