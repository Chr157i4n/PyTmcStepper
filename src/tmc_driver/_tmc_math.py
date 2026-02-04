"""TMC2209_Raspberry_Pi math library."""


def rps_to_vactual(rps, steps_per_rev: int, fclk: int = 12000000) -> int:
    """Converts rps -> vactual.

    Args:
        rps (float): revolutions per second
        steps_per_rev (int): steps per revolution
        fclk (int): clock speed of the tmc (Default value = 12000000)

    Returns:
        vactual (int): value for vactual
    """
    return int(round(rps / (fclk / 16777216) * steps_per_rev))


def vactual_to_rps(vactual: int, steps_per_rev: int, fclk: int = 12000000) -> float:
    """Converts vactual -> rps.

    Args:
        vactual (int): value for VACTUAL
        steps_per_rev (int): steps per revolution
        fclk (int): clock speed of the tmc (Default value = 12000000)

    Returns:
        rps (float): revolutions per second
    """
    return vactual * (fclk / 16777216) / steps_per_rev


def rps_to_steps(rps: float, steps_per_rev: int) -> int:
    """Converts rps -> steps/second.

    Args:
        rps (float): revolutions per second
        steps_per_rev (int): steps per revolution

    Returns:
        steps (int): steps per second
    """
    return int(round(rps * steps_per_rev))


def steps_to_rps(steps: int, steps_per_rev: int) -> float:
    """Converts steps/second -> rps."""
    return steps / steps_per_rev


def rps_to_tstep(rps: float, steps_per_rev: int, mres: int) -> int:
    """Converts rps -> tstep.

    Args:
        rps (float): revolutions per second
        steps_per_rev (int): steps per revolution
        mres (int): µstep resolution

    Returns:
        tstep (int): time per step
    """
    return int(round(12000000 / (rps_to_steps(rps, steps_per_rev) * 256 / mres)))


def steps_to_tstep(steps: int, mres: int) -> int:
    """Converts steps/second -> tstep."""
    if steps == 0:
        return 0
    return int(round(12000000 / (steps * 256 / mres)))


def constrain(val: int, min_val: int, max_val: int) -> int:
    """Constrains a value between a min and a max.

    Args:
        val (int): value that should be constrained
        min_val (int): minimum value
        max_val (int): maximum value

    Returns:
        int: constrained value
    """
    if val < min_val:
        return min_val
    if val > max_val:
        return max_val
    return val


def mean(data) -> int:
    """Calculates the mean of a list of numbers."""
    count = len(data)
    if count == 0:
        return 0

    total = sum(data)

    return total // count
