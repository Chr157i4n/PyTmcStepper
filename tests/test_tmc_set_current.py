"""
test for _tmc_move.py
"""

import time
import unittest
from unittest import mock
from src.tmc_driver.tmc_2209 import *
from src.tmc_driver.tmc_2240 import *
from src.tmc_driver.com._tmc_com import *
import src.tmc_driver.reg._tmc2209_reg as tmc2209_reg
import src.tmc_driver.reg._tmc224x_reg as tmc224x_reg


class TestTmcCom(TmcCom):
    """TestTmcCom class for testing purposes"""

    def init(self):
        """init communication"""

    def deinit(self):
        """deinit communication"""

    def read_int(self, addr: int, tries: int = 3):
        """reads the registry on the TMC with a given address.
        returns the binary value of that register
        Args:
            addr (int): address of the register
            tries (int): number of tries
        Returns:
            bytes: binary value of the register
            None: error message
        """
        return 0, None

    def write_reg_check(self, addr: int, val: int, tries: int = 3):
        """writes the registry on the TMC with a given address.
        returns an error message if any
        Args:
            addr (int): address of the register
            data (bytes): binary value to write to the register
            tries (int): number of tries
        Returns:
            None: if no error
            str: error message
        """
        return None


class TestTMCCurrent(unittest.TestCase):
    """TestTMCCurrent"""

    def setUp(self):
        """setUp"""

    def tearDown(self):
        """tearDown"""

    def test_tmc2209_set_current(self):
        """test_tmc2209_set_current"""
        tmc_com_test = TestTmcCom()

        tmc = Tmc2209(TmcEnableControlPin(21), TmcMotionControlStepDir(16, 20), None)
        tmc.gconf = tmc2209_reg.GConf(tmc_com_test)
        tmc.chopconf = tmc2209_reg.ChopConf(tmc_com_test)
        tmc.ihold_irun = tmc2209_reg.IHoldIRun(tmc_com_test)

        # desired_current: (i_scale_analog, vsense, irun)
        TEST_CASES = {
            400: (False, True, 12),
            450: (False, True, 14),
            1400: (False, False, 24),
            1750: (False, False, 31),
            1800: (False, False, 31),  # max current
        }

        for desired_current, (i_scale_analog, vsense, irun) in TEST_CASES.items():
            with self.subTest(desired_current=desired_current):
                result = tmc.set_current(desired_current)

                self.assertAlmostEqual(
                    result, desired_current, delta=desired_current * 0.05
                )
                self.assertEqual(tmc.gconf.i_scale_analog, i_scale_analog)
                self.assertEqual(tmc.chopconf.vsense, vsense)
                self.assertEqual(tmc.ihold_irun.irun, irun)

    def test_tmc2240_set_current(self):
        """test_tmc2240_set_current"""
        tmc_com_test = TestTmcCom()

        tmc = Tmc2240(TmcEnableControlPin(21), TmcMotionControlStepDir(16, 20), None)
        tmc.drv_conf = tmc224x_reg.DrvConf(tmc_com_test)
        tmc.global_scaler = tmc224x_reg.GlobalScaler(tmc_com_test)
        tmc.ihold_irun = tmc224x_reg.IHoldIRun(tmc_com_test)

        # (desired_current, rref): (current_range, global_scaler, irun)
        TEST_CASES = {
            (300, 12): (0, 78, 31),
            (400, 12): (0, 26, 31),
            (400, 12): (0, 105, 31),
            (300, 27): (0, 176, 31),
            (400, 27): (0, 235, 31),
            (500, 27): (1, 144, 31),
        }

        for (desired_current, rref), (
            current_range,
            global_scaler,
            irun,
        ) in TEST_CASES.items():
            with self.subTest(desired_current=desired_current, rref=rref):
                result = tmc.set_current_peak(desired_current, rref=rref)

                self.assertAlmostEqual(
                    result, desired_current, delta=desired_current * 0.05
                )
                self.assertEqual(tmc.drv_conf.current_range, current_range)
                self.assertEqual(tmc.global_scaler.global_scaler, global_scaler)
                self.assertEqual(tmc.ihold_irun.irun, irun)

    def test_tmc2240_set_current_peak(self):
        """test_tmc2240_set_current"""
        tmc_com_test = TestTmcCom()

        tmc = Tmc2240(TmcEnableControlPin(21), TmcMotionControlStepDir(16, 20), None)
        tmc.drv_conf = tmc224x_reg.DrvConf(tmc_com_test)
        tmc.global_scaler = tmc224x_reg.GlobalScaler(tmc_com_test)
        tmc.ihold_irun = tmc224x_reg.IHoldIRun(tmc_com_test)

        # (desired_current, rref): (current_range, global_scaler, irun)
        TEST_CASES = {
            (10, 12): (0, 3, 28),
            (100, 12): (0, 26, 31),
            (400, 12): (0, 105, 31),
            (1500, 12): (1, 192, 31),
            (2400, 12): (2, 205, 31),
            (2500, 12): (2, 213, 31),
            (3000, 12): (3, 256, 31),
            (3100, 12): (3, 256, 31),  # max current for rref=12
            (10, 27): (0, 6, 31),
            (50, 27): (0, 29, 31),
            (200, 27): (0, 118, 31),
            (300, 27): (0, 176, 31),
            (400, 27): (0, 235, 31),
            (500, 27): (1, 144, 31),
            (800, 27): (1, 230, 31),
            (1200, 27): (2, 230, 31),
            (1300, 27): (2, 250, 31),
            (1400, 27): (3, 256, 31),  # max current for rref=27
        }

        for (desired_current, rref), (
            current_range,
            global_scaler,
            irun,
        ) in TEST_CASES.items():
            with self.subTest(desired_current=desired_current, rref=rref):
                result = tmc.set_current_peak(desired_current, rref=rref)

                self.assertAlmostEqual(
                    result, desired_current, delta=desired_current * 0.05
                )
                self.assertEqual(tmc.drv_conf.current_range, current_range)
                self.assertEqual(tmc.global_scaler.global_scaler, global_scaler)
                self.assertEqual(tmc.ihold_irun.irun, irun)


if __name__ == "__main__":
    unittest.main()
