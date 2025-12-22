#pylint: disable=broad-exception-caught
#pylint: disable=unused-import
"""
TmcComUart stepper driver uart module
"""

import serial
from ._tmc_com_uart_base import TmcComUartBase, TmcLogger, Loglevel
from .._tmc_exceptions import TmcComException, TmcDriverException



class TmcComUart(TmcComUartBase):
    """TmcComUart

    this class is used to communicate with the TMC via UART using pyserial
    it can be used to change the settings of the TMC.
    like the current or the microsteppingmode
    """

    def __init__(self,
                 serialport: str,
                 baudrate: int = 115200,
                 mtr_id: int = 0
                 ):
        """constructor

        Args:
            tmc_logger (class): TMCLogger class
            serialport (string): serialport path
            baudrate (int): baudrate
            mtr_id (int, optional): driver address [0-3]. Defaults to 0.
        """
        super().__init__(mtr_id)

        self.ser = serial.Serial()

        if serialport is None:
            return

        self.ser.port = serialport
        self.ser.baudrate = baudrate

    def init(self):
        """init"""
        try:
            self.ser.open()
        except Exception as e:
            errnum = e.args[0]
            self._tmc_logger.log(f"SERIAL ERROR: {e}")
            if errnum == 2:
                self._tmc_logger.log(f""""{self.ser.serialport} does not exist.
                      You need to activate the serial port with \"sudo raspi-config\"""", Loglevel.ERROR)
                raise SystemExit from e

            if errnum == 13:
                self._tmc_logger.log("""you have no permission to use the serial port.
                                    You may need to add your user to the dialout group
                                    with \"sudo usermod -a -G dialout pi\"""", Loglevel.ERROR)
                raise SystemExit from e

        # adjust per baud and hardware. Sequential reads without some delay fail.
        self.communication_pause = 500 / self.ser.baudrate

        if self.ser is None:
            return

        self.ser.BYTESIZES = 1
        self.ser.PARITIES = serial.PARITY_NONE
        self.ser.STOPBITS = 1

        # adjust per baud and hardware. Sequential reads without some delay fail.
        self.ser.timeout = 20000 / self.ser.baudrate

        self._uart_flush()

    def __del__(self):
        self.deinit()

    def deinit(self):
        """destructor"""
        if self.ser is not None and isinstance(self.ser, serial.Serial):
            self.ser.close()

    def _uart_write(self, data: list) -> int:
        """Write data to UART using pyserial

        Args:
            data: Data to send

        Returns:
            Number of bytes written
        """
        return self.ser.write(data)

    def _uart_read(self, length: int) -> bytes:
        """Read data from UART using pyserial

        Args:
            length: Number of bytes to read

        Returns:
            Received data
        """
        return self.ser.read(length)

    def _uart_flush(self):
        """Flush UART buffers"""
        if self.ser is not None:
            self.ser.reset_output_buffer()
            self.ser.reset_input_buffer()
