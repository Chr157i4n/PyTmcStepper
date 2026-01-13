# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
"""
test file for testing the UART connection
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
UART_PORT = {
    Board.RASPBERRY_PI: "/dev/serial0",
    Board.RASPBERRY_PI5: "/dev/ttyAMA0",
    Board.NVIDIA_JETSON: "/dev/ttyTHS1",
}

tmc = Tmc2209(
    None,
    None,
    TmcComUart(UART_PORT.get(tmc_gpio.BOARD, "/dev/serial0")),
    loglevel=Loglevel.DEBUG,
)


# -----------------------------------------------------------------------
# these functions change settings in the TMC register
# -----------------------------------------------------------------------
tmc.set_direction_reg(False)
tmc.set_current_rms(300)
tmc.set_interpolation(True)
tmc.set_spreadcycle(False)
tmc.set_microstepping_resolution(2)
tmc.set_internal_rsense(False)


print("---\n---")


# -----------------------------------------------------------------------
# these functions read and print the current settings in the TMC register
# -----------------------------------------------------------------------
tmc.read_register("ioin")
tmc.read_register("chopconf")
tmc.read_register("drvstatus")
tmc.read_register("gconf")

print("---\n---")


# -----------------------------------------------------------------------
# deinitiate the Tmc2209 class
# -----------------------------------------------------------------------
del tmc

print("---")
print("SCRIPT FINISHED")
print("---")
