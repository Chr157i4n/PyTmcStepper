# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
"""
test file for testing basic movement
"""
from pyftdi.spi import SpiController
from tmc_driver.tmc_5160 import *
from tmc_driver.com._tmc_com_spi_ftdi import *
from tmc_driver import tmc_gpio

print("---")
print("SCRIPT START")
print("---")


# -----------------------------------------------------------------------
# initiate the Tmc2240 class
# use your pins for pin_en, pin_step, pin_dir here
# -----------------------------------------------------------------------
spi_ctrl = SpiController()
spi_ctrl.configure("ftdi://ftdi:232h/1")
spi_port = spi_ctrl.get_port(cs=0, freq=1e6, mode=0)
gpio_port = spi_ctrl.get_gpio()
tmc_gpio.tmc_gpio = tmc_gpio.FtdiWrapper(gpio_port)

tmc = Tmc5160(
    TmcEnableControlPin(5),
    TmcMotionControlIntRampGenerator(),
    TmcComSpiFtdi(spi_port),
    loglevel=Loglevel.DEBUG,
)


# -----------------------------------------------------------------------
# set the loglevel of the libary (currently only printed)
# set whether the movement should be relative or absolute
# both optional
# -----------------------------------------------------------------------
tmc.tmc_logger.loglevel = Loglevel.MOVEMENT
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
tmc.set_motor_enabled(False)

print("---\n---")


# -----------------------------------------------------------------------
# deinitiate the Tmc2240 class
# -----------------------------------------------------------------------
del tmc

print("---")
print("SCRIPT FINISHED")
print("---")
