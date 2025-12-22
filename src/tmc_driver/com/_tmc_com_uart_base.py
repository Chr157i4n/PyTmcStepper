#pylint: disable=wildcard-import
#pylint: disable=unused-wildcard-import
#pylint: disable=unused-import
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

    def __init__(self,
                 mtr_id: int = 0
                 ):
        """constructor

        Args:
            tmc_logger (class): TMCLogger class
            mtr_id (int, optional): driver address [0-3]. Defaults to 0.
        """
        super().__init__(mtr_id)

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

    def read_reg(self, addr: int):
        """reads the registry on the TMC with a given address.
        returns the binary value of that register

        Args:
            addr (int): HEX, which register to read
        Returns:
            bytes: raw response
            Dict: flags (None for UART)
        """
        if self.ser is None:
            self._tmc_logger.log("Cannot read reg, serial is not initialized", Loglevel.ERROR)
            return None, None
        if not self.ser.is_open:
            self._tmc_logger.log("Cannot read reg, serial port is closed", Loglevel.ERROR)
            return None, None

        self._uart_flush()

        self.r_frame[1] = self.mtr_id
        self.r_frame[2] = addr
        self.r_frame[3] = compute_crc8_atm(self.r_frame[:-1])

        rtn = self._uart_write(self.r_frame)
        if rtn != len(self.r_frame):
            self._tmc_logger.log("Err in write", Loglevel.ERROR)
            return None, None

        # adjust per baud and hardware. Sequential reads without some delay fail.
        time.sleep(self.communication_pause)

        rtn = self._uart_read(12)

        time.sleep(self.communication_pause)

        return rtn, None

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
        if self.ser is None:
            self._tmc_logger.log("Cannot read int, serial is not initialized", Loglevel.ERROR)
            return -1, None

        while True:
            tries -= 1
            rtn, flags = self.read_reg(addr)
            if rtn is None:
                return -1, None
            rtn_data = rtn[7:11]
            not_zero_count = len([elem for elem in rtn if elem != 0])

            if len(rtn) < 12 or not_zero_count == 0:
                self._tmc_logger.log(f"""UART Communication Error:
                                    {len(rtn_data)} data bytes |
                                    {len(rtn)} total bytes""", Loglevel.ERROR)
            elif rtn[11] != compute_crc8_atm(rtn[4:11]):
                self._tmc_logger.log("UART Communication Error: CRC MISMATCH", Loglevel.ERROR)
            else:
                break

            if tries <= 0:
                self._tmc_logger.log("after 10 tries not valid answer", Loglevel.ERROR)
                self._tmc_logger.log(f"addr:\t{addr}", Loglevel.DEBUG)
                self._tmc_logger.log(f"rtn:\t{rtn}", Loglevel.DEBUG)
                self.handle_error()
                return -1, None

        val = struct.unpack(">i", rtn_data)[0]
        return val, flags

    def write_reg(self, addr: int, val: int):
        """this function can write a value to the register of the tmc
        1. use read_int to get the current setting of the TMC
        2. then modify the settings as wished
        3. write them back to the driver with this function

        Args:
            addr (int): HEX, which register to write
            val (int): value for that register
        """
        if self.ser is None:
            self._tmc_logger.log("Cannot write reg, serial is not initialized", Loglevel.ERROR)
            return False
        if not self.ser.is_open:
            self._tmc_logger.log("Cannot read reg, serial port is closed", Loglevel.ERROR)
            return None, None

        self._uart_flush()

        self.w_frame[1] = self.mtr_id
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

    def write_reg_check(self, addr: int, val: int, tries: int = 10):
        """this function als writes a value to the register of the TMC
        but it also checks if the writing process was successfully by checking
        the InterfaceTransmissionCounter before and after writing

        Args:
            addr: HEX, which register to write
            val: value for that register
            tries: how many tries, before error is raised (Default value = 10)
        """
        if self.ser is None:
            self._tmc_logger.log("Cannot write reg check, serial is not initialized", Loglevel.ERROR)
            return False

        self._tmc_registers["ifcnt"].read()
        ifcnt1 = self._tmc_registers["ifcnt"].ifcnt

        if ifcnt1 == 255:
            ifcnt1 = -1

        while True:
            self.write_reg(addr, val)
            tries -= 1
            self._tmc_registers["ifcnt"].read()
            ifcnt2 = self._tmc_registers["ifcnt"].ifcnt
            if ifcnt1 >= ifcnt2:
                self._tmc_logger.log("writing not successful!", Loglevel.ERROR)
                self._tmc_logger.log(f"ifcnt: {ifcnt1}, {ifcnt2}", Loglevel.DEBUG)
            else:
                return True
            if tries <= 0:
                self._tmc_logger.log("after 10 tries no valid write access", Loglevel.ERROR)
                self.handle_error()
                return False

    def flush_serial_buffer(self):
        """this function clear the communication buffers"""
        if self.ser is None:
            return
        self._uart_flush()

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
        """test UART connection

        Args:
            addr (int):  HEX, which register to test
        """
        if self.ser is None:
            self._tmc_logger.log("Cannot test UART, serial is not initialized", Loglevel.ERROR)
            return False

        self._uart_flush()

        self.r_frame[1] = self.mtr_id
        self.r_frame[2] = addr
        self.r_frame[3] = compute_crc8_atm(self.r_frame[:-1])

        rtn = self._uart_write(self.r_frame)
        if rtn != len(self.r_frame):
            self._tmc_logger.log("Err in write", Loglevel.ERROR)
            return False

        snd = bytes(self.r_frame)

        rtn = self._uart_read(12)
        self._tmc_logger.log(f"received {len(rtn)} bytes; {len(rtn)*8} bits", Loglevel.DEBUG)
        self._tmc_logger.log(f"hex: {rtn.hex()}", Loglevel.DEBUG)
        rtn_bin = format(int(rtn.hex(), 16), f"0>{len(rtn)*8}b")
        self._tmc_logger.log(f"bin: {rtn_bin}", Loglevel.DEBUG)

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
            self.tmc_logger.log("""the Raspberry Pi received the sent
                                bytes and the answer from the TMC""", Loglevel.DEBUG)
        elif len(rtn) == 4:
            self.tmc_logger.log("the Raspberry Pi received only the sent bytes",
                                Loglevel.ERROR)
            status = False
        elif len(rtn) == 0:
            self.tmc_logger.log("the Raspberry Pi did not receive anything",
                                Loglevel.ERROR)
            status = False
        else:
            self.tmc_logger.log(f"the Raspberry Pi received an unexpected amount of bytes: {len(rtn)}",
                                Loglevel.ERROR)
            status = False

        if snd[0:4] == rtn[0:4]:
            self.tmc_logger.log("""the Raspberry Pi received exactly the bytes it has send.
                        the first 4 bytes are the same""", Loglevel.DEBUG)
        else:
            self.tmc_logger.log("""the Raspberry Pi did not received the bytes it has send.
                        the first 4 bytes are different""", Loglevel.DEBUG)
            status = False

        self.tmc_logger.log("---")
        if status:
            self.tmc_logger.log("UART connection: OK", Loglevel.INFO)
        else:
            self.tmc_logger.log("UART connection: not OK", Loglevel.ERROR)

        self.tmc_logger.log("---")

        return status
