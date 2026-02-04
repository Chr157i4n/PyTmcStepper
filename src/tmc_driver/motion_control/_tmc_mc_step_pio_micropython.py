# pylint: skip-file
# pyright: reportUndefinedVariable=false
"""MicroPython PIO implementation for STEP/DIR Motion Control.

This module provides the MicroPython-specific PIO wrapper and assembly
for the RP2040/RP2350 microcontroller.
"""

from machine import Pin
import rp2

from ._tmc_mc_step_pio_base import BasePioWrapper


@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def step_pulse_pio():
    """PIO assembly program for step pulse generation.

    Generates step pulses and pushes magic pattern to RX FIFO when
    complete. Triggers IRQ 0 after each step for position tracking.
    """
    wrap_target()
    # Pull data (steps << 16 | delay) from FIFO into OSR
    pull(block)
    # Shift right 16 bits and move to Y (step count)
    out(y, 16)
    # Move remaining 16 bits to ISR (delay value)
    out(isr, 16)

    # Main loop - repeat for Y toggle cycles
    label("step_loop")

    # Set pin high for one cycle only
    set(pins, 1)
    # Set pin low immediately (no delay while high)
    set(pins, 0)

    # Trigger IRQ 0 to notify controller about step
    irq(0)

    # Delay countdown - copy delay from ISR to X, count down X
    mov(x, isr)
    label("low_delay")
    jmp(x_dec, "low_delay")

    # Decrement step counter (Y) and repeat if not zero
    jmp(y_dec, "step_loop")

    label("done")

    # Push any value to RX FIFO to signal block completion
    # The controller only checks if something was pushed, not the actual value
    push(noblock)
    wrap()


class MicroPythonPioWrapper(BasePioWrapper):
    """PIO wrapper for MicroPython using rp2.StateMachine."""

    def __init__(self, pio_id: int, sm_id: int, pin_step, frequency: int):
        """Initialize MicroPython PIO state machine.

        Args:
            pio_id: PIO block (0 or 1)
            sm_id: State machine ID (0-3)
            pin_step: GPIO pin number for step signal
            frequency: PIO frequency in Hz
        """
        self._sm = rp2.StateMachine(
            pio_id * 4 + sm_id,
            step_pulse_pio,
            freq=frequency,
            set_base=Pin(pin_step),
        )

    def deinit(self):
        """Deinitialize the state machine."""
        self._sm.active(0)

    def put(self, data: int):
        """Put data into TX FIFO."""
        self._sm.put(data)

    def get(self) -> int:
        """Get data from RX FIFO."""
        return self._sm.get()

    def active(self, value: int):
        """Set state machine active state."""
        self._sm.active(value)

    def restart(self):
        """Restart the state machine."""
        self._sm.restart()

    def tx_fifo(self) -> int:
        """Get number of entries in TX FIFO."""
        return self._sm.tx_fifo()

    def rx_fifo(self) -> int:
        """Get number of entries in RX FIFO."""
        return self._sm.rx_fifo()

    def irq(self, handler=None):
        """Set IRQ handler for step counting."""
        self._sm.irq(handler=handler)
