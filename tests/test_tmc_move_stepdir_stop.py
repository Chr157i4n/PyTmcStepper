"""
test for stopping a movement (StopMode) of _tmc_mc_step_dir.py
"""

import time
import unittest
from src.tmc_driver.tmc_2209 import *


class TestTMCMoveStop(unittest.TestCase):
    """TestTMCMoveStop"""

    # with mres = 2: max speed = 2000 steps/s, acceleration = 4000 steps/s^2
    # => distance needed to stop from max speed: v^2 / (2a) = 500 steps
    MAX_SPEED_FULLSTEP = 1000
    ACCELERATION_FULLSTEP = 2000
    STOP_DISTANCE = 500
    TOLERANCE = 25

    TARGET = 5000

    def setUp(self):
        """setUp"""
        self.tmc = Tmc2209(None, TmcMotionControlStepDir(16, 20))

        # these values are normally set by reading the driver
        self.tmc.mres = 2

        self.tmc.acceleration_fullstep = self.ACCELERATION_FULLSTEP
        self.tmc.max_speed_fullstep = self.MAX_SPEED_FULLSTEP
        self.tmc.movement_abs_rel = MovementAbsRel.ABSOLUTE

    def tearDown(self):
        """tearDown"""
        # make sure no movement thread outlives a failed test
        self.tmc.tmc_mc.stop(StopMode.HARDSTOP)
        thread = self.tmc.tmc_mc._movement_thread
        if thread is not None:
            thread.join(timeout=10)

    def _wait_until_distance(self, distance, timeout=5):
        """block until the motor has travelled at least 'distance' steps
        (absolute value) from position 0"""
        start = time.time()
        while abs(self.tmc.tmc_mc.current_pos) < distance:
            self.assertLess(
                time.time() - start,
                timeout,
                f"motor did not reach {distance} steps within {timeout}s",
            )
            time.sleep(0.001)

    def _start_and_stop(self, target, stop_after, stop_mode):
        """start a threaded movement to 'target' and stop it with 'stop_mode'
        once 'stop_after' steps are travelled

        Returns:
            (position when stopped, final position, returned StopMode)
        """
        self.tmc.tmc_mc.run_to_position_steps_threaded(target, MovementAbsRel.RELATIVE)
        self._wait_until_distance(stop_after)
        self.tmc.tmc_mc.stop(stop_mode)
        pos_stop = self.tmc.tmc_mc.current_pos
        result = self.tmc.tmc_mc.wait_for_movement_finished_threaded()
        pos_end = self.tmc.tmc_mc.current_pos
        return pos_stop, pos_end, result

    def _assert_softstop_at_max_speed(self, target):
        """softstop while running at max speed must decelerate
        over v^2 / (2a) steps and not run to the target"""
        # the acceleration phase is 500 steps long,
        # so after 1000 steps the motor runs at max speed
        pos_stop, pos_end, result = self._start_and_stop(
            target, 1000, StopMode.SOFTSTOP
        )
        travelled = abs(pos_end - pos_stop)

        self.assertEqual(result, StopMode.SOFTSTOP)
        self.assertNotEqual(
            pos_end, target, "softstop had no effect, motor ran to the target"
        )
        self.assertAlmostEqual(
            travelled,
            self.STOP_DISTANCE,
            delta=self.TOLERANCE,
            msg=f"stopped at {pos_stop}, ended at {pos_end}: "
            f"travelled {travelled} steps, expected about {self.STOP_DISTANCE}",
        )
        self.assertEqual(self.tmc.tmc_mc.movement_phase, MovementPhase.STANDSTILL)

    def test_softstop_cw(self):
        """test_softstop_cw"""
        self._assert_softstop_at_max_speed(self.TARGET)

    def test_softstop_ccw(self):
        """test_softstop_ccw"""
        self._assert_softstop_at_max_speed(-self.TARGET)

    def test_softstop_during_acceleration(self):
        """softstop during acceleration must stop sooner than from max speed"""
        pos_stop, pos_end, result = self._start_and_stop(
            self.TARGET, 100, StopMode.SOFTSTOP
        )
        travelled = pos_end - pos_stop

        self.assertEqual(result, StopMode.SOFTSTOP)
        self.assertGreaterEqual(travelled, 0)
        self.assertLess(
            travelled,
            self.STOP_DISTANCE,
            f"stopped at {pos_stop}, ended at {pos_end}: travelled {travelled} steps",
        )

    def test_hardstop(self):
        """hardstop must stop (almost) immediately"""
        pos_stop, pos_end, result = self._start_and_stop(
            self.TARGET, 1000, StopMode.HARDSTOP
        )

        self.assertEqual(result, StopMode.HARDSTOP)
        self.assertLessEqual(
            abs(pos_end - pos_stop), 2, f"stopped at {pos_stop}, ended at {pos_end}"
        )

    def test_move_after_softstop(self):
        """a movement after a softstop must run normally to its target"""
        self._start_and_stop(self.TARGET, 1000, StopMode.SOFTSTOP)

        result = self.tmc.run_to_position_steps(0)
        pos = self.tmc.tmc_mc.current_pos
        self.assertEqual(result, StopMode.NO)
        self.assertEqual(pos, 0, f"actual position: {pos}, expected position: 0")


if __name__ == "__main__":
    unittest.main()
