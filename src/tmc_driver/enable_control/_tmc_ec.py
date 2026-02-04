"""Enable Control base module."""

from abc import abstractmethod
from ..tmc_logger import TmcLogger
from .._tmc_exceptions import TmcEnableControlException


class TmcEnableControl:
    """Enable Control base class."""

    def __init__(self):
        """constructor."""
        self._tmc_logger: TmcLogger
        self._get_register_callback = None

    def init(self, tmc_logger: TmcLogger):
        """Init: called by the Tmc class."""
        self._tmc_logger = tmc_logger

    def set_get_register_callback(self, callback):
        """Set callback to get registers from parent TMC class.

        Args:
            callback: Function that takes register name (str) and returns register object
        """
        self._get_register_callback = callback

    def get_register(self, name: str):
        """Get register by name.

        Args:
            name (str): register name

        Returns:
            register object
        """
        if self._get_register_callback is None:
            raise TmcEnableControlException(
                "Get register callback not set in enable control"
            )
        return self._get_register_callback(name)

    def __del__(self):
        """destructor."""
        self.deinit()

    def deinit(self):
        """destructor."""
        # Only disable motor if callback is still available
        # During garbage collection, parent object may already be destroyed
        if self._get_register_callback is not None:
            self.set_motor_enabled(False)

    @abstractmethod
    def set_motor_enabled(self, en):
        """Enables or disables the motor current output.

        Args:
            en (bool): whether the motor current output should be enabled
        """
