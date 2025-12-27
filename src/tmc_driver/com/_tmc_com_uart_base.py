# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# pylint: disable=unused-import
"""
TmcComUartBase - Abstract base class for UART communication
This class contains no hardware-specific imports (no serial/pyserial)
"""

from abc import abstractmethod
from ._tmc_com import *
from .._tmc_exceptions import TmcComException, TmcDriverException


class TmcComUartBase(TmcCom):
    """TmcComUartBase

    Abstract base class for UART communication with TMC drivers.
    This class contains common UART functionality without hardware-specific imports.
    Subclasses must implement the actual UART transfer methods.
    """

    def __init__(self, driver_address: int = 0):
        """constructor

        Args:
            driver_address (int, optional): driver address. Defaults to 0.
        """
        super().__init__(driver_address)

        self.ser = None  # To be set by subclass

        self.r_frame = [0x55, 0, 0, 0]
        self.w_frame = [0x55, 0, 0, 0, 0, 0, 0, 0]

    @abstractmethod
    def init(self):
        """init - to be implemented by subclass"""

    @abstractmethod
    def deinit(self):
        """destructor - to be implemented by subclass"""

    @abstractmethod
    def _uart_write(self, data: list) -> int:
        """Write data to UART - to be implemented by subclass

        Args:
            data: Data to send

        Returns:
            Number of bytes written
        """

    @abstractmethod
    def _uart_read(self, length: int) -> bytes:
        """Read data from UART - to be implemented by subclass

        Args:
            length: Number of bytes to read

        Returns:
            Received data
        """

    @abstractmethod
    def _uart_flush(self):
        """Flush UART buffers - to be implemented by subclass"""

    def read_reg(self, addr: int) -> tuple[bytes, None]:
        """reads the registry on the TMC with a given address.
        returns the binary value of that register

        Args:
            addr (int): HEX, which register to read

        Returns:
            bytes: raw response
            Dict: flags (None for UART)

        Raises:
            TmcComException: if serial is not initialized or port is closed
        """
        if self.ser is None:
            raise TmcComException("Cannot read reg, serial is not initialized")
        if not self.ser.is_open:
            raise TmcComException("Cannot read reg, serial port is closed")

        self._uart_flush()

        self.r_frame[1] = self.driver_address
        self.r_frame[2] = addr
        self.r_frame[3] = compute_crc8_atm(self.r_frame[:-1])

        rtn = self._uart_write(self.r_frame)
        if rtn != len(self.r_frame):
            raise TmcComException("Error in UART write")

        # adjust per baud and hardware. Sequential reads without some delay fail.
        time.sleep(self.communication_pause)

        rtn = self._uart_read(12)

        time.sleep(self.communication_pause)

        return rtn, None

    def read_int(self, addr: int, tries: int = 10) -> tuple[int, None]:
        """this function tries to read the registry of the TMC 10 times
        if a valid answer is returned, this function returns it as an integer

        Args:
            addr (int): HEX, which register to read
            tries (int): how many tries, before error is raised (Default value = 10)

        Returns:
            int: register value
            Dict: flags

        Raises:
            TmcComException: if serial is not initialized or port is closed
        """
        if self.ser is None:
            raise TmcComException("Cannot read reg, serial is not initialized")
        if not self.ser.is_open:
            raise TmcComException("Cannot read reg, serial port is closed")

        while True:
            tries -= 1
            rtn, flags = self.read_reg(addr)
            if rtn is None:
                return -1, None
            rtn_data = rtn[7:11]
            not_zero_count = len([elem for elem in rtn if elem != 0])

            if len(rtn) < 12 or not_zero_count == 0:
                self._tmc_logger.log(
                    f"""UART Communication Error:
                                    {len(rtn_data)} data bytes |
                                    {len(rtn)} total bytes""",
                    Loglevel.ERROR,
                )
            elif rtn[11] != compute_crc8_atm(rtn[4:11]):
                self._tmc_logger.log(
                    "UART Communication Error: CRC MISMATCH", Loglevel.ERROR
                )
            else:
                break

            if tries <= 0:
                raise TmcComException(
                    f"after 10 tries not valid answer; addr: {addr}; rtn: {rtn}"
                )

        val = struct.unpack(">i", rtn_data)[0]
        return val, flags

    def write_reg(self, addr: int, val: int) -> bool:
        """this function can write a value to the register of the tmc
        1. use read_int to get the current setting of the TMC
        2. then modify the settings as wished
        3. write them back to the driver with this function

        Args:
            addr (int): HEX, which register to write
            val (int): value for that register

        Returns:
            True if write was successful

        Raises:
            TmcComException: if serial is not initialized or port is closed
        """
        if self.ser is None:
            raise TmcComException("Cannot write reg, serial is not initialized")
        if not self.ser.is_open:
            raise TmcComException("Cannot write reg, serial port is closed")

        self._uart_flush()

        self.w_frame[1] = self.driver_address
        self.w_frame[2] = addr | 0x80  # set write bit

        self.w_frame[3] = 0xFF & (val >> 24)
        self.w_frame[4] = 0xFF & (val >> 16)
        self.w_frame[5] = 0xFF & (val >> 8)
        self.w_frame[6] = 0xFF & val

        self.w_frame[7] = compute_crc8_atm(self.w_frame[:-1])

        rtn = self._uart_write(self.w_frame)
        if rtn != len(self.w_frame):
            self._tmc_logger.log("Err in write", Loglevel.ERROR)
            return False

        time.sleep(self.communication_pause)

        return True

    def write_reg_check(self, addr: int, val: int, tries: int = 10) -> bool:
        """this function als writes a value to the register of the TMC
        but it also checks if the writing process was successfully by checking
        the InterfaceTransmissionCounter before and after writing

        Args:
            addr: HEX, which register to write
            val: value for that register
            tries: how many tries, before error is raised (Default value = 10)

        Returns:
            True if write was successful

        Raises:
            TmcComException: if IFCNT register is not set or write fails after retries
        """
        ifcnt = self.get_register("ifcnt")
        if ifcnt is None:
            raise TmcComException("TMC register IFCNT not available")

        ifcnt.read()
        ifcnt1 = ifcnt.ifcnt

        if ifcnt1 == 255:
            ifcnt1 = -1

        while True:
            self.write_reg(addr, val)
            tries -= 1
            ifcnt.read()
            ifcnt2 = ifcnt.ifcnt
            if ifcnt2 >= ifcnt1:
                return True
            self._tmc_logger.log("writing not successful!", Loglevel.ERROR)
            self._tmc_logger.log(f"ifcnt: {ifcnt1}, {ifcnt2}", Loglevel.DEBUG)
            if tries <= 0:
                raise TmcComException("after 10 tries writing not successful")

    def flush_serial_buffer(self):
        """this function clear the communication buffers"""
        if self.ser is None:
            return
        self._uart_flush()

    def test_com(self):
        """test UART connection

        Returns:
            bool: True if communication is OK, False otherwise

        Raises:
            TmcComException: if TMC register IOIN not available or serial not initialized
        """
        if self.ser is None:
            raise TmcComException("Cannot test com, serial is not initialized")
        if not self.ser.is_open:
            raise TmcComException("Cannot test com, serial port is closed")

        ioin = self.get_register("ioin")
        if ioin is None:
            raise TmcComException("TMC register IOIN not available")

        self.r_frame[1] = self.driver_address
        self.r_frame[2] = ioin.addr
        self.r_frame[3] = compute_crc8_atm(self.r_frame[:-1])

        rtn = self._uart_write(self.r_frame)
        if rtn != len(self.r_frame):
            self._tmc_logger.log("Err in write", Loglevel.ERROR)
            return False

        snd = bytes(self.r_frame)

        rtn = self._uart_read(12)
        self._tmc_logger.log(
            f"received {len(rtn)} bytes; {len(rtn)*8} bits", Loglevel.DEBUG
        )
        self._tmc_logger.log(f"hex: {rtn.hex()}", Loglevel.DEBUG)

        self.tmc_logger.log(f"length snd: {len(snd)}", Loglevel.DEBUG)
        self.tmc_logger.log(f"length rtn: {len(rtn)}", Loglevel.DEBUG)

        self.tmc_logger.log("complete messages:", Loglevel.DEBUG)
        self.tmc_logger.log(str(snd.hex()), Loglevel.DEBUG)
        self.tmc_logger.log(str(rtn.hex()), Loglevel.DEBUG)

        self.tmc_logger.log("just the first 4 bytes:", Loglevel.DEBUG)
        self.tmc_logger.log(str(snd[0:4].hex()), Loglevel.DEBUG)
        self.tmc_logger.log(str(rtn[0:4].hex()), Loglevel.DEBUG)

        status = True

        if len(rtn) == 12:
            self.tmc_logger.log(
                """the Raspberry Pi received the sent
                                bytes and the answer from the TMC""",
                Loglevel.DEBUG,
            )
        elif len(rtn) == 4:
            self.tmc_logger.log(
                "the Raspberry Pi received only the sent bytes", Loglevel.ERROR
            )
            status = False
        elif len(rtn) == 0:
            self.tmc_logger.log(
                "the Raspberry Pi did not receive anything", Loglevel.ERROR
            )
            status = False
        else:
            self.tmc_logger.log(
                f"the Raspberry Pi received an unexpected amount of bytes: {len(rtn)}",
                Loglevel.ERROR,
            )
            status = False

        if snd[0:4] == rtn[0:4]:
            self.tmc_logger.log(
                """the Raspberry Pi received exactly the bytes it has send.
                        the first 4 bytes are the same""",
                Loglevel.DEBUG,
            )
        else:
            self.tmc_logger.log(
                """the Raspberry Pi did not received the bytes it has send.
                        the first 4 bytes are different""",
                Loglevel.DEBUG,
            )
            status = False

        if status:
            ioin.read()

            if ioin.version < 0x21:
                self._tmc_logger.log(
                    f"No correct Version from TMC received: {ioin.version}",
                    Loglevel.ERROR,
                )
                status = False

        self.tmc_logger.log("---")
        if status:
            self.tmc_logger.log("UART connection: OK", Loglevel.INFO)
        else:
            self.tmc_logger.log("UART connection: not OK", Loglevel.ERROR)

        self.tmc_logger.log("---")

        return status
