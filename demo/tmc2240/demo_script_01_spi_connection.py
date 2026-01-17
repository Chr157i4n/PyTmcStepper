"""
Demo file for testing the SPI connection
"""

from tmc_driver import Tmc2240, Loglevel
from tmc_driver.com import TmcComSpi


print("---")
print("SCRIPT START")
print("---")


# -----------------------------------------------------------------------
# initiate the Tmc2240 class
# use your pins for pin_en, pin_step, pin_dir here
# -----------------------------------------------------------------------
tmc = Tmc2240(
    None,
    None,
    TmcComSpi(0, 0),
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


print("---\n---")


# -----------------------------------------------------------------------
# these functions read and print the current settings in the TMC register
# -----------------------------------------------------------------------
tmc.read_register("ioin")
tmc.read_register("chopconf")
tmc.read_register("drvstatus")
tmc.read_register("gconf")

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


# -----------------------------------------------------------------------
# deinitiate the Tmc2240 class
# -----------------------------------------------------------------------
del tmc

print("---")
print("SCRIPT FINISHED")
print("---")
