"""
test for Tmc2240
"""

import time
import unittest
from src.tmc_driver.tmc_2240 import *
from src.tmc_driver.reg import _tmc224x_reg as tmc224x_reg

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
        self.tmc = Tmc2240(TmcEnableControlPin(1), TmcMotionControlStepDir(2, 3))

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

    def test_reg_adcvsupplyain(self):
        """test_reg_adcvsupplyain"""
        global faketmccom_return_value
        adcvsupplyain = tmc224x_reg.ADCVSupplyAIN(_FakeTmcCom())

        faketmccom_return_value = 0x00000000
        adcvsupplyain.read()
        self.assertEqual(
            adcvsupplyain.adc_ain,
            0,
            f"actual adc_ain: {adcvsupplyain.adc_ain}, expected adc_ain: 0",
        )
        self.assertEqual(
            adcvsupplyain.adc_vsupply,
            0,
            f"actual adc_vsupply: {adcvsupplyain.adc_vsupply}, expected adc_vsupply: 0",
        )
        self.assertEqual(
            adcvsupplyain.adc_vsupply_v,
            0,
            f"actual adc_vsupply_v: {adcvsupplyain.adc_vsupply_v}, expected adc_vsupply_v: 0",
        )
        self.assertEqual(
            adcvsupplyain.adc_ain_v,
            0,
            f"actual adc_ain_v: {adcvsupplyain.adc_ain_v}, expected adc_ain_v: 0",
        )

        faketmccom_return_value = 0x199904D1
        adcvsupplyain.read()

        self.assertEqual(
            adcvsupplyain.adc_ain,
            6553,
            f"actual adc_ain: {adcvsupplyain.adc_ain}, expected adc_ain: 255",
        )
        self.assertEqual(
            adcvsupplyain.adc_vsupply,
            1233,
            f"actual adc_vsupply: {adcvsupplyain.adc_vsupply}, expected adc_vsupply: 255",
        )
        self.assertEqual(
            adcvsupplyain.adc_vsupply_v,
            12.0,
            f"actual adc_vsupply_v: {adcvsupplyain.adc_vsupply_v}, expected adc_vsupply_v: 12.0 V",
        )
        self.assertEqual(
            adcvsupplyain.adc_ain_v,
            2.0,
            f"actual adc_ain_v: {adcvsupplyain.adc_ain_v}, expected adc_ain_v: 2.0 V",
        )

    def test_reg_adctemp(self):
        """test_reg_adctemp"""
        global faketmccom_return_value
        adctemp = tmc224x_reg.ADCTemp(_FakeTmcCom())

        faketmccom_return_value = 0x00000000
        adctemp.read()
        self.assertEqual(
            adctemp.adc_temp,
            0,
            f"actual adc_temp: {adctemp.adc_temp}, expected adc_temp: 0",
        )
        self.assertEqual(
            adctemp.adc_temp_c,
            -264.7,
            f"actual adc_temp_c: {adctemp.adc_temp_c}, expected adc_temp_c: -273.15 °C",
        )

        faketmccom_return_value = 0x000008DD
        adctemp.read()

        self.assertEqual(
            adctemp.adc_temp,
            2269,
            f"actual adc_temp: {adctemp.adc_temp}, expected adc_temp: 255",
        )
        self.assertAlmostEqual(
            adctemp.adc_temp_c,
            30.0,
            places=1,
            msg=f"actual adc_temp_c: {adctemp.adc_temp_c}, expected adc_temp_c: 85.0 °C",
        )


if __name__ == "__main__":
    unittest.main()
