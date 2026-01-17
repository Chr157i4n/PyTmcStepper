"""
test file for testing basic movement
"""

from tmc_driver import (
    Tmc2209,
    Loglevel,
    TmcEnableControlPin,
    TmcMotionControlStepDir,
    MovementAbsRel,
)
from tmc_driver.com import TmcComUartMicroPython


print("---")
print("SCRIPT START")
print("---")

# -----------------------------------------------------------------------
# initiate the Tmc2240 class
# use your pins for pin_en, pin_step, pin_dir here
# -----------------------------------------------------------------------
tmc = Tmc2209(
    TmcEnableControlPin(18),
    TmcMotionControlStepDir(17, 16),
    TmcComUartMicroPython(1, 4, 5),
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
# set the Acceleration and maximal Speed in fullsteps
# -----------------------------------------------------------------------
tmc.acceleration_fullstep = 1000
tmc.max_speed_fullstep = 100


# -----------------------------------------------------------------------
# activate the motor current output
# -----------------------------------------------------------------------
tmc.set_motor_enabled(True)


# -----------------------------------------------------------------------
# Home in negative dir and then set position to 0
# Afterwards home in positive dir
# Finally move to the middle position
# -----------------------------------------------------------------------

result = tmc.do_homing(
    diag_pin=22,
    revolutions=-1,
    threshold=50,
)

if result:
    print("Endstop 1 found")
    tmc.reset_position()

    result = tmc.do_homing(
        diag_pin=22,
        revolutions=1,
        threshold=50,
        cb_success=None,
    )

    if result:
        print("Endstop 2 found")

        middle = tmc.current_pos_fullstep // 2
        tmc.run_to_position_fullsteps(middle, MovementAbsRel.ABSOLUTE)

    else:
        print("Endstop 2 not found")

else:
    print("Endstop 1 not found")


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
