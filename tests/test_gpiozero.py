"""
test for Tmc2209 with gpiozero
"""

import time
import unittest
from gpiozero.pins.mock import MockFactory, MockPWMPin
from gpiozero import Device

# Konfiguriere MockFactory mit PWM-Unterstützung
Device.pin_factory = MockFactory(pin_class=MockPWMPin)

import src.tmc_driver.tmc_gpio as tmc_driver_gpio
from src.tmc_driver.tmc_gpio._tmc_gpio_board_gpiozero import GpiozeroWrapper

from src.tmc_driver import (
    Tmc2209,
    TmcEnableControlPin,
    TmcMotionControlStepPwmDir,
    MovementAbsRel,
)
from src.tmc_driver import tmc_2209


class _FakeTmcCom:
    """_FakeTmcCom class for testing purposes"""

    def read_int(self, addr: int, tries: int = 3):  # pylint: disable=unused-argument
        """fake read_int method for testing purposes"""
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


class TestTMCMove(unittest.TestCase):
    """TestTMCMove with gpiozero"""

    @classmethod
    def setUpClass(cls):
        """setUpClass"""

        cls.original_tmc_gpio = tmc_driver_gpio.tmc_gpio
        tmc_driver_gpio.tmc_gpio = GpiozeroWrapper()

    @classmethod
    def tearDownClass(cls):
        """tearDownClass"""
        # Setze tmc_gpio auf die ursprüngliche Implementierung zurück
        if cls.original_tmc_gpio is not None:
            tmc_driver_gpio.tmc_gpio = cls.original_tmc_gpio

    def setUp(self):
        """setUp"""

        self.MovementAbsRel = MovementAbsRel
        self.tmc = Tmc2209(TmcEnableControlPin(1), TmcMotionControlStepPwmDir(2, 3))
        self.tmc.gconf = tmc_2209.GConf(fake_com)
        self.tmc.sgthrs = tmc_2209.SgThrs(fake_com)
        self.tmc.tcoolthrs = tmc_2209.TCoolThrs(fake_com)

        # these values are normally set by reading the driver
        self.tmc.mres = 2

        self.tmc.acceleration_fullstep = 100000
        self.tmc.max_speed_fullstep = 10000
        self.tmc.movement_abs_rel = MovementAbsRel.ABSOLUTE

    def tearDown(self):
        """tearDown"""
        del self.tmc

    def test_run_to_position_steps(self):
        """test_run_to_position_steps"""

        self.tmc.run_to_position_steps(400, self.MovementAbsRel.RELATIVE)
        pos = self.tmc.tmc_mc.current_pos
        self.assertEqual(pos, 400, f"actual position: {pos}, expected position: 400")

        self.tmc.run_to_position_steps(-200, self.MovementAbsRel.RELATIVE)
        pos = self.tmc.tmc_mc.current_pos
        self.assertEqual(pos, 200, f"actual position: {pos}, expected position: 200")

        self.tmc.run_to_position_steps(400)
        pos = self.tmc.tmc_mc.current_pos
        self.assertEqual(pos, 400, f"actual position: {pos}, expected position: 400")

    def test_stallguard_interrupt(self):
        """test_stallguard_interrupt"""
        self.tmc.set_stallguard_callback(4, 100, lambda: print("Stallguard interrupt"))

    def test_run_pwm(self):
        """test_run_to_position_steps_threaded"""
        # continous movement using pwm
        self.tmc.tmc_mc.run_speed_pwm_fullstep(250)
        time.sleep(0.1)
        self.tmc.tmc_mc.run_speed_pwm_fullstep(0)
        time.sleep(0.1)
        self.tmc.tmc_mc.run_speed_pwm_fullstep(-250)
        time.sleep(0.1)
        self.tmc.tmc_mc.run_speed_pwm_fullstep(0)


if __name__ == "__main__":
    unittest.main()
