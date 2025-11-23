"""
test for _tmc_move.py
"""

import time
import unittest
from unittest import mock
from src.tmc_driver.tmc_2209 import *

class TestTMCModules(unittest.TestCase):
    """TestTMCMove"""

    def setUp(self):
        """setUp"""

    def tearDown(self):
        """tearDown"""

    def test_modules(self):
        """test_modules"""

        for _ in range(2):
            tmc = Tmc2209(TmcEnableControlPin(21), TmcMotionControlStepDir(16, 20), None)

            self.assertTrue(tmc.tmc_ec is not None, "tmc_ec should not be None")
            self.assertEqual(tmc.tmc_ec.pin_en, 21, "tmc_ec pin_en should be 21")
            self.assertTrue(tmc.tmc_mc is not None, "tmc_mc should not be None")
            self.assertEqual(tmc.tmc_mc.pin_step, 16, "tmc_mc pin_step should be 16")
            self.assertEqual(tmc.tmc_mc.pin_dir, 20, "tmc_mc pin_dir should be 20")
            self.assertTrue(tmc.tmc_com is None, "tmc_mc should be None")

            tmc.deinit()
            self.assertTrue(tmc.tmc_ec is not None, "tmc_ec should not be None")
            self.assertEqual(tmc.tmc_ec.pin_en, None, "tmc_ec pin_en should be 21")
            self.assertTrue(tmc.tmc_mc is not None, "tmc_mc should not be None")
            self.assertEqual(tmc.tmc_mc.pin_step, None, "tmc_mc pin_step should be 16")
            self.assertEqual(tmc.tmc_mc.pin_dir, None, "tmc_mc pin_dir should be 20")
            self.assertTrue(tmc.tmc_com is None, "tmc_mc should be None")
        pass

        tmc = Tmc2209(TmcEnableControlPin(21), TmcMotionControlStepDir(16, 20), None)
        tmc.deinit()

        tmc = Tmc2209(TmcEnableControlPin(21), TmcMotionControlStepReg(16), None)
        tmc.deinit()

        tmc = Tmc2209(TmcEnableControlPin(21), TmcMotionControlVActual(), None)
        tmc.deinit()

        with mock.patch.object(TmcStepperDriver, 'set_motor_enabled'):
            tmc = Tmc2209(TmcEnableControlToff(), TmcMotionControlStepDir(16, 20), None)
            tmc.deinit()

            tmc = Tmc2209(TmcEnableControlToff(), TmcMotionControlStepReg(16), None)
            tmc.deinit()

            tmc = Tmc2209(TmcEnableControlToff(), TmcMotionControlVActual(), None)
            tmc.deinit()


if __name__ == '__main__':
    unittest.main()
