# pylint: disable=too-many-instance-attributes
# pylint: disable=unused-import

"""
Register module
"""

from .._tmc_logger import TmcLogger, Loglevel


class TmcComStub:
    """Stub for type hints"""

    def read_int(self, address: int):
        """Stub for type hints"""
        raise NotImplementedError

    def write_reg(self, address: int, data: int):
        """Stub for type hints"""
        raise NotImplementedError

    def write_reg_check(self, address: int, data: int):
        """Stub for type hints"""
        raise NotImplementedError


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
    ):
        """Constructor"""
        self.name = name
        self.pos = pos
        self.mask = mask
        self.reg_class = reg_class
        self.conv_func = conv_func
        self.unit = unit


class TmcReg:
    """Register class"""

    ADDR: int
    _REG_MAP: tuple[TmcRegField, ...] = ()
    _data_int: int
    _flags: dict

    @property
    def reg_map(self) -> tuple[TmcRegField, ...]:
        """returns the register map"""
        return self._REG_MAP

    @property
    def data_int(self) -> int:
        """returns the raw register data as integer"""
        return self._data_int

    @property
    def flags(self) -> dict:
        """returns the flags from the last read operation"""
        return self._flags

    def __init__(self, tmc_com: TmcComStub):
        """Constructor"""
        self._data_int: int
        self._flags: dict

        self._tmc_com = tmc_com

        self.deserialise(0)

    def deserialise(self, data: int):
        """Deserialises the register value

        Args:
            data (int): register value
        """
        for reg in self._REG_MAP:
            value = data >> reg.pos & reg.mask
            setattr(self, reg.name, reg.reg_class(value))

    def serialise(self) -> int:
        """Serialises the object to a register value

        Returns:
            int: register value
        """
        data = 0

        for reg in self._REG_MAP:
            value = getattr(self, reg.name)
            data |= (int(value) & reg.mask) << reg.pos

        return data

    def log(self, logger: TmcLogger | None):
        """log this register"""
        if logger is None:
            return
        logger.log(
            f"{self.__class__.__name__.upper()} | {hex(self.ADDR)} | {bin(self._data_int)}"
        )

        for reg in self._REG_MAP:
            value = getattr(self, reg.name)
            log_string = f"  {reg.name:<20}{value:<10}"
            if reg.conv_func is not None:
                log_string += f"{getattr(self, reg.conv_func, '')} {reg.unit}"
            logger.log(log_string, Loglevel.INFO)

    def read(self) -> tuple[int, dict]:
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
