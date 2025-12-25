"""Exceptions module"""


class TmcException(Exception):
    """Base class for all TMC exceptions"""


class TmcDriverException(TmcException):
    """Base class for all TMC driver exceptions"""


class TmcComException(TmcException):
    """Base class for all TMC communication exceptions"""


class TmcMotionControlException(TmcException):
    """Base class for all TMC motion control exceptions"""


class TmcEnableControlException(TmcException):
    """Base class for all TMC enable control exceptions"""
