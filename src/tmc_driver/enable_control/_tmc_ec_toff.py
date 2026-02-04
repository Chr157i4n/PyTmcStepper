"""Enable Control base module."""

from ._tmc_ec import TmcEnableControl
from ..tmc_logger import Loglevel
from ..reg import _tmc_shared_regs as tmc_shared_reg


class TmcEnableControlToff(TmcEnableControl):
    """Enable Control base class."""

    def __init__(self):
        """constructor."""
        super().__init__()
        self._default_toff = 3

    def set_motor_enabled(self, en):
        """Enables or disables the motor current output.

        Args:
            en (bool): whether the motor current output should be enabled
        """
        self._tmc_logger.log(f"Motor output active: {en}", Loglevel.INFO)

        val = self._default_toff if en else 0

        chopconf: tmc_shared_reg.ChopConf = self.get_register("chopconf")

        chopconf.modify("toff", val)
