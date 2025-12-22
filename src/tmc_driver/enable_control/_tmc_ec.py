"""
Enable Control base module
"""

from abc import abstractmethod
from .._tmc_logger import TmcLogger


class TmcEnableControl():
    """Enable Control base class"""


    def __init__(self):
        """constructor"""
        self._tmc_logger:TmcLogger|None = None


    def init(self, tmc_logger: TmcLogger):
        """init: called by the Tmc class"""
        self._tmc_logger = tmc_logger


    def deinit(self):
        """destructor"""


    @abstractmethod
    def set_motor_enabled(self, en):
        """enables or disables the motor current output

        Args:
            en (bool): whether the motor current output should be enabled
        """
