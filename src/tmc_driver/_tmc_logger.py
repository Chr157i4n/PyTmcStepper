#pylint: disable=protected-access
#pylint: skip-file
"""
Tmc2209 stepper driver logger module
"""

from enum import IntEnum
import sys

# Detect MicroPython
MICROPYTHON = sys.implementation.name == "micropython"

if not MICROPYTHON:
    import logging





class Loglevel(IntEnum):
    """loglevel"""
    ALL = 1             # all messages will be logged
    MOVEMENT = 5        # error, warning, info, debug and movement messages will be logged
    DEBUG = 10          # error, warning, info and debug messages will be logged
    INFO = 20           # error, warning and info messages will be logged
    WARNING = 30        # error and warning messages will be logged
    ERROR = 40          # only error messages will be logged
    NONE = -1           # no messages will be logged



if MICROPYTHON:
    class TmcLogger:
        """minimal logger for MicroPython"""

        def __init__(self, loglevel=None, logprefix=None, handlers=None, formatter=None):
            self._loglevel = Loglevel.NONE

        @property
        def loglevel(self):
            return self._loglevel

        @loglevel.setter
        def loglevel(self, loglevel):
            self._loglevel = loglevel

        def __del__(self):
            pass

        def deinit(self):
            pass

        def set_logprefix(self, logprefix):
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
            if loglevel is None or self.loglevel is None or loglevel >= self._loglevel:
                print(message)
else:
    class TmcLogger:
        """Tmc2209_logger

        this class has the function:
        log messages from the Tmc2209 lib
        """

        @property
        def loglevel(self):
            """get the loglevel"""
            return self._loglevel

        @loglevel.setter
        def loglevel(self, loglevel: Loglevel):
            """set the loglevel"""
            self._loglevel = loglevel
            self.logger.setLevel(int(loglevel))


        def __init__(self,
                     loglevel: Loglevel = Loglevel.INFO,
                     logprefix: str = "TMC2209",
                     handlers: list|None = None,
                     formatter: logging.Formatter|None = None):
            """constructor

            Args:
                logprefix (string): new logprefix (name of the logger) (default: "TMC2209")
                loglevel (enum): level for which to log
                handlers (list): list of logging handlers, see logging.handlers (default: None)
                formatter (logging.Formatter): formatter for the log messages (default: None)
            """
            self._loglevel: Loglevel = Loglevel.INFO

            if logprefix is None:
                logprefix = "TMC2209"

            # Add our custom log levels to the logger
            for level in [Loglevel.ALL, Loglevel.MOVEMENT, Loglevel.NONE]:
                self._add_logging_level(level.name, int(level))

            self.logger = logging.getLogger(logprefix)

            self.loglevel = loglevel
            if formatter is None:
                formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            self.formatter = formatter

            if handlers is None:
                # Default handler: StreamHandler (logs to console)
                handlers = [logging.StreamHandler()]

            for handler in handlers:
                handler.setFormatter(self.formatter)
                self.logger.addHandler(handler)

            self.logger.propagate = True


        def __del__(self):
            """destructor"""
            self.deinit()


        def deinit(self):
            """destructor"""
            self.remove_all_handlers()


        def set_logprefix(self, logprefix: str):
            """set the logprefix.

            Args:
                logprefix (string): new logprefix
            """
            self.logger.name = logprefix


        def add_handler(self, handler, formatter=None):
            """add a handler to the logger

            Args:
                handler (logging.Handler): handler to add
                formatter (logging.Formatter): formatter for the handler,
                    or None to use the existing formatter (default: None)
            """
            if formatter is None:
                formatter = self.formatter
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)


        def remove_handler(self, handler):
            """remove a handler from the logger

            Args:
                handler (logging.Handler): handler to remove
            """
            self.logger.removeHandler(handler)


        def remove_all_handlers(self):
            """remove all handlers from the logger"""
            for handler in self.logger.handlers:
                self.logger.removeHandler(handler)


        def set_formatter(self, formatter, handlers=None):
            """set a new formatter for the log messages

            Args:
                formatter (logging.Formatter): new formatter
                handlers (list): list of logging handlers to set the new formatting for,
                    or None to set it for all the handlers
                    (default: None)
            """
            self.formatter = formatter
            if handlers is None:
                handlers = self.logger.handlers
            for handler in handlers:
                handler.setFormatter(formatter)


        @staticmethod
        def _add_logging_level(level_name: str, level_num: int, method_name: str|None = None):
            if not method_name:
                method_name = level_name.lower()

            def logForLevel(self, message, *args, **kwargs):
                if self.isEnabledFor(level_num):
                    self._log(level_num, message, args, **kwargs)

            def logToRoot(message, *args, **kwargs):
                logging.log(level_num, message, *args, **kwargs)

            logging.addLevelName(level_num, level_name)
            setattr(logging, level_name, level_num)
            setattr(logging.getLoggerClass(), method_name, logForLevel)
            setattr(logging, method_name, logToRoot)


        def log(self, message, loglevel: Loglevel = Loglevel.INFO):
            """logs a message

            Args:
                message (string): message to log
                loglevel (enum): loglevel of this message (Default value = Loglevel.INFO)
            """
            if self.loglevel is not Loglevel.NONE:
                self.logger.log(int(loglevel), message)
