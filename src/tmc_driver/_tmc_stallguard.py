# pylint: disable=too-many-arguments
# pylint: disable=too-many-public-methods
# pylint: disable=too-many-branches
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-positional-arguments
# pylint: disable=bare-except
# pylint: disable=no-member
# pylint: disable=unused-import
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
"""StallGuard mixin"""

import types
from ._tmc_stepperdriver import *
from .com._tmc_com import TmcCom
from .tmc_gpio import GpioPUD, GpioMode
from . import tmc_gpio
from ._tmc_logger import Loglevel
from .reg import _tmc_shared_regs as tmc_shared_regs
from . import _tmc_math as tmc_math
from ._tmc_exceptions import (
    TmcComException,
    TmcMotionControlException,
    TmcDriverException,
)

_CB_SENTINEL = object()


class StallGuard:
    """StallGuard

    This class is used to control the stallguard feature of the TMC stepper driver.
    The drivers class needs to inherit from this class to use the stallguard feature (mixin).
    """

    tmc_logger: TmcLogger
    tmc_com: TmcCom | None
    tmc_mc: TmcMotionControl

    coolconf: tmc_shared_regs.CoolConf
    sgthrs: tmc_shared_regs.SGThrs
    sgresult: tmc_shared_regs.SGResult
    tcoolthrs: tmc_shared_regs.TCoolThrs

    @property
    def sg_callback(self):
        """stallguard callback function"""
        return self._sg_callback

    @sg_callback.setter
    def sg_callback(self, callback):
        if self._pin_stallguard is None:
            raise TmcDriverException(
                "StallGuard pin not set. Cannot set callback function."
            )
        self._sg_callback = callback
        tmc_gpio.tmc_gpio.gpio_remove_event_detect(self._pin_stallguard)
        if callback is not None:
            tmc_gpio.tmc_gpio.gpio_add_event_detect(self._pin_stallguard, callback)

    def __init__(self):
        """initialize StallGuard instance variables"""
        self._pin_stallguard: int | None = None
        self._sg_threshold: int = 100  # threshold for stallguard

    def __del__(self):
        self.deinit()

    def deinit(self):
        """destructor"""
        if (
            getattr(self, "_pin_stallguard", None) is not None
            and self._pin_stallguard is not None
        ):
            tmc_gpio.tmc_gpio.gpio_remove_event_detect(self._pin_stallguard)
            tmc_gpio.tmc_gpio.gpio_cleanup(self._pin_stallguard)
            self._pin_stallguard = None

    def set_stallguard_callback(
        self, pin_stallguard, threshold, callback, min_speed=100
    ):
        """set a function to call back, when the driver detects a stall
        via stallguard
        high value on the diag pin can also mean a driver error

        Args:
            pin_stallguard (int): pin needs to be connected to DIAG
            threshold (int): value for SGTHRS
            callback (func): will be called on StallGuard trigger
            min_speed (int): min speed [steps/s] for StallGuard (Default value = 100)
        """
        self.tmc_logger.log(
            f"setup stallguard callback on GPIO {pin_stallguard}", Loglevel.INFO
        )
        self.tmc_logger.log(
            f"StallGuard Threshold: {threshold} | minimum Speed: {min_speed}",
            Loglevel.INFO,
        )

        self._set_stallguard_threshold(threshold)
        self._set_coolstep_threshold(
            tmc_math.steps_to_tstep(min_speed, self.get_microstepping_resolution())
        )
        self._sg_callback = callback
        self._pin_stallguard = pin_stallguard

        if self._pin_stallguard is not None:
            tmc_gpio.tmc_gpio.gpio_setup(
                self._pin_stallguard, GpioMode.IN, pull_up_down=GpioPUD.PUD_DOWN
            )
            # first remove existing events
            tmc_gpio.tmc_gpio.gpio_remove_event_detect(self._pin_stallguard)
            if callback is not None:
                tmc_gpio.tmc_gpio.gpio_add_event_detect(self._pin_stallguard, callback)

    def enable_coolstep(
        self,
        semin_sg: int = 150,
        semax_sg: int = 200,
        seup: int = 1,
        sedn: int = 3,
        min_speed: int = 100,
    ):
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
        self.coolconf.semin = round(max(0, min(semin_sg / 32, 15)))
        self.coolconf.semax = round(max(0, min(semax_sg / 32, 15)))
        self.coolconf.seimin = True  # scale down to until 1/4 of IRun (7 - 31)
        self.coolconf.seup = int(seup)
        self.coolconf.sedn = int(sedn)
        self.coolconf.write_check()

        self._set_coolstep_threshold(
            tmc_math.steps_to_tstep(int(min_speed), self.get_microstepping_resolution())
        )

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
        self.sgthrs.modify("sgthrs", int(threshold))

    def _set_coolstep_threshold(self, threshold):
        """This  is  the  lower  threshold  velocity  for  switching
        on  smart energy CoolStep and StallGuard to DIAG output. (unsigned)

        Args:
            threshold (int): threshold velocity for coolstep
        """
        self.tcoolthrs.modify("tcoolthrs", int(threshold))

    def _reset_current_pos(self):
        """resets the current position of the motor to 0"""
        if self.tmc_mc is None:
            raise TmcMotionControlException("tmc_mc is None; cannot reset current pos")
        self.tmc_mc.current_pos = 0

    def do_homing(
        self,
        diag_pin: int,
        revolutions=10,
        threshold=100,
        max_speed: int | None = None,
        cb_success: types.FunctionType | object | None = _CB_SENTINEL,
        cb_failure: types.FunctionType | object | None = None,
    ) -> bool:
        """homes the motor in the given direction using stallguard.
        this method is using vactual to move the motor and an interrupt on the DIAG pin

        Args:
            diag_pin (int): DIAG pin number
            revolutions (int): max number of revolutions. Can be negative for inverse direction
                (Default value = 10)
            threshold (int): StallGuard detection threshold (Default value = 100)
            max_speed (int): max speed for homing in steps/s (Default value = None)
            cb_success (func|None): callback function on successful homing
            cb_failure (func|None): callback function on failed homing

        Returns:
            not homing_failed (bool): true when homing was successful
        """
        if self.tmc_com is None:
            raise TmcComException("tmc_com is None; cannot do homing")
        if self.tmc_mc is None:
            raise TmcMotionControlException("tmc_mc is None; cannot do homing")

        self.tmc_logger.log(f"Stallguard threshold: {threshold}", Loglevel.DEBUG)

        if max_speed is None:
            max_speed = self.tmc_mc.max_speed_homing
        if cb_success is _CB_SENTINEL:
            cb_success = self._reset_current_pos

        self.tmc_logger.log("---", Loglevel.INFO)
        self.tmc_logger.log("homing", Loglevel.INFO)

        self.set_spreadcycle(0)

        self.set_stallguard_callback(
            diag_pin,
            threshold,
            lambda _: self.tmc_mc.stop(),
            round(0.5 * max_speed),
        )

        stop_mode = self.tmc_mc.run_to_position_steps(
            revolutions * self.tmc_mc.steps_per_rev, MovementAbsRel.RELATIVE
        )

        homing_succeeded = stop_mode is StopMode.HARDSTOP

        if homing_succeeded:
            self.tmc_logger.log("homing successful", Loglevel.INFO)
            if cb_success is not None:
                cb_success()
        else:
            self.tmc_logger.log("homing failed", Loglevel.INFO)
            if cb_failure is not None:
                cb_failure()

        return homing_succeeded
