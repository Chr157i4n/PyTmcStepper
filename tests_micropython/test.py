import sys

print(sys.version)
print(sys.implementation)

sys.path.insert(0, "src")

import os

cwd = os.getcwd()
print("Current working directory:", cwd)

files = os.listdir(cwd)

# Print the files
for file in files:
    print(file)


import unittest
from src.tmc_driver import (
    Tmc2209,
    TmcEnableControlPin,
    TmcMotionControlStepDir,
    MovementAbsRel,
)


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


if __name__ == "__main__":
    unittest.main()
