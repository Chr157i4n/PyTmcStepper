"""
Demo file for basic movement
"""

import board
from tmc_driver.tmc_2209 import Tmc2209
from tmc_driver.tmc_logger import Loglevel
from tmc_driver.enable_control._tmc_ec_pin import TmcEnableControlPin
from tmc_driver.motion_control._tmc_mc_step_dir import TmcMotionControlStepDir
from tmc_driver.com._tmc_com_uart_circuitpython import TmcComUartCircuitPython


print("---")
print("SCRIPT START")
print("---")

# -----------------------------------------------------------------------
# initiate the Tmc2240 class
# use your pins for pin_en, pin_step, pin_dir here
# -----------------------------------------------------------------------
tmc = Tmc2209(
    TmcEnableControlPin(board.GP18),
    TmcMotionControlStepDir(board.GP17, board.GP16),
    TmcComUartCircuitPython(tx=board.GP4, rx=board.GP5),
    loglevel=Loglevel.DEBUG,
)


# -----------------------------------------------------------------------
# set the loglevel of the libary (currently only printed)
# set whether the movement should be relative or absolute
# both optional
# -----------------------------------------------------------------------
tmc.tmc_logger.loglevel = Loglevel.DEBUG

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
# this function test whether the connection of the DIR, STEP and EN pin
# between Raspberry Pi and TMC driver is working
# -----------------------------------------------------------------------
tmc.test_dir_step_en()

print("---\n---")


# -----------------------------------------------------------------------
# deactivate the motor current output
# -----------------------------------------------------------------------
tmc.set_motor_enabled(False)

print("---\n---")


# -----------------------------------------------------------------------
# deinitiate the Tmc2209 class
# -----------------------------------------------------------------------
del tmc

print("---")
print("SCRIPT FINISHED")
print("---")
