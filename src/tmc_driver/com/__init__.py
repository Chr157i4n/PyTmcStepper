"""Communication module for TMC stepper drivers

Provides UART and SPI communication implementations for different platforms:
- TmcComUart: Standard UART communication (CPython with pyserial)
- TmcComSpi: Standard SPI communication (CPython with spidev)
- TmcComUartMicroPython: UART for MicroPython
- TmcComSpiMicroPython: SPI for MicroPython
- TmcComSpiFtdi: SPI via FTDI USB devices

Example:
    >>> from tmc_driver.com import TmcComUart
    >>> tmc_com = TmcComUart("/dev/serial0")

Note: Base classes (TmcCom, TmcComUartBase, TmcComSpiBase) can be imported
      directly from their respective files if needed for type hints or subclassing.
"""

try:
    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        # Import for type checkers/IDE only - not executed at runtime
        from ._tmc_com_uart import TmcComUart
        from ._tmc_com_spi import TmcComSpi
        from ._tmc_com_uart_micropython import TmcComUartMicroPython
        from ._tmc_com_spi_micropython import TmcComSpiMicroPython
        from ._tmc_com_spi_ftdi import TmcComSpiFtdi
except ImportError:
    pass


def __getattr__(name):
    """Lazy import of communication classes to avoid circular imports"""
    if name == "TmcComUart":
        from ._tmc_com_uart import TmcComUart

        return TmcComUart
    elif name == "TmcComSpi":
        from ._tmc_com_spi import TmcComSpi

        return TmcComSpi
    elif name == "TmcComUartMicroPython":
        from ._tmc_com_uart_micropython import TmcComUartMicroPython

        return TmcComUartMicroPython
    elif name == "TmcComSpiMicroPython":
        from ._tmc_com_spi_micropython import TmcComSpiMicroPython

        return TmcComSpiMicroPython
    elif name == "TmcComSpiFtdi":
        from ._tmc_com_spi_ftdi import TmcComSpiFtdi

        return TmcComSpiFtdi
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "TmcComUart",
    "TmcComSpi",
    "TmcComUartMicroPython",
    "TmcComSpiMicroPython",
    "TmcComSpiFtdi",
]
