"""
Enable Control base module
"""

from abc import abstractmethod
from .._tmc_logger import TmcLogger
from ..reg._tmc_reg import TmcReg


class TmcEnableControl:
    """Enable Control base class"""

    def __init__(self):
        """constructor"""
        self._tmc_logger: TmcLogger
        self._get_register_callback = None

    def init(self, tmc_logger: TmcLogger):
        """init: called by the Tmc class"""
        self._tmc_logger = tmc_logger

    def set_get_register_callback(self, callback):
        """Set callback to get registers from parent TMC class

        Args:
            callback: Function that takes register name (str) and returns register object
        """
        self._get_register_callback = callback

    def get_register(self, name: str) -> TmcReg | None:
        """Get register by name from parent TMC class

        Args:
            name: Register name (e.g. 'gconf', 'chopconf')

        Returns:
            Register object or None if callback not set
        """
        if self._get_register_callback is not None:
            return self._get_register_callback(name)
        return None

    def deinit(self):
        """destructor"""

    @abstractmethod
    def set_motor_enabled(self, en):
        """enables or disables the motor current output

        Args:
            en (bool): whether the motor current output should be enabled
        """
