"""
test for _tmc_move.py
"""

import time
import copy
import unittest
from unittest import mock
from src.tmc_driver.tmc_2208 import *
from src.tmc_driver.tmc_2209 import *
from src.tmc_driver.tmc_2240 import *
from src.tmc_driver.tmc_5160 import *

from src.tmc_driver.com._tmc_com_uart import *
from src.tmc_driver.com._tmc_com_uart_base import compute_crc8_atm

from src.tmc_driver._tmc_exceptions import *

SPI_AVAILABLE = False
try:
    from src.tmc_driver.com._tmc_com_spi import *

    SPI_AVAILABLE = True
except ImportError:
    pass


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


class _FakeSpi:
    """Fake SPI object for compatibility with base class"""

    def __init__(self):
        """Constructor for fake SPI object"""
        self.is_open = True
        self.max_speed_hz = 8000000
        self.mode = 0b11
        self.lsbfirst = False
        self.com_counter = 0

    def open(self, bus: int, dev: int):
        """Open the fake SPI port"""
        self.is_open = True

    def close(self):
        """Close the fake SPI port"""
        self.is_open = False

    def xfer2(self, data: list[int]) -> list[int]:
        """Transfer bytes via fake SPI port"""
        rtn = [0] * len(data)
        return rtn


class TestTMCModules(unittest.TestCase):
    """TestTMCMove"""

    DRIVER: list[TmcXXXX] = [Tmc2208, Tmc2209, Tmc2240, Tmc5160]
    EC: list[TmcEnableControl] = [TmcEnableControlPin(3), TmcEnableControlToff()]
    MC: list[TmcMotionControl] = [
        TmcMotionControlStepDir(1, 2),
        TmcMotionControlStepPwmDir(1, 2),
        TmcMotionControlStepReg(1),
        TmcMotionControlVActual(),
    ]
    COM: list[TmcCom] = [TmcComUart("/dev/serial0", 115200)]
    COM[0].ser = _FakeSerial()

    if SPI_AVAILABLE:
        COM.append(TmcComSpi(0, 0))
        COM[1].spi = _FakeSpi()

    def setUp(self):
        """setUp"""

    def tearDown(self):
        """tearDown"""

    def test_modules(self):
        """test_modules"""

        for driver in self.DRIVER:
            for ec in self.EC:
                for mc in self.MC:
                    for com in self.COM:
                        with self.subTest(
                            driver=driver.__name__,
                            ec=ec.__class__.__name__,
                            mc=mc.__class__.__name__,
                            com=com.__class__.__name__,
                        ):
                            NOT_SUPPORTED = False
                            if not any(
                                isinstance(ec, ec_type)
                                for ec_type in driver.SUPPORTED_EC_TYPES
                            ):
                                NOT_SUPPORTED = True
                            if not any(
                                isinstance(mc, mc_type)
                                for mc_type in driver.SUPPORTED_MC_TYPES
                            ):
                                NOT_SUPPORTED = True
                            if not any(
                                isinstance(com, com_type)
                                for com_type in driver.SUPPORTED_COM_TYPES
                            ):
                                NOT_SUPPORTED = True

                            if NOT_SUPPORTED:
                                with self.assertRaises(Exception) as context:
                                    instance = driver(
                                        copy.copy(ec),
                                        copy.copy(mc),
                                        copy.copy(com),
                                    )

                                self.assertEqual(
                                    type(context.exception), TmcDriverException
                                )
                            else:
                                instance = driver(
                                    copy.copy(ec),
                                    copy.copy(mc),
                                    copy.copy(com),
                                )
                                self.assertIsInstance(instance, driver)
                                self.assertIsInstance(instance.tmc_ec, ec.__class__)
                                self.assertIsInstance(instance.tmc_mc, mc.__class__)
                                self.assertIsInstance(instance.tmc_com, com.__class__)

                                instance.set_microstepping_resolution(2)

                                instance.acceleration_fullstep = 1000
                                instance.max_speed_fullstep = 250

                                self.assertEqual(instance.acceleration_fullstep, 1000)
                                self.assertEqual(instance.max_speed_fullstep, 250)

                                instance.set_motor_enabled(True)
                                instance.set_motor_enabled(False)

                                instance.run_to_position_steps(10)

                                instance.deinit()

        for driver in self.DRIVER:
            with self.subTest(
                driver=driver.__name__,
                ec=TmcEnableControlPin.__name__,
                mc=TmcMotionControlStepDir.__name__,
                com=None,
            ):
                instance = driver(
                    TmcEnableControlPin(3),
                    TmcMotionControlStepDir(1, 2),
                    None,
                )
                self.assertIsInstance(instance, driver)
                self.assertIsInstance(instance.tmc_ec, TmcEnableControlPin)
                self.assertIsInstance(instance.tmc_mc, TmcMotionControlStepDir)
                self.assertEqual(instance.tmc_com, None)

                instance.set_motor_enabled(True)
                instance.set_motor_enabled(False)

                instance.run_to_position_steps(10)

                instance.deinit()

            with self.subTest(
                driver=TmcStepperDriver.__name__,
                ec=TmcEnableControlPin.__name__,
                mc=TmcMotionControlStepDir.__name__,
            ):
                instance = TmcStepperDriver(
                    TmcEnableControlPin(3),
                    TmcMotionControlStepDir(1, 2),
                )
                self.assertIsInstance(instance, TmcStepperDriver)
                self.assertIsInstance(instance.tmc_ec, TmcEnableControlPin)
                self.assertIsInstance(instance.tmc_mc, TmcMotionControlStepDir)

                instance.set_motor_enabled(True)

                instance.run_to_position_steps(10)
                self.assertEqual(instance.current_pos, 10)
                instance.run_to_position_steps(-5, MovementAbsRel.RELATIVE)
                self.assertEqual(instance.current_pos, 5)
                instance.run_to_position_steps(0)
                self.assertEqual(instance.current_pos, 0)

                instance.set_motor_enabled(False)

                instance.deinit()


if __name__ == "__main__":
    unittest.main()
