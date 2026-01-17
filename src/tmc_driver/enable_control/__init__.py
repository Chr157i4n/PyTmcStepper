# pylint: disable=import-outside-toplevel
"""Enable control module for TMC stepper drivers

Provides motor enable/disable functionality:
- TmcEnableControlPin: Enable via dedicated GPIO pin
- TmcEnableControlToff: Enable via TOFF register field

Example:
    >>> from tmc_driver.enable_control import TmcEnableControlPin
    >>> ec = TmcEnableControlPin(enable_pin=21)
    >>> ec.set_motor_enabled(True)

Note: Uses lazy imports to avoid circular import issues.
"""

try:
    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        # Import for type checkers/IDE only - not executed at runtime
        from ._tmc_ec import TmcEnableControl
        from ._tmc_ec_pin import TmcEnableControlPin
        from ._tmc_ec_toff import TmcEnableControlToff

    if TYPE_CHECKING:
        # Import for type checkers/IDE only - not executed at runtime
        from ._tmc_ec import TmcEnableControl
        from ._tmc_ec_pin import TmcEnableControlPin
        from ._tmc_ec_toff import TmcEnableControlToff
except ImportError:
    pass


def __getattr__(name):
    """Lazy import of enable control classes to avoid circular imports"""
    if name == "TmcEnableControl":
        from ._tmc_ec import TmcEnableControl

        return TmcEnableControl
    if name == "TmcEnableControlPin":
        from ._tmc_ec_pin import TmcEnableControlPin

        return TmcEnableControlPin
    if name == "TmcEnableControlToff":
        from ._tmc_ec_toff import TmcEnableControlToff

        return TmcEnableControlToff
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "TmcEnableControl",
    "TmcEnableControlPin",
    "TmcEnableControlToff",
]
