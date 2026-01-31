"""
test for _tmc_ec_pin.py
"""

import unittest


class TestTmcEnableControlPin(unittest.TestCase):
    """TestTmcEnableControlPin"""

    def setUp(self):
        """setUp"""

    def test_imports(self):
        """test_enable"""
        from src.tmc_driver import TmcLogger, Loglevel
        from src.tmc_driver import Tmc2208, Tmc2209, Tmc2240, Tmc5160
        from src.tmc_driver import tmc_gpio, Board

        from src.tmc_driver.com import TmcComUart

        try:
            from src.tmc_driver.com import TmcComSpi
        except ImportError:
            pass

        from src.tmc_driver.enable_control import (
            TmcEnableControlPin,
            TmcEnableControlToff,
        )

        from src.tmc_driver.motion_control import (
            TmcMotionControlStepDir,
            TmcMotionControlStepPwmDir,
            TmcMotionControlStepReg,
            TmcMotionControlVActual,
            TmcMotionControlIntRampGenerator,
            StopMode,
            MovementAbsRel,
            MovementPhase,
            Direction,
        )


if __name__ == "__main__":
    unittest.main()
