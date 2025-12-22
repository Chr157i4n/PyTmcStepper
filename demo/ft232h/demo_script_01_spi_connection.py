"""
test file for testing the UART connection
"""

import time
try:
    from src.tmc_driver.tmc_2240 import *
    from src.tmc_driver.com._tmc_com_spi_ftdi import *
    from src.tmc_driver import tmc_gpio
except ModuleNotFoundError:
    from tmc_driver.tmc_2240 import *
    from tmc_driver.com._tmc_com_spi_ftdi import *
    from tmc_driver import tmc_gpio
from pyftdi.spi import SpiController


print("---")
print("SCRIPT START")
print("---")


#-----------------------------------------------------------------------
# initiate the Tmc2240 class
# use your pins for pin_en, pin_step, pin_dir here
#-----------------------------------------------------------------------
spi_ctrl = SpiController()
spi_ctrl.configure('ftdi://ftdi:232h/1', cs_count=1)
spi_port = spi_ctrl.get_port(cs=0, freq=1E6, mode=0)
gpio_port = spi_ctrl.get_gpio()
tmc_gpio.tmc_gpio = tmc_gpio.FtdiWrapper(gpio_port)

tmc = Tmc2240(None, None, TmcComSpiFtdi(spi_port), loglevel=Loglevel.DEBUG)



#-----------------------------------------------------------------------
# set the loglevel of the libary (currently only printed)
# set whether the movement should be relative or absolute
# both optional
#-----------------------------------------------------------------------
tmc.tmc_logger.loglevel = Loglevel.DEBUG
tmc.movement_abs_rel = MovementAbsRel.ABSOLUTE





#-----------------------------------------------------------------------
# these functions change settings in the TMC register
#-----------------------------------------------------------------------
tmc.set_direction_reg(False)
tmc.set_current(300)
tmc.set_interpolation(True)
tmc.set_spreadcycle(False)
tmc.set_microstepping_resolution(2)


print("---\n---")





#-----------------------------------------------------------------------
# these functions read and print the current settings in the TMC register
#-----------------------------------------------------------------------
tmc.read_ioin()
tmc.read_chopconf()
tmc.read_drv_status()
tmc.read_gconf()

print("---\n---")

# you can either read the register like this:
# unfortunately you need to know the names of the register for this method
# because they are generated at runtime and therefore not available in the IDE as a suggestion
tmc.adcv_supply_ain.read()
tmc.adcv_supply_ain.log(tmc.tmc_logger)

tmc.adc_temp.read()
tmc.adc_temp.log(tmc.tmc_logger)

print("---\n---")

# or use the wrapper functions in the Tmc2240 class
print(f"Temperature:\t{tmc.get_temperature()} °C")
print(f"VSupply:\t{tmc.get_vsupply()} V")

print("---\n---")


#-----------------------------------------------------------------------
# deinitiate the Tmc2240 class
#-----------------------------------------------------------------------
del tmc

print("---")
print("SCRIPT FINISHED")
print("---")
