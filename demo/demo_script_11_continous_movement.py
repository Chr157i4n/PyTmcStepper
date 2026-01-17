"""
test file for testing basic movement
"""

import time
from tmc_driver import (
    Tmc2209,
    Loglevel,
    Board,
    tmc_gpio,
    MovementAbsRel,
    TmcEnableControlPin,
    TmcMotionControlStepDir,
)
from tmc_driver.com import TmcComUart


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
    TmcEnableControlPin(21),
    TmcMotionControlStepDir(16, 20),
    TmcComUart(UART_PORT.get(tmc_gpio.BOARD, "/dev/serial0")),
    loglevel=Loglevel.DEBUG,
)


# -----------------------------------------------------------------------
# set the loglevel of the libary (currently only printed)
# set whether the movement should be relative or absolute
# both optional
# -----------------------------------------------------------------------
tmc.tmc_logger.loglevel = Loglevel.DEBUG
tmc.movement_abs_rel = MovementAbsRel.ABSOLUTE


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
# set the max Speed and Speed in fullsteps
# -----------------------------------------------------------------------
tmc.tmc_mc.max_speed_fullstep = 200
tmc.tmc_mc.speed_fullstep = 100


# -----------------------------------------------------------------------
# activate the motor current output
# -----------------------------------------------------------------------
tmc.set_motor_enabled(True)


# -----------------------------------------------------------------------
# move the motor 4 seconds
# -----------------------------------------------------------------------
time_start = time.time()

while time.time() < time_start + 4:
    tmc.tmc_mc.run_speed()


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
