# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments
# pylint: disable=too-many-branches
# pylint: disable=too-many-positional-arguments
# pylint: skip-file
# pyright: reportUndefinedVariable=false
"""
STEP/DIR Motion Control module using PIO (Programmable I/O)
for Raspberry Pi Pico (RP2040/RP2350) under MicroPython

This module provides precise step pulse generation using the PIO hardware
of the RP2040/RP2350 microcontroller. The PIO generates step pulses with
consistent timing, independent of Python execution.
"""

import time
import math
from machine import Pin
import rp2

from ._tmc_mc import (
    TmcMotionControl,
    MovementAbsRel,
    MovementPhase,
    Direction,
    StopMode,
)
from ..tmc_logger import TmcLogger, Loglevel
from ..tmc_gpio import GpioMode
from .. import tmc_gpio
from .._tmc_exceptions import TmcMotionControlException
from ..platform_utils import get_time_us


class PioData:

    def __init__(self, steps=0, delay=0):
        """
        PIO data structure to hold steps and delay

        Args:
            steps (int): Number of step cycles (16 bits; max 65535)
            delay (int): Delay between steps in ms (16 bits; max 65535)
        """
        self.steps = min(steps, 0xFFFF)
        self.delay = min(delay, 0xFFFF)

    def put(self, sm: rp2.StateMachine, pio_freq=2000):
        """
        Put the steps and delay into the PIO state machine FIFO

        Args:
            sm (rp2.StateMachine): The PIO state machine
            pio_freq (int): Frequency of the PIO state machine in Hz
        """
        if self.steps == 0:
            return  # Nothing to do

        delay = int((self.delay / 1000) * pio_freq)
        # PIO loop does N+1 iterations for Y=N (do-while structure with jmp y_dec)
        # So we send steps-1 to get the correct number of steps
        steps_adjusted = self.steps - 1
        # print(
        #     f"Putting steps: {self.steps} (adjusted: {steps_adjusted}) | delay {self.delay} ms | delay: {delay} (PIO cycles)"
        # )
        data = ((steps_adjusted & 0xFFFF) << 16) | (delay & 0xFFFF)
        sm.put(data)


@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def step_pulse_pio():
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
    set(pins, 1)  # pyright: ignore[reportCallIssue]
    # Set pin low immediately (no delay while high)
    set(pins, 0)  # pyright: ignore[reportCallIssue]

    # Trigger IRQ 0 to notify controller about step
    irq(0)

    # Delay countdown - restore delay from ISR to X, then count down
    mov(x, isr)
    label("low_delay")
    jmp(x_dec, "low_delay")

    # Decrement remaining steps (Y) and repeat if not zero
    jmp(y_dec, "step_loop")

    # All steps done, wrap to beginning for next data
    wrap()


class TmcMotionControlStepPio(TmcMotionControl):
    """STEP/DIR Motion Control class using PIO

    Uses the Programmable I/O (PIO) hardware of the RP2040/RP2350
    to generate precise step pulses. This provides more accurate
    timing compared to software-based stepping.

    Attributes:
        pin_step: GPIO pin number for step signal
        pin_dir: GPIO pin number for direction signal (optional)
        pio_id: PIO block to use (0 or 1)
        sm_id: State machine ID within the PIO block (0-3)
    """

    @property
    def max_speed(self):
        """_max_speed property"""
        return self._max_speed

    @max_speed.setter
    def max_speed(self, speed: int):
        """_max_speed setter"""
        speed = abs(speed)
        if self._max_speed != speed:
            self._max_speed = speed
            if speed == 0.0:
                self._cmin = 0
            else:
                self._cmin = round(1000000.0 / speed)

    @property
    def acceleration(self):
        """_acceleration property"""
        return self._acceleration

    @acceleration.setter
    def acceleration(self, acceleration: int):
        """_acceleration setter"""
        acceleration = abs(acceleration)
        if acceleration == 0:
            return
        self._acceleration = acceleration
        # Calculate c0 per Equation 7, with correction per Equation 15
        self._c0 = round(0.676 * math.sqrt(2.0 / acceleration) * 1000000.0)

    @property
    def pio_frequency(self):
        """Current PIO state machine frequency"""
        return self._pio_frequency

    def pio_irq_handler(self, sm):
        """IRQ handler called by PIO after each step"""
        # Only increment position, don't double-count
        if self._direction == Direction.CW:
            self.current_pos += 1
        else:
            self.current_pos -= 1
        self._steps_completed += 1

        # print(f"IRQ: step {self._steps_completed}")

    def __init__(
        self,
        pin_step: int,
        pin_dir: int | None,
        pio_id: int = 0,
        sm_id: int = 0,
    ):
        """constructor

        Args:
            pin_step: GPIO pin number for step signal
            pin_dir: GPIO pin number for direction signal (None if not used)
            pio_id: PIO block to use (0 or 1), default 0
            sm_id: State machine ID within the PIO block (0-3), default 0
        """
        super().__init__()
        self._pin_step = pin_step
        self._pin_dir = pin_dir
        self._pio_id = pio_id
        self._sm_id = sm_id

        self._sm: rp2.StateMachine | None = None
        self._pio_frequency: int = 20000  # PIO frequency in Hz
        self._steps_completed: int = 0
        self._sqrt_twoa: float = 1.0
        self._step_interval: int = 0
        self._min_pulse_width: int = 1
        self._last_step_time: int = 0
        self._n: int = 0
        self._c0: int = 0
        self._cn: int = 0
        self._cmin: int = 0

    def init(self, tmc_logger: TmcLogger):
        """init: called by the Tmc class"""
        super().init(tmc_logger)
        self._tmc_logger.log(f"STEP Pin (PIO): {self._pin_step}", Loglevel.DEBUG)
        self._tmc_logger.log(
            f"Using PIO {self._pio_id}, SM {self._sm_id}", Loglevel.DEBUG
        )

        # Initialize the PIO state machine for step pulse generation
        self._init_pio()

        if self._pin_dir is not None:
            self._tmc_logger.log(f"DIR Pin: {self._pin_dir}", Loglevel.DEBUG)
            tmc_gpio.tmc_gpio.gpio_setup(
                self._pin_dir, GpioMode.OUT, initial=int(self._direction)
            )

    def _init_pio(self):
        """Initialize or reinitialize the PIO state machine"""
        if self._sm is not None:
            self._sm.active(0)

        # Fixed high frequency - speed control via delay values
        self._sm = rp2.StateMachine(
            self._pio_id * 4 + self._sm_id,
            step_pulse_pio,
            freq=self._pio_frequency,
            set_base=Pin(self._pin_step),
        )

        # Register IRQ handler once for step counting
        self._sm.irq(handler=self.pio_irq_handler)

        self._sm.active(1)

    def deinit(self):
        """destructor"""
        if self._sm is not None:
            self._sm.active(0)
            self._sm = None

        if hasattr(self, "_pin_dir") and self._pin_dir is not None:
            tmc_gpio.tmc_gpio.gpio_cleanup(self._pin_dir)
            del self._pin_dir

    def _start_pio_movement(self, steps: int):
        """Start the PIO with the given number of steps

        Args:
            steps: Number of steps to execute (must be positive)
        """
        if self._sm is None:
            return

        # Clear TX FIFO to remove any old data from previous movements
        # Restart the state machine to reset its state
        self._sm.active(0)
        # Brief delay to ensure clean stop
        time.sleep_ms(1)
        self._sm.restart()
        self._sm.active(1)
        self._steps_completed = 0

    def _drain_rx_fifo(self):
        """Drain the RX FIFO to clear old data"""
        if self._sm is None:
            return
        while self._sm.rx_fifo() > 0:
            self._sm.get()

    def set_direction(self, direction: Direction):
        """sets the motor shaft direction to the given value: 0 = CCW; 1 = CW

        Args:
            direction (bool): motor shaft direction: False = CCW; True = CW
        """
        if self._pin_dir is None:
            return
        super().set_direction(direction)
        tmc_gpio.tmc_gpio.gpio_output(self._pin_dir, int(direction))

    def run_to_position_steps(
        self, steps, movement_abs_rel: MovementAbsRel | None = None
    ) -> StopMode:
        """runs the motor to the given position using PIO.
        Sends total step count to PIO and dynamically adjusts frequency
        for acceleration and deceleration.
        Blocks the code until finished or stopped from a different thread!

        Args:
            steps (int): amount of steps; can be negative
            movement_abs_rel (enum): whether the movement should be absolute or relative

        Returns:
            stop (enum): how the movement was finished
        """
        if self._sm is None:
            return StopMode.HARDSTOP

        print(f"cur: {self.current_pos} target: {steps} abs_rel: {movement_abs_rel}")

        if movement_abs_rel is None:
            movement_abs_rel = self.movement_abs_rel

        if movement_abs_rel == MovementAbsRel.ABSOLUTE:
            steps = steps - self.current_pos

        if steps == 0:
            return StopMode.NO

        # Set direction based on steps
        self.set_direction(Direction.CW if steps > 0 else Direction.CCW)
        steps = abs(steps)

        # Initialize movement
        self._movement_phase = MovementPhase.ACCELERATING
        self._start_pio_movement(steps)
        self._n = 0  # Reset step counter for acceleration calculations
        self._cn = self._c0  # Start with initial step interval

        # Calculate acceleration/deceleration profile
        # Steps needed to accelerate to max speed
        steps_to_max = round(
            (self._max_speed * self._max_speed) / (2.0 * self._acceleration)
        )

        # Determine if we can reach max speed
        if steps >= 2 * steps_to_max:
            # Full trapezoidal profile: accel -> cruise -> decel
            accel_steps = steps_to_max
            decel_steps = steps_to_max
            cruise_steps = steps - accel_steps - decel_steps
        else:
            # Triangular profile: accel -> decel (no cruise)
            accel_steps = steps // 2
            decel_steps = steps - accel_steps
            cruise_steps = 0

        self._tmc_logger.log(
            f"Total steps: {steps} | Accel: {accel_steps} | Cruise: {cruise_steps} | Decel: {decel_steps}",
            Loglevel.MOVEMENT,
        )

        steps_sent = 0
        soft_stop_initiated = False

        # Main loop: send data to PIO FIFO
        while steps_sent < steps:

            # Wait for FIFO space (max 4 entries)
            while self._sm.tx_fifo() >= 4:
                time.sleep_us(100)
                if self._stop != StopMode.NO:
                    break

            if self._stop == StopMode.HARDSTOP:
                self._sm.active(0)  # Immediately stop PIO
                break
            elif self._stop == StopMode.SOFTSTOP and not soft_stop_initiated:
                steps_sent = accel_steps + cruise_steps  # Jump to deceleration phase
                soft_stop_initiated = True

            # Determine current phase and calculate delay
            if steps_sent < accel_steps:
                # ACCELERATION phase - send ONE step at a time for accurate ramping
                self._movement_phase = MovementPhase.ACCELERATING
                block_steps = 1  # Single step for acceleration

                # Update step interval for next step (Equation 13)
                # Subtract from current cn to get faster
                self._n += 1
                self._cn = round(self._cn - ((2.0 * self._cn) / ((4.0 * self._n) + 1)))
                if self._cn < self._cmin:
                    self._cn = self._cmin

            elif steps_sent < accel_steps + cruise_steps:
                # CRUISE phase (constant speed) - can send larger blocks
                self._movement_phase = MovementPhase.MAXSPEED
                remaining_cruise = accel_steps + cruise_steps - steps_sent
                block_steps = min(
                    remaining_cruise, 100
                )  # Larger blocks at constant speed
                self._cn = self._cmin

            else:
                # DECELERATION phase - send ONE step at a time for accurate ramping
                self._movement_phase = MovementPhase.DECELERATING
                block_steps = 1  # Single step for deceleration

                # Decrement n and calculate new (slower) delay
                if self._n > 0:
                    self._n -= 1
                    if self._n > 0:
                        self._cn = round(
                            self._cn + ((2.0 * self._cn) / ((4.0 * self._n) + 1))
                        )
                    else:
                        self._cn = self._c0
                else:
                    self._cn = self._c0

                if self._cn > self._c0:
                    self._cn = self._c0
                self._cn = min(self._cn, self._c0)

            # Convert microseconds to milliseconds for PIO
            delay_ms = max(1, self._cn // 1000)

            # Send to PIO using PioData
            self._tmc_logger.log(
                f"Block: {block_steps} steps, delay: {delay_ms}ms, total sent: {steps_sent + block_steps}/{steps}",
                Loglevel.MOVEMENT,
            )
            pio_data = PioData(block_steps, delay_ms)
            pio_data.put(self._sm, self._pio_frequency)

            steps_sent += block_steps

        # Wait for all steps to complete
        self._tmc_logger.log(
            f"Waiting for completion: sent={steps_sent}, target={steps}, stopmode={self._stop}",
            Loglevel.MOVEMENT,
        )
        timeout_counter = 0
        while self._steps_completed < steps and self._stop == StopMode.NO:
            time.sleep_us(100)
            timeout_counter += 1
            if timeout_counter % 1000 == 0:  # Every second
                self._tmc_logger.log(
                    f"Still waiting: completed={self._steps_completed}/{steps}, sent={steps_sent}",
                    Loglevel.MOVEMENT,
                )
            if timeout_counter > 10000:  # 10 second timeout
                self._tmc_logger.log(
                    f"TIMEOUT! completed={self._steps_completed}/{steps}",
                    Loglevel.ERROR,
                )
                break

        self._tmc_logger.log(
            f"Movement complete: completed={self._steps_completed}, target={steps}",
            Loglevel.MOVEMENT,
        )

        # Don't unregister IRQ handler - it stays registered from _init_pio()
        # self._sm.irq(handler=None)
        self._movement_phase = MovementPhase.STANDSTILL

        if self._stop != StopMode.NO:
            stop_mode = self._stop
            self._stop = StopMode.NO
            return stop_mode

        return StopMode.NO

    def stop(self, stop_mode: StopMode = StopMode.HARDSTOP):
        """stop the current movement
        SOFTSTOP in PIO is delayed until the current queued blocks are done, this
        can be up to several hundred steps depending on the FIFO state.
        HARDSTOP immediately stops the PIO state machine.

        Args:
            stop_mode (enum): whether the movement should be stopped immediately or softly
        """
        super().stop(stop_mode)
