"""
TMC validation module

This module provides validation functions for TMC driver components.
"""

import sys
from ._tmc_exceptions import TmcDriverException


SUBMODULE_VALIDATION = not (
    sys.implementation.name == "micropython"
    or sys.implementation.name == "circuitpython"
)


def validate_submodule(
    module, supported_types: tuple, driver_name: str, module_name: str = "module"
):
    """Validate that a module is of a supported type.

    Args:
        module: The module instance to validate
        supported_types: Tuple of supported base classes
        driver_name: Name of the driver (for error messages)
        module_name: Name of the module being validated (for error messages)

    Raises:
        TmcDriverException: If the module type is not supported
    """
    if module is not None and not isinstance(module, supported_types):
        supported_names = ", ".join(cls.__name__ for cls in supported_types)
        raise TmcDriverException(
            f"{driver_name} does not support {type(module).__name__} as {module_name}. "
            f"Supported types: {supported_names}"
        )
