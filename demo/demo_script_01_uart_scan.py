"""
debug file for debuging the UART connection
"""

from tmc_driver import TmcLogger, Loglevel, Board, tmc_gpio
from tmc_driver import tmc_2240
from tmc_driver import tmc_2209
from tmc_driver.com._tmc_com_uart import TmcComUart


# -----------------------------------------------------------------------
# initiate the TmcCom class
# -----------------------------------------------------------------------
UART_PORT = {
    Board.RASPBERRY_PI: "/dev/serial0",
    Board.RASPBERRY_PI5: "/dev/ttyAMA0",
    Board.NVIDIA_JETSON: "/dev/ttyTHS1",
}

tmc_com = TmcComUart(UART_PORT.get(tmc_gpio.BOARD, "/dev/serial0"))

tmc_com.tmc_logger = TmcLogger(Loglevel.NONE)
tmc_com.init()

# -----------------------------------------------------------------------
# scan for devices and test which driver it could be
# -----------------------------------------------------------------------
res = tmc_com.scan_for_devices([tmc_2209.Ioin, tmc_2240.Ioin])

for addr, driver in res:
    print(f"Driver found at address {addr}", end="")
    if driver is not None:
        print(f": maybe {driver}")
    else:
        print("")
