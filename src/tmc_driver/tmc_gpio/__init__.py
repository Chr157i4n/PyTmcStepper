#pylint: disable=unused-import
#pylint: disable=import-outside-toplevel
"""
Module for GPIO handling across different boards and libraries.
Automatically detects the board type and imports the appropriate GPIO library.
"""

import sys
from enum import Enum, IntEnum
from .._tmc_logger import TmcLogger, Loglevel
from ._tmc_gpio_board_base import *


MICROPYTHON = sys.implementation.name == "micropython"

# ------------------------------
# LIB           | BOARD
# ------------------------------
# RPi.GPIO      | Pi4, Pi3 etc.
# Jetson.GPIO   | Nvidia Jetson
# gpiozero      | Pi5
# pheriphery    | Luckfox Pico
# OPi.GPIO      | Orange Pi
# machine       | MicroPython
# ------------------------------

if MICROPYTHON:
    from ._tmc_gpio_board_micropython import MicroPythonGPIOWrapper

    tmc_gpio = MicroPythonGPIOWrapper()
    BOARD = Board.MICROPYTHON
else:
    from os.path import exists
    from ._tmc_gpio_board_ftdi import FtdiWrapper

    # Board mapping: (module_path, class_name, Board enum)
    board_mapping = {
        "raspberry pi 5": ("._tmc_gpio_board_gpiozero", "GpiozeroWrapper", Board.RASPBERRY_PI5),
        "raspberry": ("._tmc_gpio_board_rpi_gpio", "RPiGPIOWrapper", Board.RASPBERRY_PI),
        "jetson": ("._tmc_gpio_board_rpi_gpio", "JetsonGPIOWrapper", Board.NVIDIA_JETSON),
        "luckfox": ("._tmc_gpio_board_periphery", "peripheryWrapper", Board.LUCKFOX_PICO),
        "orange": ("._tmc_gpio_board_rpi_gpio", "OPiGPIOWrapper", Board.ORANGE_PI)
    }

    # Determine the board and instantiate the appropriate GPIO class
    def get_board_model_name():
        """get board model name from /proc/device-tree/model file"""
        if not exists('/proc/device-tree/model'):
            return "mock"
        with open('/proc/device-tree/model', encoding="utf-8") as f:
            return f.readline().lower()

    def initialize_gpio():
        """initialize GPIO"""
        from importlib import import_module

        model = get_board_model_name()
        dependencies_logger.log(f"Board model: {model}", Loglevel.INFO)

        if model == "mock":
            from ._tmc_gpio_board_rpi_gpio import MockGPIOWrapper
            return MockGPIOWrapper(), Board.UNKNOWN

        for key, (module_path, class_name, board_enum) in board_mapping.items():
            if key in model:
                # Import module dynamically only when needed
                module = import_module(module_path, package=__name__)
                wrapper_class = getattr(module, class_name)
                return wrapper_class(), board_enum

        dependencies_logger.log(
            "The board is not recognized. Trying import default RPi.GPIO module...",
            Loglevel.INFO)
        try:
            from ._tmc_gpio_board_rpi_gpio import RPiGPIOWrapper
            return RPiGPIOWrapper(), Board.UNKNOWN
        except ImportError:
            from ._tmc_gpio_board_rpi_gpio import MockGPIOWrapper
            return MockGPIOWrapper(), Board.UNKNOWN

    tmc_gpio, BOARD = initialize_gpio()
