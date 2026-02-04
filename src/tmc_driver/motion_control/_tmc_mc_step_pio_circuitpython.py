# pylint: skip-file
"""CircuitPython PIO implementation for STEP/DIR Motion Control.

This module provides the CircuitPython-specific PIO wrapper for the
RP2040/RP2350 microcontroller using rp2pio and adafruit_pioasm.
"""

import rp2pio
import adafruit_pioasm

from ._tmc_mc_step_pio_base import BasePioWrapper


PIO_PROGRAM_STR = """
.program step_pulse
.wrap_target
    ; Pull data (steps << 16 | delay) from FIFO into OSR
    pull block
    ; Shift right 16 bits and move to Y (step count)
    out y, 16
    ; Move remaining 16 bits to ISR (delay value)
    out isr, 16

step_loop:
    ; Set pin high for one cycle only
    set pins, 1
    ; Set pin low immediately (no delay while high)
    set pins, 0
    ; Trigger IRQ 0 to notify controller about step (MicroPython only)
    irq 0
    ; Delay countdown - copy delay from ISR to X, count down X
    mov x, isr
low_delay:
    jmp x--, low_delay

    ; Decrement step counter (Y) and repeat if not zero
    jmp y--, step_loop

done:
    ; Push magic pattern (0x1234) to RX FIFO to signal completion
    ; Load magic pattern using set (4 bits at a time) into ISR
    set x, 0x01        ; upper 4 bits: 0001
    mov isr, x
    in isr, 4
    set x, 0x02        ; next 4 bits: 0010
    in x, 4
    set x, 0x03        ; next 4 bits: 0011
    in x, 4
    set x, 0x04        ; last 4 bits: 0100
    in x, 4
    push noblock
.wrap
"""


class CircuitPythonPioWrapper(BasePioWrapper):
    """PIO wrapper for CircuitPython using rp2pio.StateMachine."""

    def __init__(self, pio_id: int, sm_id: int, pin_step, frequency: int):
        """Initialize CircuitPython PIO state machine.

        Args:
            pio_id: PIO block (0 or 1)
            sm_id: State machine ID (0-3)
            pin_step: Board pin object (e.g., board.GP17)
            frequency: PIO frequency in Hz
        """
        raise NotImplementedError

    def deinit(self):
        """Deinitialize the state machine."""
        raise NotImplementedError

    def put(self, data: int):
        """Put data into TX FIFO."""
        raise NotImplementedError

    def get(self) -> int:
        """Get data from RX FIFO."""
        raise NotImplementedError

    def active(self, value: int):
        """Set state machine active state."""
        raise NotImplementedError

    def restart(self):
        """Restart the state machine."""
        raise NotImplementedError

    def tx_fifo(self) -> int:
        """Get number of entries in TX FIFO (pending writes)"""
        raise NotImplementedError

    def rx_fifo(self) -> int:
        """Get number of entries in RX FIFO (available reads)"""
        raise NotImplementedError

    def irq(self, handler=None):
        """IRQ not supported in CircuitPython - no-op"""
        pass
