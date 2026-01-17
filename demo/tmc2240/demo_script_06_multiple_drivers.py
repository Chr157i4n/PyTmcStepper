# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
"""
test file for testing multiple drivers via one UART connection
"""

from tmc_driver import (
    Tmc2209,
    Tmc2240,
    Board,
    tmc_gpio,
    Loglevel,
    MovementAbsRel,
    TmcEnableControlPin,
    TmcMotionControlStepDir,
)
from tmc_driver.com._tmc_com_uart import *
from tmc_driver.com._tmc_com_spi import *

print("---")
print("SCRIPT START")
print("---")


# -----------------------------------------------------------------------
# initiate the Tmc2240 class
# use your pins for pin_en, pin_step, pin_dir here
# -----------------------------------------------------------------------
UART_PORT = {
    Board.RASPBERRY_PI: "/dev/serial0",
    Board.RASPBERRY_PI5: "/dev/ttyAMA0",
    Board.NVIDIA_JETSON: "/dev/ttyTHS1",
}

tmc1 = Tmc2209(
    TmcEnableControlPin(21),
    TmcMotionControlStepDir(16, 20),
    TmcComUart(UART_PORT.get(tmc_gpio.BOARD, "/dev/serial0")),
    loglevel=Loglevel.DEBUG,
)

tmc2 = Tmc2240(
    TmcEnableControlPin(26),
    TmcMotionControlStepDir(13, 19),
    TmcComSpi(0, 0),
    loglevel=Loglevel.DEBUG,
)


# -----------------------------------------------------------------------
# set the loglevel of the libary (currently only printed)
# set whether the movement should be relative or absolute
# both optional
# -----------------------------------------------------------------------
tmc1.tmc_logger.loglevel = Loglevel.DEBUG
tmc1.movement_abs_rel = MovementAbsRel.ABSOLUTE

tmc2.tmc_logger.loglevel = Loglevel.DEBUG
tmc2.movement_abs_rel = MovementAbsRel.ABSOLUTE


# -----------------------------------------------------------------------
# these functions read and print the current settings in the TMC register
# -----------------------------------------------------------------------

print("---")
print("IOIN tmc1")
print("---")
tmc1.read_register("ioin")

print("---\n---")


print("---")
print("IOIN tmc2")
print("---")
tmc2.read_register("ioin")

print("---\n---")


# -----------------------------------------------------------------------
# deinitiate the Tmc2240 class
# -----------------------------------------------------------------------
tmc1.set_motor_enabled(False)
tmc2.set_motor_enabled(False)
del tmc1
del tmc2

print("---")
print("SCRIPT FINISHED")
print("---")
