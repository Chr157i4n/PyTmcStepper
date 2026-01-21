"""
test for Tmc2209
"""

import unittest
from src.tmc_driver import (
    Tmc2209,
    TmcEnableControlPin,
    TmcMotionControlStepDir,
    MovementAbsRel,
)
from src.tmc_driver.reg import _tmc220x_reg as tmc220x_reg


faketmccom_return_value = 0


class _FakeTmcCom:
    """_FakeTmcCom class for testing purposes"""

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
        return faketmccom_return_value, None


class TestTMCMove(unittest.TestCase):
    """TestTMCMove"""

    def setUp(self):
        """setUp"""
        self.tmc = Tmc2209(TmcEnableControlPin(1), TmcMotionControlStepDir(2, 3))

        # these values are normally set by reading the driver
        self.tmc.mres = 2

        self.tmc.acceleration_fullstep = 100000
        self.tmc.max_speed_fullstep = 10000
        self.tmc.movement_abs_rel = MovementAbsRel.ABSOLUTE

    def tearDown(self):
        """tearDown"""

    def test_run_to_position_steps(self):
        """test_run_to_position_steps"""

        self.tmc.run_to_position_steps(400, MovementAbsRel.RELATIVE)
        pos = self.tmc.tmc_mc.current_pos
        self.assertEqual(pos, 400, f"actual position: {pos}, expected position: 400")

        self.tmc.run_to_position_steps(-200, MovementAbsRel.RELATIVE)
        pos = self.tmc.tmc_mc.current_pos
        self.assertEqual(pos, 200, f"actual position: {pos}, expected position: 200")

        self.tmc.run_to_position_steps(400)
        pos = self.tmc.tmc_mc.current_pos
        self.assertEqual(pos, 400, f"actual position: {pos}, expected position: 400")

    def test_reg_gstat(self):
        """test_reg_gstat"""
        global faketmccom_return_value
        gstat = tmc220x_reg.GStat(_FakeTmcCom())

        faketmccom_return_value = 0x1

        gstat.read()
        self.assertTrue(gstat.reset, "GStat reset bit should be True")
        self.assertFalse(gstat.drv_err, "GStat drv_err bit should be False")
        self.assertFalse(gstat.uv_cp, "GStat uv_cp bit should be False")
        with self.assertRaises(Exception) as context:
            gstat.check()
            self.assertIn("reset detected", str(context.exception))

        faketmccom_return_value = 0x2

        gstat.read()
        self.assertFalse(gstat.reset, "GStat reset bit should be False")
        self.assertTrue(gstat.drv_err, "GStat drv_err bit should be True")
        self.assertFalse(gstat.uv_cp, "GStat uv_cp bit should be False")
        with self.assertRaises(Exception) as context:
            gstat.check()
            self.assertIn("driver error detected", str(context.exception))

        faketmccom_return_value = 0x4
        gstat.read()
        self.assertFalse(gstat.reset, "GStat reset bit should be False")
        self.assertFalse(gstat.drv_err, "GStat drv_err bit should be False")
        self.assertTrue(gstat.uv_cp, "GStat uv_cp bit should be True")
        with self.assertRaises(Exception) as context:
            gstat.check()
            self.assertIn("undervoltage detected", str(context.exception))

        faketmccom_return_value = 0x0

        gstat.read()
        self.assertFalse(gstat.reset, "GStat reset bit should be False")
        self.assertFalse(gstat.drv_err, "GStat drv_err bit should be False")
        self.assertFalse(gstat.uv_cp, "GStat uv_cp bit should be False")

        gstat.check()  # should not raise


if __name__ == "__main__":
    unittest.main()
