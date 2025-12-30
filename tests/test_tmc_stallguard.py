"""
test for _tmc_move.py
"""

import time
import unittest
from threading import Thread
from src.tmc_driver.tmc_2209 import *
from src.tmc_driver.com._tmc_com_uart import *
from src.tmc_driver.com._tmc_com_uart_base import compute_crc8_atm


class _FakeSerial:
    """Fake serial object for compatibility with base class"""

    def __init__(self):
        """Constructor for fake serial object"""
        self.is_open = True
        self.baudrate = 115200
        self.com_counter = 0

    def close(self):
        """Close the fake serial port"""
        self.is_open = False

    def open(self):
        """Open the fake serial port"""
        self.is_open = True

    def read(self, size: int) -> bytes:
        """Read bytes from fake serial port"""
        self.com_counter += 1

        rtn = [0] * size
        # Faking IFCNT Value
        rtn[7:11] = [0x00, 0x00, 0x00, self.com_counter & 0xFF]
        if size == 12:
            rtn[11] = compute_crc8_atm(rtn[4:11])
        return bytes(rtn)

    def write(self, data: bytes) -> int:
        """Write bytes to fake serial port"""
        return len(data)

    def reset_output_buffer(self):
        """Reset output buffer"""

    def reset_input_buffer(self):
        """Reset input buffer"""


homing_result = False


def do_homing_with_result_as_global(
    tmc: Tmc2209, pin, revolutions=10, threshold=100, max_speed: int | None = None
):
    """Thread target for homing"""
    global homing_result
    homing_result = tmc.do_homing(pin, revolutions, threshold, max_speed)


class TestTMCStallGuard(unittest.TestCase):
    """TestTMCMove"""

    def setUp(self):
        """setUp"""
        tmc_com = TmcComUart("/dev/serial0", 115200)
        tmc_com.ser = _FakeSerial()
        self.tmc = Tmc2209(
            TmcEnableControlPin(1), TmcMotionControlStepDir(2, 3), tmc_com
        )

        # these values are normally set by reading the driver
        self.tmc.mres = 2

        self.tmc.acceleration_fullstep = 100000
        self.tmc.max_speed_fullstep = 10000
        self.tmc.movement_abs_rel = MovementAbsRel.ABSOLUTE

    def tearDown(self):
        """tearDown"""

    def test_homing(self):
        """test_run_to_position_steps"""

        result = self.tmc.do_homing(4, 1)
        self.assertFalse(result, "Homing should have failed")
        result = self.tmc.do_homing(4, -1)
        self.assertFalse(result, "Homing should have failed")

        homing_thread = Thread(
            target=do_homing_with_result_as_global, args=(self.tmc, 4, 10)
        )
        homing_thread.start()
        time.sleep(0.1)
        self.tmc.tmc_mc.stop()
        homing_thread.join()
        self.assertTrue(homing_result, "Homing failed")

        homing_thread = Thread(
            target=do_homing_with_result_as_global, args=(self.tmc, 4, -10)
        )
        homing_thread.start()
        time.sleep(0.1)
        self.tmc.tmc_mc.stop()
        homing_thread.join()
        self.assertTrue(homing_result, "Homing failed")


if __name__ == "__main__":
    unittest.main()
