"""Tmc logger module base."""

from enum import IntEnum
from abc import abstractmethod


class Loglevel(IntEnum):
    """Loglevel."""

    ALL = 1  # all messages will be logged
    MOVEMENT = 5  # error, warning, info, debug and movement messages will be logged
    DEBUG = 10  # error, warning, info and debug messages will be logged
    INFO = 20  # error, warning and info messages will be logged
    WARNING = 30  # error and warning messages will be logged
    ERROR = 40  # only error messages will be logged
    NONE = -1  # no messages will be logged


class TmcLoggerBase:
    """Tmc2209_logger.

    this class has the function:
    log messages from the Tmc2209 lib
    """

    @property
    def loglevel(self):
        """Get the loglevel."""
        return self._loglevel

    @loglevel.setter
    def loglevel(self, loglevel: Loglevel):
        """Set the loglevel."""
        self._loglevel = loglevel

    @property
    def logprefix(self):
        """Get the logprefix."""
        return self._logprefix

    @logprefix.setter
    def logprefix(self, logprefix: str):
        """Set the logprefix."""
        self._logprefix = logprefix

    def __init__(
        self,
        loglevel: Loglevel = Loglevel.INFO,
        logprefix: str = "TMCXXXX",
    ):
        """Constructor.

        Args:
            loglevel (enum): level for which to log
            logprefix (string): new logprefix (name of the logger) (default: "TMCXXXX")
        """
        self.logprefix = logprefix
        self.loglevel = loglevel

    def __del__(self):
        """Destructor."""
        self.deinit()

    @abstractmethod
    def deinit(self):
        """destructor."""
        self.remove_all_handlers()

    @abstractmethod
    def add_handler(self, handler, formatter=None):
        """Add a handler to the logger.

        Args:
            handler (logging.Handler): handler to add
            formatter (logging.Formatter): formatter for the handler,
                or None to use the existing formatter (default: None)
        """

    @abstractmethod
    def remove_handler(self, handler):
        """Remove a handler from the logger."""

    @abstractmethod
    def remove_all_handlers(self):
        """Remove all handlers from the logger."""

    @abstractmethod
    def set_formatter(self, formatter, handlers=None):
        """Set a new formatter for the log messages.

        Args:
            formatter (logging.Formatter): new formatter
            handlers (list): list of logging handlers to set the new formatting for,
                or None to set it for all the handlers
                (default: None)
        """

    @abstractmethod
    def log(self, message, loglevel: Loglevel = Loglevel.INFO):
        """Logs a message.

        Args:
            message (string): message to log
            loglevel (enum): loglevel of this message (Default value = Loglevel.INFO)
        """
