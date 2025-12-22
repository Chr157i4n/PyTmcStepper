# PyTmcStepper

[![PyPI python version PyTmcStepper](https://badgen.net/pypi/python/PyTmcStepper)](https://pypi.org/project/PyTmcStepper)
[![PyPI version PyTmcStepper](https://badgen.net/pypi/v/PyTmcStepper)](https://pypi.org/project/PyTmcStepper)
[![PyPI downloads PyTmcStepper](https://img.shields.io/pypi/dm/PyTmcStepper)](https://pypi.org/project/PyTmcStepper)
[![GitHub issues](https://img.shields.io/github/issues/Chr157i4n/PyTmcStepper.svg)](https://GitHub.com/Chr157i4n/PyTmcStepper/issues/)

\
\
This is a Python libary to drive a stepper motor with a Trinamic stepper driver and a single board computer like a Raspberry Pi.

This code is still experimental, so use it on your own risk.

This library is programmed in pure Python. The performance of Python is not good enough to drive the motor with high speed.
So if you move the motor with high speed using this library the motor will lose steps.

Tested on a [Bigtreetech TMC2209 V1.2](https://github.com/bigtreetech/BIGTREETECH-Stepper-Motor-Driver/tree/master/TMC2209/V1.2) and [Bigtreetech TMC2209 V1.3](https://github.com/bigtreetech/BIGTREETECH-Stepper-Motor-Driver/tree/master/TMC2209/V1.3).

It has a rSense of 110 mOhm and it uses one Pin (PDN_UART) for UART RX and TX.
So the PDN_UART-Pin needs to be connected to the Raspberrry Pis RX-Pin directly and to the TX-Pin with an 1kOhm resistor.
You can read more about this in the datasheet from Trinamic.

Because the TMC2209 uses one shared pin for transmit and receive in the UART communication line, the Raspberry Pi also receives what it sends.
Well, the Pi receives 4 bytes from itself and 8 bytes from the driver. So the Pi receives a total of 12 bytes and only the last 8 are the reply, of which only 4 are data bytes.

The Documentation of the TMC2209 can be found here:
[TMC2209 - Datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/TMC2209_datasheet_rev1.09.pdf)

The code is also available on [PyPI](https://pypi.org/project/PyTmcStepper).

## Installation (on Raspberry Pi)

### Installation with PIP

```shell
pip3 install PyTmcStepper
```

### Installation with GIT

- clone this repo to your Raspberry Pi using

    ```shell
    git clone https://github.com/Chr157i4n/PyTmcStepper
    ```

- install the required modules

    ```shell
    pip3 install RPi.GPIO pyserial
    ```

- enable the serial port in

    ```shell
    sudo raspi-config
    ```

### Board Support

The following table shows the supported boards and which libraries for GPIO access is beeing used for that board.

Library     | Installation Parameter    | Boards
----------- | ------------------------- | -----------
RPi.GPIO    | RASPBERRY_PI              | Pi4, Pi3 etc.
gpiozero    | RASPBERRY_PI5             | Pi5
Jetson.GPIO | NVIDIA_JETSON             | Nvidia Jetson
pheriphery  | LUCKFOX_PICO              | Luckfox Pico
OPi.GPIO    | ORANGE_PI                 | Orange Pi
pyftdi      | -                         | Windows/Linux
machine     | -                         | Pico, Pico2, ESP32, etc.

Those libraries are needed for this library to work. You can either install the correct library yourself.
You can also install the needed GPIO library by specifing the Installation Parameter while installing this library:

```shell
pip3 install PyTmcStepper[RASPBERRY_PI]
```

## Driver Support

The currently supported drivers are:

Driver  | Interface
--      | --
TMC2208 | UART
TMC2209 | UART
TMC2240 | SPI/UART

## Submodules

with V0.7 the code for enabling the motor current output and the code for controling the motion of the drivers
is split into their own classes to be able to support the diverse methods.

### EnableControl

The EnableControl module controls the motor current output. It has a function `set_motor_enabled` with one boolean parameter. This function is used to enable or disable the Motor current output.

EnableControl   | Class                                                                 | Driver    | Notes
--              | --                                                                    | --        | --
Pin             | [TmcEnableControlPin](src/tmc_driver/enable_control/_tmc_ec_pin.py)   | all       | the EN Pin of the Driver needs to be connected to a GPIO of the Pi
TOff            | [TmcEnableControlToff](src/tmc_driver/enable_control/_tmc_ec_toff.py) | all       | the EN Pin needs to be connected to GND.<br />On the TMC2209 this enables current Output on Startup!<br />On the TMC2240 this works fine, because TOff is per default 0 (off).

### MotionControl

The MotionControl module controls the motion of the motor. Before a movement the motor current output needs to be enabled by the [EnableControl](#enablecontrol) module.

MotionControl   | Class                                                                                 | Driver    | Notes
--              | --                                                                                    | --        | --
STEP/DIR        | [TmcMotionControlStepDir](src/tmc_driver/motion_control/_tmc_mc_step_dir.py)          | all       | the STEP and DIR pin of the driver must each be connected to a GPIO of the Pi
STEP/REG        | [TmcMotionControlStepReg](src/tmc_driver/motion_control/_tmc_mc_step_reg.py)          | all       | only the STEP pin needs to be connected to a GPIO of the Pi.<br />The direction is controlled via the Register.
VACTUAL         | [TmcMotionControlVActual](src/tmc_driver/motion_control/_tmc_mc_vactual.py)           | TMC220x   | the Direction and Speed is controlled via Register. But VActual does only allow setting a speed and therefore cannot control positioning of the Motor.
STEP_PWM/DIR    | [TmcMotionControlStepPwmDir](src/tmc_driver/motion_control/_tmc_mc_step_pwm_dir.py)   | all       | In contrast to STEP/DIR, the step pin is controlled by PWM. This reduces the load on the CPU, but does not allow precise positioning (similar to the VACTUAL).<br />STEP must be connected to a PWM-capable pin for this purpose

Further methods of controlling the motion of a motor could be:

- using the built in Motion Controller of the TMC5130
- via a µC which controlls the Motor
- highperformance Step/Dir Library written in a compiled language (C/C++)

### Com

Com             | Class                                                     | Driver    | Notes
--              | --                                                        | --        | --
UART            | [TmcComUart](src/tmc_driver/com/_tmc_com_uart.py)         | all       | Communication via UART (RX, TX). See [Wiring](#uart)<br />[pyserial](https://pypi.org/project/pyserial) needs to be installed
SPI             | [TmcComSpi](src/tmc_driver/com/_tmc_com_spi.py)           | TMC2240   | Communication via SPI (MOSI, MISO, CLK, CS). See [Wiring](#spi)<br />[spidev](https://pypi.org/project/spidev) needs to be installed
SPI over FT232H | [TmcComSpiFtdi](src/tmc_driver/com/_tmc_com_spi_ftdi.py)  | TMC2240   | Communication via SPI using a FT232H. This can be used on any OS.<br />[pyftdi](https://pypi.org/project/pyftdi) needs to be installed

## Wiring

![wiring diagram](docs/images/wiring_diagram.png)

Pin TMC | Color     | connect to                    | Function
--      | --        | --                            | --
VDD     |           | 3,3V of Raspberry Pi          | recommended, for forcing the TMC to use 3,3V logic level
GND     | BLACK     | GND of Raspberry Pi           | GND for VDD and Signals
VM      | RED       | 12V or 24V of power supply    | power for the motor
GND     | BLACK     | GND of power supply           | power for the motor
EN      | RED       | GPIO21 of Raspberry Pi        | enable the motor output
STEP    | GREEN     | GPIO16 of Raspberry Pi        | moves the motor one step per pulse
DIR     | WHITE     | GPIO20 of Raspberry Pi        | set the direction of the motor
DIAG    | ORANGE    | GPIO26 of Raspberry Pi        | optional, for StallGuard

The GPIO pins can be specific when initiating the class.
If you test this on a breadboard, make sure to cut off the bottomside of the pins (Vref and DIAG) next to the EN pin, so that they are not shorted trough the breadboard.

### UART

Pin TMC                     | Color     | connect to            | Function
--                          | --        | --                    | --
TX or PDN_UART with 1kOhm   | YELLOW    | TX of Raspberry Pi    | send data to TMC via UART
RX or PDN_UART directly     | YELLOW    | RX of Raspberry Pi    | receive data from TMC via UART

### SPI

Pin TMC | Color | connect to                        | Function
--      | --    | --                                | --
MOSI    |       | MOSI                              | Data from Pi to TMC
MISO    |       | MOSI                              | Data from TMC to Pi
SPI-CLK |       | CLK                               | Clock for SPI
CS      |       | SPI CE0 (for the demo scripts)    | Chipselect (2nd parameter of TmcComSpi "spi_dev")

## Demo scripts

You can run the demo scripts files from the main directory with

```shell
python3 -m demo.demo_script_01_uart_connection
```

### [demo_script_01_uart_connection.py](demo/demo_script_01_uart_connection.py)

This only communicates with the TMC driver over UART. It should set some settings in the driver and then outputs the settings.
When it outputs ```TMC2209: UART Communication Error```, you need to check the UART-connection.

### [demo_script_02_pin_connection.py](demo/demo_script_02_pin_connection.py)

This script enables the raspberry GPIO output for the dir, en and step pin and then checks the TMC driver register,
whether the driver sees them as HIGH or LOW. Because the enabled pin is activated for a short time, the motor current ouput
will be also activated in this script for a short time.
This script should output:
Pin DIR:        OK
Pin STEP:       OK
Pin EN:         OK
if not, check the connection of the pin.

### [demo_script_03_basic_movement.py](demo/demo_script_03_basic_movement.py)

This script shows the different functions available to move the motors.
The motor is moved 4 times one revolution back and forth.

### [demo_script_04_stallguard.py](demo/demo_script_04_stallguard.py)

In this script the stallguard feature of the TMC2209 is being setup.
A funtion will be called, if the driver detects a stall. The function stops the current movement.
The motor will be moved 10 revolutions. If the movement is finished unhindered, the script outputs ```Movement finished successfully```.
If you block the motor with pliers or something similar, the the motor will stop and the script outputs ```StallGuard!``` and ```Movement was not completed```

### [demo_script_05_vactual.py](demo/demo_script_05_vactual.py)

VACTUAL enables the motor to be moved via the COM interface (UART) without additional GPIOs. The motor speed is transmitted as a value in +-(2^23)-1 [µsteps / t] via the COM interface.

### [demo_script_06_multiple_drivers.py](demo/demo_script_06_multiple_drivers.py)

Multiple drivers can be addressed via UART by setting different addresses with the MS1 and MS2 pins.
Simultaneous movement of multiple motors can be done with threaded movement.
When using SPI different Drivers are accessed via the Chip Select pin.

### [demo_script_07_threads.py](demo/demo_script_07_threads.py)

In this script, the movement of a stepper with threads is shown. This can be used to do other task while moving a motor, or to move several motors simultaneous.

### [demo_script_08_log_to_file.py](demo/demo_script_08_log_to_file.py)

This script shows how you can alter the formatting of the TMC2209 log messages and redirect the log output to a file called `tmc2209_log_file.log` that will be created in the current directory.

\
\
For me these baudrates worked fine: 19200, 38400, 57600, 115200, 230400, 460800, 576000.

If the TMC2209 driver is connected to the Vmotor, the internal voltage regulator will create the Vio for the chip.
So you don't need to connect anything to the Vio pin of the driver.

### Micropython

The lib is also compatible with MicroPython. For using it with Micropython the VSCode addon [MicroPico](https://marketplace.visualstudio.com/items?itemName=paulober.pico-w-go) is used. Use the Upload Project function to upload the src folder and the needed lib folder.

the needed libs, which are not builtin in Micropython are:

Lib         | available on MIP
--          | --
abc         | yes
enum        | no
threading   | yes
types       | yes

You can also use MicroPico to run the demo script by opening one and then pressing Run on the bottom left corner

## Usage

The library currently uses functions to access the TMC registers, but Python properties for internal getters/setters.

```python
from tmc_driver.tmc_2209 import *
tmc = Tmc2209(TmcEnableControlPin(21), TmcMotionControlStepDir(16, 20), TmcComUart("/dev/serial0"))

tmc.set_direction_reg(False)
tmc.set_current(300)
tmc.set_interpolation(True)
tmc.set_spreadcycle(False)
tmc.set_microstepping_resolution(2)
tmc.set_internal_rsense(False)

tmc.acceleration_fullstep = 1000
tmc.max_speed_fullstep = 250

tmc.set_motor_enabled(True)

tmc.run_to_position_steps(400)
tmc.run_to_position_steps(0)

tmc.set_motor_enabled(False)
```

## Troubleshoot

If you have questions please check out the [Wiki](https://github.com/Chr157i4n/PyTmcStepper/wiki) and the other issues.

If you encounter any problems, feel free to open an issue (ENG/GER).
Please don't send any E-Mails to me. Pls use Github, so that i don't need to answer the same question multiple times.
I reserve the right not to answer E-Mails.

Problem                                                                                 | Solution
--                                                                                      | --
FileNotFoundError: [Errno 2] No such file or directory: '/dev/serial0'                  | depending on your Raspberry Pi version, you need to enable the Serial Port <br /> run `sudo raspi-config` in your terminal. <br /> there go to '3 Interface Options' -> 'P3 Serial Port' <br /> Would you like a login shell to be accessible over serial? No <br /> Would you like the serial port hardware to be enabled? Yes <br /> Finish and then reboot
PermissionError: [Errno 13] <br /> Permission denied: '/dev/serial0'                    | you need to give the permission to acces the Serial Port to your current user <br /> You may need to add your user (pi) to the dialout group with `sudo usermod -a -G dialout pi` and then relog. <br /> If that does not work, make sure that your user has read/write permissions on the dev file `/dev/serial0` by calling `sudo chmod 660 /dev/serial0`.
"TMC2209: UART Communication Error"                                                     | You can use the 'debug_script_01_uart_connection' script to get a better reading on the received bytes and troubleshoot your problem
"TMC2209: UART Communication Error: 0 data bytes \| 4 total bytes"                      | only 4 total bytes received indicates, that the Raspberry Pi receives its own data, but nothing from the TMC driver. This happens if RX and TX are connected properly, but the TMC driver has no power
"TMC2209: UART Communication Error: 0 data bytes \| 0 total bytes"                      | 0 total bytes received indicates, a problem with your wiring or your Raspberry Pi. This happens if TX is not connected
"TMC2209: UART Communication Error: 4 data bytes \| 12 total bytes"                     | this indicates, the Raspberry Pi received only zeroes. This happens if only RX is connected and TX not
"the Raspberry Pi received only the sended bits" or<br /> inconsistent received bits    | Make sure the UART ist properly connected to the TMC driver and the driver is powered and working. <br /> Make sure login shell (console) over serial is disabled.

![wiring photo](docs/images/wiring_photo.jpg)

## Acknowledgements

The code to run the stepper motor is based on the code of the [AccelStepper Library from Mike McCauley](http://www.airspayce.com/mikem/arduino/AccelStepper).

The code for the UART communication is based on this [code from troxel](https://github.com/troxel/TMC_UART).

For the implementation of Python-stdlib for micropython [micropython-lib](https://github.com/micropython/micropython-lib)

My goal is to make a library, that can run a stepper motor with a TMC2209 stepper driver and can write the setting in the register of the TMC2209, entirely in Python.
The main focus for this are Test setups, as Python is not fast enough for high motor speeds.

## Feedback/Contributing

If you encounter any problem, feel free to open an issue on the Github [issue page](https://github.com/Chr157i4n/PyTmcStepper/issues).
Feedback will keep this project growing and I encourage all suggestions.
Feel free to submit a pull request on the dev branch.
