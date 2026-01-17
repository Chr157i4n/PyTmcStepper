"""
test file for testing basic movement
"""

import time
from tmc_driver import (
    Tmc2240,
    Loglevel,
    MovementAbsRel,
    TmcEnableControlPin,
    TmcMotionControlStepDir,
)
from tmc_driver.com import TmcComSpi


print("---")
print("SCRIPT START")
print("---")


# -----------------------------------------------------------------------
# initiate the Tmc2240 class
# use your pins for pin_en, pin_step, pin_dir here
# -----------------------------------------------------------------------
tmc = Tmc2240(
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
tmc.set_toff(5)


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
# activate the motor current output
# -----------------------------------------------------------------------
tmc.set_motor_enabled(True)
print("BEFORE MOVEMENT")
print(f"Temperature:\t{tmc.get_temperature()} °C")
print(f"VSupply:\t{tmc.get_vsupply()} V")


# -----------------------------------------------------------------------
# move the motor
# -----------------------------------------------------------------------
tmc.tmc_mc.run_speed_pwm_fullstep(800)
time.sleep(5)
tmc.tmc_mc.run_speed_pwm_fullstep(0)
time.sleep(1)
tmc.tmc_mc.run_speed_pwm_fullstep(-800)
time.sleep(5)
tmc.tmc_mc.run_speed_pwm_fullstep(0)


# -----------------------------------------------------------------------
# deactivate the motor current output
# -----------------------------------------------------------------------
print("AFTER MOVEMENT")
print(f"Temperature:\t{tmc.get_temperature()} °C")
print(f"VSupply:\t{tmc.get_vsupply()} V")
tmc.set_motor_enabled(False)

print("---\n---")


# -----------------------------------------------------------------------
# deinitiate the Tmc2240 class
# -----------------------------------------------------------------------
del tmc

print("---")
print("SCRIPT FINISHED")
print("---")
