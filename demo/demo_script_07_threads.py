"""
test file for testing movement of motors with threads
"""

import time
from tmc_driver import (
    Tmc2209,
    Loglevel,
    Board,
    tmc_gpio,
    MovementPhase,
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

tmc1 = Tmc2209(
    TmcEnableControlPin(21),
    TmcMotionControlStepDir(16, 20),
    TmcComUart(UART_PORT.get(tmc_gpio.BOARD, "/dev/serial0")),
    loglevel=Loglevel.DEBUG,
)

tmc_driverlist = [tmc1]


# -----------------------------------------------------------------------
# set the loglevel of the libary (currently only printed)
# set whether the movement should be relative or absolute
# both optional
# -----------------------------------------------------------------------
tmc1.tmc_logger.loglevel = Loglevel.DEBUG
tmc1.movement_abs_rel = MovementAbsRel.ABSOLUTE


# -----------------------------------------------------------------------
# these functions change settings in the TMC register
# -----------------------------------------------------------------------
for tmc in tmc_driverlist:
    tmc.set_direction_reg(False)
    tmc.set_current_rms(300)
    tmc.set_interpolation(True)
    tmc.set_spreadcycle(False)
    tmc.set_microstepping_resolution(2)
    tmc.set_internal_rsense(False)
    tmc.set_motor_enabled(True)

    tmc.acceleration_fullstep = 1000
    tmc.max_speed_fullstep = 250


print("---\n---")


# -----------------------------------------------------------------------
# run part
# -----------------------------------------------------------------------

# move 4000 steps forward
tmc1.tmc_mc.run_to_position_steps_threaded(4000, MovementAbsRel.RELATIVE)

time.sleep(1)
tmc1.tmc_mc.stop()  # stop the movement after 1 second

tmc1.tmc_mc.wait_for_movement_finished_threaded()

# move 4000 steps backward
tmc1.tmc_mc.run_to_position_steps_threaded(-4000, MovementAbsRel.RELATIVE)


# while the motor is still moving
while tmc1.movement_phase != MovementPhase.STANDSTILL:
    # print the current movement phase
    print(tmc1.movement_phase)
    time.sleep(0.02)

tmc1.tmc_mc.wait_for_movement_finished_threaded()


print("---\n---")


# -----------------------------------------------------------------------
# deinitiate the Tmc2209 class
# -----------------------------------------------------------------------
tmc1.set_motor_enabled(False)
del tmc1


print("---")
print("SCRIPT FINISHED")
print("---")
