"""
test for _tmc_move.py
"""

import time
import unittest
from src.tmc_driver.tmc_5160 import *
from src.tmc_driver import tmc_5160


current_pos = 100


class _FakeTmcCom:
    """_FakeTmcCom class for testing purposes"""

    def read_int(self, addr: int, tries: int = 3):
        """fake read_int method for testing purposes"""
        value = 0
        if addr == tmc_5160.XActual.ADDR:
            value = current_pos
        if addr == tmc_5160.RampStat.ADDR:
            value = 0xFFFFFFFF  # all flags set - pos reached
        return value, None

    def write_reg(self, addr: int, data: int):
        """fake write_reg method for testing purposes"""
        global current_pos
        if addr == tmc_5160.XActual.ADDR:
            current_pos = data
        if addr == tmc_5160.XTarget.ADDR:
            current_pos = data


fake_com = _FakeTmcCom()

reg_dict = {
    "xactual": tmc_5160.XActual(fake_com),
    "xtarget": tmc_5160.XTarget(fake_com),
    "rampmode": tmc_5160.RampMode(fake_com),
    "rampstat": tmc_5160.RampStat(fake_com),
    "vstart": tmc_5160.VStart(fake_com),
    "vmax": tmc_5160.VMax(fake_com),
    "v1": tmc_5160.V1(fake_com),
    "amax": tmc_5160.AMax(fake_com),
    "a1": tmc_5160.A1(fake_com),
    "dmax": tmc_5160.DMax(fake_com),
    "d1": tmc_5160.D1(fake_com),
    "vstop": tmc_5160.VStop(fake_com),
    "loststeps": tmc_5160.LostSteps(fake_com),
}


def register_callback(reg: str):
    """register_callback function for testing purposes"""
    return reg_dict.get(reg, None)


class TestTMCMove(unittest.TestCase):
    """TestTMCMove"""

    def setUp(self):
        """setUp"""
        self.tmc = Tmc5160(None, TmcMotionControlIntRampGenerator())
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
