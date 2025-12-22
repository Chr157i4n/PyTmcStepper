#pylint: disable=too-many-arguments
#pylint: disable=too-many-public-methods
#pylint: disable=too-many-branches
#pylint: disable=too-many-instance-attributes
#pylint: disable=too-many-positional-arguments
#pylint: disable=bare-except
#pylint: disable=no-member
#pylint: disable=unused-import
#pylint: disable=wildcard-import
#pylint: disable=unused-wildcard-import
"""StallGuard mixin
"""

import types
from ._tmc_stepperdriver import *
from .com._tmc_com import TmcCom
from .tmc_gpio import GpioPUD, GpioMode
from . import tmc_gpio
from ._tmc_logger import Loglevel
from .reg._tmc224x_reg import *
from . import _tmc_math as tmc_math





class StallGuard():
    """StallGuard

    This class is used to control the stallguard feature of the TMC stepper driver.
    The drivers class needs to inherit from this class to use the stallguard feature (mixin).
    """

    def __init__(self):
        """initialize StallGuard instance variables"""
        self._pin_stallguard:int|None = None
        self._sg_callback:types.FunctionType|None = None


    def __del__(self):
        self.deinit()


    def deinit(self):
        """destructor"""
        if self._deinit_finished is False:
            if self._pin_stallguard is not None:
                tmc_gpio.tmc_gpio.gpio_remove_event_detect(self._pin_stallguard)
                tmc_gpio.tmc_gpio.gpio_cleanup(self._pin_stallguard)
                self._pin_stallguard = None


    def set_stallguard_callback(self, pin_stallguard, threshold, callback,
                                min_speed = 100):
        """set a function to call back, when the driver detects a stall
        via stallguard
        high value on the diag pin can also mean a driver error

        Args:
            pin_stallguard (int): pin needs to be connected to DIAG
            threshold (int): value for SGTHRS
            callback (func): will be called on StallGuard trigger
            min_speed (int): min speed [steps/s] for StallGuard (Default value = 100)
        """
        self.tmc_logger.log(f"setup stallguard callback on GPIO {pin_stallguard}", Loglevel.INFO)
        self.tmc_logger.log(f"StallGuard Threshold: {threshold} | minimum Speed: {min_speed}", Loglevel.INFO)

        self._set_stallguard_threshold(threshold)
        self._set_coolstep_threshold(tmc_math.steps_to_tstep(min_speed, self.get_microstepping_resolution()))
        self._sg_callback = callback
        self._pin_stallguard = pin_stallguard

        tmc_gpio.tmc_gpio.gpio_setup(self._pin_stallguard, GpioMode.IN, pull_up_down=GpioPUD.PUD_DOWN)
        # first remove existing events
        tmc_gpio.tmc_gpio.gpio_remove_event_detect(self._pin_stallguard)
        tmc_gpio.tmc_gpio.gpio_add_event_detect(self._pin_stallguard, self.stallguard_callback)



    def stallguard_callback(self, gpio_pin):
        """the callback function for StallGuard.
        only checks whether the duration of the current movement is longer than
        _sg_delay and then calls the actual callback

        Args:
            gpio_pin (int): pin number of the interrupt pin
        """
        del gpio_pin
        if self._sg_callback is None:
            self.tmc_logger.log("StallGuard callback is None", Loglevel.DEBUG)
            return
        self._sg_callback()



    def enable_coolstep(self, semin_sg:int = 150, semax_sg:int = 200, seup:int = 1, sedn:int = 3, min_speed:int = 100):
        """enables coolstep and sets the parameters for coolstep
        The values for semin etc. can be tested with the test_stallguard_threshold function

        Args:
            semin_sg (int): lower threshold. Current will be increased if SG_Result goes below this
            semax_sg (int): upper threshold. Current will be decreased if SG_Result goes above this
            seup (int): current increment step
            sedn (int): number of SG_Result readings for each current decrement
        """
        semax_sg = semax_sg - semin_sg

        self.coolconf.read()
        self.coolconf.semin = round(max(0, min(semin_sg/32, 15)))
        self.coolconf.semax = round(max(0, min(semax_sg/32, 15)))
        self.coolconf.seimin = 1        # scale down to until 1/4 of IRun (7 - 31)
        self.coolconf.seup = seup
        self.coolconf.sedn = sedn
        self.coolconf.write_check()

        self._set_coolstep_threshold(tmc_math.steps_to_tstep(min_speed, self.get_microstepping_resolution()))



    def get_stallguard_result(self):
        """return the current stallguard result
        its will be calculated with every fullstep
        higher values means a lower motor load

        Returns:
            sgresult (int): StallGuard Result
        """
        self.sgresult.read()
        return self.sgresult.sgresult



    def _set_stallguard_threshold(self, threshold):
        """sets the register bit "SGTHRS" to to a given value
        this is needed for the stallguard interrupt callback
        SGRESULT becomes compared to the double of this threshold.
        SGRESULT ≤ SGTHRS*2

        Args:
            threshold (int): value for SGTHRS
        """
        self.sgthrs.modify("sgthrs", threshold)



    def _set_coolstep_threshold(self, threshold):
        """This  is  the  lower  threshold  velocity  for  switching
        on  smart energy CoolStep and StallGuard to DIAG output. (unsigned)

        Args:
            threshold (int): threshold velocity for coolstep
        """
        self.tcoolthrs.modify("tcoolthrs", threshold)
