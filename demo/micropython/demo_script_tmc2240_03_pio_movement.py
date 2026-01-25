"""
Demo file for PIO-based step control on Raspberry Pi Pico (RP2040/RP2350)

This demo uses the PIO (Programmable I/O) hardware to generate
precise step pulses for the stepper motor driver.

The PIO provides more accurate timing compared to software-based
stepping, especially at higher speeds.
"""

from tmc_driver.tmc_2240 import Tmc2240
from tmc_driver.tmc_logger import Loglevel
from tmc_driver.motion_control._tmc_mc import MovementAbsRel
from tmc_driver.enable_control._tmc_ec_pin import TmcEnableControlPin
from tmc_driver.motion_control._tmc_mc_step_pio import TmcMotionControlStepPio
from tmc_driver.com._tmc_com_uart_micropython import TmcComUartMicroPython

# from tmc_driver.com._tmc_com_spi_micropython import TmcComSpiMicroPython

print("---")
print("SCRIPT START - PIO Motion Control Demo")
print("---")

# -----------------------------------------------------------------------
# initiate the Tmc2209 class
# use your pins for pin_en, pin_step, pin_dir here
# The PIO-based motion control uses the RP2040/RP2350 PIO hardware
# for precise step pulse generation
# -----------------------------------------------------------------------
# PIO parameters:
#   pio_id: PIO block (0 or 1)
#   sm_id: State machine within PIO block (0-3)
# -----------------------------------------------------------------------
tmc = Tmc2240(
    TmcEnableControlPin(18),
    TmcMotionControlStepPio(
        pin_step=17,
        pin_dir=16,
        pio_id=0,
        sm_id=0,
    ),
    TmcComUartMicroPython(1, 4, 5),
    driver_address=7,
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
# set the Acceleration and maximal Speed in fullsteps
# -----------------------------------------------------------------------
tmc.acceleration_fullstep = 1000
tmc.max_speed_fullstep = 250


# -----------------------------------------------------------------------
# activate the motor current output
# -----------------------------------------------------------------------
tmc.set_motor_enabled(True)
print("BEFORE MOVEMENT")
print(f"Temperature:\t{tmc.get_temperature()} °C")
print(f"VSupply:\t{tmc.get_vsupply()} V")


# -----------------------------------------------------------------------
# move the motor 1 revolution
# -----------------------------------------------------------------------
tmc.run_to_position_fullsteps(200)  # move to position 200 (fullsteps)
tmc.run_to_position_fullsteps(0)  # move to position 0

tmc.run_to_position_fullsteps(
    200, MovementAbsRel.RELATIVE
)  # move 200 fullsteps forward
tmc.run_to_position_fullsteps(
    -200, MovementAbsRel.RELATIVE
)  # move 200 fullsteps backward

tmc.run_to_position_steps(400)  # move to position 400 (µsteps)
tmc.run_to_position_steps(0)  # move to position 0

tmc.run_to_position_revolutions(1)  # move 1 revolution forward
tmc.run_to_position_revolutions(0)  # move 1 revolution backward


# -----------------------------------------------------------------------
# deactivate the motor current output
# -----------------------------------------------------------------------
print("AFTER MOVEMENT")
print(f"Temperature:\t{tmc.get_temperature()} °C")
print(f"VSupply:\t{tmc.get_vsupply()} V")
tmc.set_motor_enabled(False)

print("---\n---")


# -----------------------------------------------------------------------
# deinitiate the Tmc2209 class
# -----------------------------------------------------------------------
del tmc

print("---")
print("SCRIPT FINISHED")
print("---")
