# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
"""
debug file for debuging the UART connection
"""

from tmc_driver.tmc_2209 import *
from tmc_driver.com._tmc_com_uart import *


print("---")
print("SCRIPT START")
print("---")


# -----------------------------------------------------------------------
# initiate the Tmc2209 class
# use your pins for pin_en, pin_step, pin_dir here
# -----------------------------------------------------------------------
tmc = Tmc2209(None, None, None, loglevel=Loglevel.DEBUG)


UART_PORT = {
    Board.RASPBERRY_PI: "/dev/serial0",
    Board.RASPBERRY_PI5: "/dev/ttyAMA0",
    Board.NVIDIA_JETSON: "/dev/ttyTHS1",
}
tmc.tmc_com = TmcComUart(UART_PORT.get(tmc_gpio.BOARD, "/dev/serial0"))

tmc.tmc_com.tmc_logger = tmc.tmc_logger
tmc.tmc_com.init()


# -----------------------------------------------------------------------
# these functions read and print the current settings in the TMC register
# -----------------------------------------------------------------------
print("---\n---")

tmc.test_com()


print("---\n---")


# -----------------------------------------------------------------------
# deinitiate the Tmc2209 class
# -----------------------------------------------------------------------
del tmc

print("---")
print("SCRIPT FINISHED")
print("---")
