#pylint: disable=unused-import
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

    # Board mapping: (module_path, class_name, Board enum, module_name, install_link)
    board_mapping = {
        "raspberry pi 5": ("._tmc_gpio_board_gpiozero", "GpiozeroWrapper", Board.RASPBERRY_PI5, "gpiozero", "https://gpiozero.readthedocs.io/en/stable/installing.html"),
        "raspberry": ("._tmc_gpio_board", "RPiGPIOWrapper", Board.RASPBERRY_PI, "RPi.GPIO", "https://sourceforge.net/p/raspberry-gpio-python/wiki/install"),
        "jetson": ("._tmc_gpio_board", "JetsonGPIOWrapper", Board.NVIDIA_JETSON, "jetson-gpio", "https://github.com/NVIDIA/jetson-gpio"),
        "luckfox": ("._tmc_gpio_board_periphery", "peripheryWrapper", Board.LUCKFOX_PICO, "periphery", "https://github.com/vsergeev/python-periphery"),
        "orange": ("._tmc_gpio_board", "OPiGPIOWrapper", Board.ORANGE_PI, "OPi.GPIO", "https://github.com/rm-hull/OPi.GPIO")
    }

    # Determine the board and instantiate the appropriate GPIO class
    def get_board_model_name():
        """get board model name from /proc/device-tree/model file"""
        if not exists('/proc/device-tree/model'):
            return "mock"
        with open('/proc/device-tree/model', encoding="utf-8") as f:
            return f.readline().lower()

    def handle_module_not_found_error(err, board_name, module_name, install_link):
        """handle module not found error"""
        dependencies_logger.log(
            (f"ModuleNotFoundError: {err}\n"
             f"Board is {board_name} but module {module_name} isn't installed.\n"
             f"Follow the installation instructions in the link below to resolve the issue:\n"
             f"{install_link}\n"
             "Exiting..."),
            Loglevel.ERROR)
        raise err

    def handle_import_error(err, board_name, module_name, install_link):
        """handle import error"""
        dependencies_logger.log(
            (f"ImportError: {err}\n"
             f"Board is {board_name} but module {module_name} isn't installed.\n"
             f"Follow the installation instructions in the link below to resolve the issue:\n"
             f"{install_link}\n"
             "Exiting..."),
            Loglevel.ERROR)
        raise err

    def initialize_gpio(force_lib=None):
        """initialize GPIO"""
        from importlib import import_module

        model = get_board_model_name()
        dependencies_logger.log(f"Board model: {model}", Loglevel.INFO)

        if model == "mock":
            from ._tmc_gpio_board import MockGPIOWrapper
            return MockGPIOWrapper(), Board.UNKNOWN

        for key, (module_path, class_name, board_enum, module_name, install_link) in board_mapping.items():
            if (key in model and force_lib is None) or (force_lib == module_name):
                try:
                    # Import module dynamically only when needed
                    module = import_module(module_path, package=__name__)
                    wrapper_class = getattr(module, class_name)
                    return wrapper_class(), board_enum
                except ModuleNotFoundError as err:
                    handle_module_not_found_error(err, key.capitalize(), module_name, install_link)
                except ImportError as err:
                    handle_import_error(err, key.capitalize(), module_name, install_link)

        dependencies_logger.log(
            "The board is not recognized. Trying import default RPi.GPIO module...",
            Loglevel.INFO)
        try:
            from ._tmc_gpio_board import RPiGPIOWrapper
            return RPiGPIOWrapper(), Board.UNKNOWN
        except ImportError:
            from ._tmc_gpio_board import MockGPIOWrapper
            return MockGPIOWrapper(), Board.UNKNOWN

    tmc_gpio, BOARD = initialize_gpio()
