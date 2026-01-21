"""
test for _tmc_move.py
"""

import time
import unittest
from src.tmc_driver.tmc_2209 import *
from src.tmc_driver import tmc_2209


class _FakeTmcCom:
    """_FakeTmcCom class for testing purposes"""

    def read_int(self, addr: int, tries: int = 3):
        """fake read_int method for testing purposes"""
        value = 0
        if addr == tmc_2209.GConf.ADDR:
            value = 0
        return value, None

    def write_reg(self, addr: int, data: int):
        """fake write_reg method for testing purposes"""
        # if addr == tmc_5160.XActual.ADDR:
        #     current_pos = data
        # if addr == tmc_5160.XTarget.ADDR:
        #     current_pos = data

    def write_reg_check(self, addr: int, data: int):
        """fake write_reg_check method for testing purposes"""
        self.write_reg(addr, data)
        return True


fake_com = _FakeTmcCom()

reg_dict = {
    "gconf": tmc_2209.GConf(fake_com),
    "vactual": tmc_2209.VActual(fake_com),
}


def register_callback(reg: str):
    """register_callback function for testing purposes"""
    return reg_dict.get(reg, None)


class TestTMCMove(unittest.TestCase):
    """TestTMCMove"""

    def setUp(self):
        """setUp"""
        self.tmc = Tmc2209(None, TmcMotionControlVActual())
        self.tmc.tmc_mc.set_get_register_callback(register_callback)

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

    def test_run_to_position_other(self):
        """test_run_to_position_other"""
        self.tmc.run_to_position_fullsteps(200)  # move to position 200 (fullsteps)
        pos = self.tmc.tmc_mc.current_pos
        self.assertEqual(pos, 400, f"actual position: {pos}, expected position: 400")

        self.tmc.run_to_position_fullsteps(0)  # move to position 0
        pos = self.tmc.tmc_mc.current_pos
        self.assertEqual(pos, 0, f"actual position: {pos}, expected position: 400")

        self.tmc.run_to_position_fullsteps(
            200, MovementAbsRel.RELATIVE
        )  # move 200 fullsteps forward
        pos = self.tmc.tmc_mc.current_pos
        self.assertEqual(pos, 400, f"actual position: {pos}, expected position: 400")

        self.tmc.run_to_position_fullsteps(
            -200, MovementAbsRel.RELATIVE
        )  # move 200 fullsteps backward
        pos = self.tmc.tmc_mc.current_pos
        self.assertEqual(pos, 0, f"actual position: {pos}, expected position: 400")

        self.tmc.run_to_position_steps(400)  # move to position 400 (µsteps)
        pos = self.tmc.tmc_mc.current_pos
        self.assertEqual(pos, 400, f"actual position: {pos}, expected position: 400")

        self.tmc.run_to_position_steps(0)  # move to position 0
        pos = self.tmc.tmc_mc.current_pos
        self.assertEqual(pos, 0, f"actual position: {pos}, expected position: 400")

        self.tmc.run_to_position_revolutions(1)  # move 1 revolution forward
        pos = self.tmc.tmc_mc.current_pos
        self.assertEqual(pos, 400, f"actual position: {pos}, expected position: 400")

        self.tmc.run_to_position_revolutions(0)  # move 1 revolution backward
        pos = self.tmc.tmc_mc.current_pos
        self.assertEqual(pos, 0, f"actual position: {pos}, expected position: 400")


if __name__ == "__main__":
    unittest.main()
