"""
Demo file for testing the UART connection
"""

import board
from tmc_driver import Tmc2209, Loglevel, TmcEnableControlPin, TmcMotionControlStepDir
from tmc_driver.com import TmcComUartCircuitPython


print("---")
print("SCRIPT START")
print("---")


# -----------------------------------------------------------------------
# initiate the Tmc2209 class
# use your pins for pin_en, pin_step, pin_dir here
# -----------------------------------------------------------------------
tmc = Tmc2209(
    TmcEnableControlPin(board.GP18),
    TmcMotionControlStepDir(board.GP17, board.GP16),
    TmcComUartCircuitPython(tx=board.GP4, rx=board.GP5),
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
