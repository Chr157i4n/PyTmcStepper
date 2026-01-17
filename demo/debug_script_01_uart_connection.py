# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
"""
debug file for debuging the UART connection
"""

from tmc_driver import TmcLogger, Loglevel, Board, tmc_gpio
from tmc_driver.com._tmc_com_uart import *
from tmc_driver.tmc_2209 import Ioin


print("---")
print("SCRIPT START")
print("---")


# -----------------------------------------------------------------------
# initiate the TmcCom class
# -----------------------------------------------------------------------
UART_PORT = {
    Board.RASPBERRY_PI: "/dev/serial0",
    Board.RASPBERRY_PI5: "/dev/ttyAMA0",
    Board.NVIDIA_JETSON: "/dev/ttyTHS1",
}
tmc_com = TmcComUart(UART_PORT.get(tmc_gpio.BOARD, "/dev/serial0"))

tmc_com.tmc_logger = TmcLogger(Loglevel.DEBUG)
tmc_com.driver_address = 0
tmc_com.init()


# -----------------------------------------------------------------------
# these functions read and print the current settings in the TMC register
# -----------------------------------------------------------------------
print("---\n---")

tmc_com.test_com(Ioin(tmc_com))


print("---\n---")


# -----------------------------------------------------------------------
# deinitiate the TmcCom class
# -----------------------------------------------------------------------
del tmc_com

print("---")
print("SCRIPT FINISHED")
print("---")
