"""Tmc logger module for MicroPython."""

from ._tmc_logger_base import Loglevel, TmcLoggerBase


class TmcLogger(TmcLoggerBase):
    """Minimal logger for MicroPython."""

    def __init__(
        self,
        loglevel: Loglevel = Loglevel.INFO,
        logprefix: str = "TMCXXXX",
        handlers=None,
        formatter=None,
    ):
        """constructor.

        Args:
            loglevel (enum): level for which to log
            logprefix (string): new logprefix (name of the logger) (default: "TMCXXXX")
            handlers (list): list of logging handlers, see logging.handlers (default: None)
            formatter (logging.Formatter): formatter for the log messages (default: None)
        """
        super().__init__(loglevel, logprefix)
        del handlers
        del formatter

    def __del__(self):
        pass

    def deinit(self):
        pass

    def add_handler(self, handler, formatter=None):
        pass

    def remove_handler(self, handler):
        pass

    def remove_all_handlers(self):
        pass

    def set_formatter(self, formatter, handlers=None):
        pass

    def log(self, message, loglevel=None):
        if self.loglevel is Loglevel.NONE:
            return
        if loglevel is None or self.loglevel is None or loglevel >= self._loglevel:
            print(message)
