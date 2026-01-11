# pylint: disable=too-many-instance-attributes
# pylint: disable=unused-import

"""
Register module
"""

from ..tmc_logger import TmcLogger, Loglevel
from ..com._tmc_com import TmcCom


class TmcRegField:
    """Register field class"""

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-positional-arguments
    # pylint: disable=too-few-public-methods

    def __init__(
        self,
        name: str,
        pos: int,
        mask: int,
        reg_class: type,
        conv_func,
        unit: str,
        clear_value: int | None = None,
        signed: bool = False,
    ):
        """Constructor

        Args:
            name (str): field name
            pos (int): bit position
            mask (int): bit mask
            reg_class (type): type of the field value
            conv_func: conversion function name (optional)
            unit (str): unit string for display
            clear_value (int|None): value to set when clearing (optional)
            signed (bool): whether the field is signed (two's complement)
        """
        self.name = name
        self.pos = pos
        self.mask = mask
        self.reg_class = reg_class
        self.conv_func = conv_func
        self.unit = unit
        self.clear_value = clear_value
        self.signed = signed

    def get_bit_width(self) -> int:
        """Get the bit width of this field based on the mask"""
        width = 0
        mask = self.mask
        while mask:
            width += 1
            mask >>= 1
        return width


class TmcReg:
    """Register class"""

    ADDR: int
    _REG_MAP: tuple[TmcRegField, ...] = ()
    _data_int: int
    _flags: dict | None

    @property
    def reg_map(self) -> tuple[TmcRegField, ...]:
        """returns the register map"""
        return self._REG_MAP

    @property
    def data_int(self) -> int:
        """returns the raw register data as integer"""
        return self._data_int

    @property
    def flags(self) -> dict | None:
        """returns the flags from the last read operation"""
        return self._flags

    def __init__(self, tmc_com: TmcCom):
        """Constructor"""

        self._tmc_com = tmc_com

        self.deserialise(0)

    def deserialise(self, data: int):
        """Deserialises the register value

        Args:
            data (int): register value
        """
        for reg in self._REG_MAP:
            value = data >> reg.pos & reg.mask
            # Convert from two's complement if signed
            if reg.signed:
                bit_width = reg.get_bit_width()
                if value >= (1 << (bit_width - 1)):
                    value -= 1 << bit_width
            setattr(self, reg.name, reg.reg_class(value))

    def serialise(self) -> int:
        """Serialises the object to a register value

        Returns:
            int: register value
        """
        data = 0

        for reg in self._REG_MAP:
            value = getattr(self, reg.name)
            int_value = int(value)
            # Convert to two's complement if signed and negative
            if reg.signed and int_value < 0:
                bit_width = reg.get_bit_width()
                int_value = (1 << bit_width) + int_value
            data |= (int_value & reg.mask) << reg.pos

        return data

    def __str__(self) -> str:
        """string representation of this register"""
        out_string = f"{self.__class__.__name__.upper()} | {hex(self.ADDR)} | {bin(self._data_int)}\n"
        for reg in self._REG_MAP:
            value = getattr(self, reg.name)
            out_string += f"  {reg.name:<20}{value:<10}"
            if reg.conv_func is not None:
                out_string += f"{getattr(self, reg.conv_func, '')} {reg.unit}"
            out_string += "\n"
        return out_string

    def log(self, logger: TmcLogger | None):
        """log this register"""
        if logger is None:
            return
        logger.log(str(self), Loglevel.INFO)

    def read(self) -> tuple[int, dict | None]:
        """read this register"""
        data, flags = self._tmc_com.read_int(self.ADDR)

        self._data_int = data
        self._flags = flags

        self.deserialise(data)
        return data, flags

    def write(self):
        """write this register"""
        data = self.serialise()
        self._tmc_com.write_reg(self.ADDR, data)

    def write_check(self):
        """write this register and checks that the write was successful"""
        data = self.serialise()
        self._tmc_com.write_reg_check(self.ADDR, data)

    def modify(self, name: str, value):
        """modify a register value

        Args:
            name (str): register name
            value: new value
        """
        self.read()
        setattr(self, name, value)
        self.write_check()

    def get(self, name: str):
        """get a register value

        Args:
            name (str): register name

        Returns:
            value: register value
        """
        self.read()
        return getattr(self, name)

    def clear(self):
        """clear this register (set to 0)"""
        self._data_int = 0
        for reg in self._REG_MAP:
            if reg.clear_value is not None:
                setattr(self, reg.name, reg.reg_class(reg.clear_value))
        self.write_check()

    def clear_verify(self) -> bool:
        """clear this register and verify that it was cleared"""
        self.clear()
        self.read()
        for reg in self._REG_MAP:
            if reg.clear_value is not None:
                value = getattr(self, reg.name)
                if int(value) != reg.reg_class(0):
                    return False
        return True
