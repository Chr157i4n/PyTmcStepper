"""
test for _tmc_com_uart.py
"""

import unittest
from unittest import mock
from src.tmc_driver.com._tmc_com_uart import TmcComUart


class _FakeSerial:
    """Fake serial object for compatibility with base class"""

    def __init__(self, uart):
        """Constructor for fake serial object"""
        self._uart = uart
        self.is_open = True

    def close(self):
        """Close the fake serial port"""
        self.is_open = False


class TestTmcComUart(unittest.TestCase):
    """TestTmcComUart"""

    def setUp(self):
        """setUp"""
        self.tmc_uart = TmcComUart(None, 115200)

    def test_read_int(self):
        """test_read_int"""
        self.tmc_uart.ser = _FakeSerial(None)
        with mock.patch.object(
            TmcComUart,
            "read_reg",
            return_value=(b"U\x00o\x03\x05\xffo\xc0\x1e\x00\x00\xca", None),
        ):
            reg_ans, _ = self.tmc_uart.read_int(0x00)
            self.assertEqual(reg_ans, -1071775744, "read_int is wrong")


if __name__ == "__main__":
    unittest.main()
