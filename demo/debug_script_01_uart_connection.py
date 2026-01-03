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
tmc = Tmc2209(None, None, None)


UART_PORT = {
    Board.RASPBERRY_PI: "/dev/serial0",
    Board.RASPBERRY_PI5: "/dev/ttyAMA0",
    Board.NVIDIA_JETSON: "/dev/ttyTHS1",
}
tmc.tmc_com = TmcComUart(UART_PORT.get(tmc_gpio.BOARD, "/dev/serial0"))

tmc.tmc_com.tmc_logger = tmc.tmc_logger
tmc.tmc_com.init()


# -----------------------------------------------------------------------
# set the loglevel of the libary (currently only printed)
# set whether the movement should be relative or absolute
# both optional
# -----------------------------------------------------------------------
tmc.tmc_logger.loglevel = Loglevel.DEBUG
tmc.movement_abs_rel = MovementAbsRel.ABSOLUTE


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
