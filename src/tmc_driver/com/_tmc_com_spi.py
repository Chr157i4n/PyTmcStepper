#pylint: disable=import-error
#pylint: disable=broad-exception-caught
#pylint: disable=unused-import
#pylint: disable=wildcard-import
#pylint: disable=unused-wildcard-import
#pylint: disable=too-few-public-methods
#pylint: disable=too-many-arguments
#pylint: disable=too-many-positional-arguments
"""
TmcComSpi stepper driver spi module
"""

import spidev
from ._tmc_com import *
from .._tmc_exceptions import TmcComException, TmcDriverException

# class MockSpiDev:
#     """MockSpiDev"""

#     def SpiDev(self):
#         """SpiDev"""

# try:
#     import spidev
# except ImportError:
#     print("spidev not found. Using MockSpiDev")
#     spidev = MockSpiDev()




class TmcComSpi(TmcCom):
    """TmcComSpi

    this class is used to communicate with the TMC via SPI
    it can be used to change the settings of the TMC.
    like the current or the microsteppingmode
    """

    spi = spidev.SpiDev()
    _spi_bus: int
    _spi_dev: int
    _spi_speed: int



    def __init__(self,
                 spi_bus,
                 spi_dev,
                 spi_speed:int = 8000000,
                 mtr_id:int = 0,
                 tmc_logger = None
                 ):
        """constructor

        Args:
            _tmc_logger (class): TMCLogger class
            mtr_id (int, optional): driver address [0-3]. Defaults to 0.
        """
        super().__init__(mtr_id, tmc_logger)

        self._spi_bus = spi_bus
        self._spi_dev = spi_dev
        self._spi_speed = spi_speed

        self._r_frame = [0x55, 0, 0, 0, 0]
        self._w_frame = [0x55, 0, 0, 0, 0]


    def init(self):
        """init"""
        try:
            self.spi.open(self._spi_bus, self._spi_dev)
        except Exception as e:
            self._tmc_logger.log(f"Error opening SPI: {e}", Loglevel.ERROR)
            errnum = e.args[0]
            if errnum == 2:
                self._tmc_logger.log(f"SPI Device {self._spi_dev} on Bus {self._spi_bus} does not exist.", Loglevel.ERROR)
                self._tmc_logger.log("You need to activate the SPI interface with \"sudo raspi-config\"", Loglevel.ERROR)
            raise SystemExit from e

        self.spi.max_speed_hz = self._spi_speed
        self.spi.mode = 0b11
        self.spi.lsbfirst = False


    def __del__(self):
        self.deinit()


    def deinit(self):
        """destructor"""


    def read_reg(self, addr:hex):
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

        self.spi.xfer2(self._w_frame)
        rtn = self.spi.xfer2(dummy_data)

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


    def read_int(self, addr:hex, tries:int = 10):
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
        return int.from_bytes(data, byteorder='big', signed=False), flags


    def write_reg(self, addr:hex, val:int):
        """this function can write a value to the register of the tmc
        1. use read_int to get the current setting of the TMC
        2. then modify the settings as wished
        3. write them back to the driver with this function

        Args:
            addr (int): HEX, which register to write
            val (int): value for that register
        """
        self._w_frame[0] = addr | 0x80  # set write bit

        self._w_frame[1] = 0xFF & (val>>24)
        self._w_frame[2] = 0xFF & (val>>16)
        self._w_frame[3] = 0xFF & (val>>8)
        self._w_frame[4] = 0xFF & val
        # self.w_frame[7] = compute_crc8_atm(self.w_frame[:-1])

        self.spi.xfer2(self._w_frame)


    def write_reg_check(self, addr:hex, val:int, tries:int=10):
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
        self._tmc_registers["ioin"].read()
        self._tmc_registers["ioin"].log(self.tmc_logger)
        if self._tmc_registers["ioin"].data_int == 0:
            self._tmc_logger.log("No answer from TMC received", Loglevel.ERROR)
            return False
        if self._tmc_registers["ioin"].version < 0x40:
            self._tmc_logger.log("No correct Version from TMC received", Loglevel.ERROR)
            return False
        return True
