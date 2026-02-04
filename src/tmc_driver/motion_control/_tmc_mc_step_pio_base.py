"""Base class for PIO state machine wrappers.

This module provides the abstract base class that defines the interface
for platform-specific PIO implementations (MicroPython and
CircuitPython).
"""

from abc import abstractmethod

# Magic pattern used by PIO to signal block completion
# Controller waits for this value in RX FIFO
PIO_MAGIC_PATTERN = 0x1234


class BasePioWrapper:
    """Base class for PIO state machine wrappers.

    Defines the common interface for MicroPython and CircuitPython PIO
    state machine implementations.
    """

    @abstractmethod
    def put(self, data: int):
        """Put data into TX FIFO.

        Args:
            data: 32-bit data word to send to PIO
        """

    @abstractmethod
    def get(self) -> int:
        """Get data from RX FIFO.

        Returns:
            32-bit data word received from PIO
        """

    @abstractmethod
    def active(self, value: int):
        """Set state machine active state.

        Args:
            value: 0 to stop, 1 to run
        """

    @abstractmethod
    def restart(self):
        """Restart the state machine."""

    @abstractmethod
    def tx_fifo(self) -> int:
        """Get number of entries in TX FIFO.

        Returns:
            Number of entries waiting to be processed
        """

    @abstractmethod
    def rx_fifo(self) -> int:
        """Get number of entries in RX FIFO.

        Returns:
            Number of entries available to read
        """

    def irq(self, handler=None):
        """Set IRQ handler (MicroPython only, no-op on CircuitPython).

        Args:
            handler: Callback function for IRQ events, or None to disable
        """

    def deinit(self):
        """Deinitialize the PIO state machine."""
