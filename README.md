# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/Chr157i4n/PyTmcStepper/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                               |    Stmts |     Miss |   Cover |   Missing |
|------------------------------------------------------------------- | -------: | -------: | ------: | --------: |
| src/tmc\_driver/\_\_init\_\_.py                                    |       18 |        0 |    100% |           |
| src/tmc\_driver/\_tmc\_exceptions.py                               |        5 |        0 |    100% |           |
| src/tmc\_driver/\_tmc\_math.py                                     |       26 |        0 |    100% |           |
| src/tmc\_driver/\_tmc\_stallguard.py                               |      125 |       25 |     80% |50, 54, 61, 65-72, 80, 141-151, 189, 235, 237, 267, 281, 318 |
| src/tmc\_driver/\_tmc\_stepperdriver.py                            |       72 |       10 |     86% |17-18, 147, 183, 200, 206-210 |
| src/tmc\_driver/\_tmc\_validation.py                               |        5 |        0 |    100% |           |
| src/tmc\_driver/\_tmc\_xxxx.py                                     |      180 |       78 |     57% |143-147, 157, 173, 201-202, 210, 218-219, 227, 235-236, 244, 269, 320-323, 352-353, 365-372, 378-389, 397-398, 416-451, 459-479, 483-489 |
| src/tmc\_driver/com/\_\_init\_\_.py                                |       28 |       24 |     14% |33-34, 40-68 |
| src/tmc\_driver/com/\_tmc\_com.py                                  |       54 |        2 |     96% |    40, 90 |
| src/tmc\_driver/com/\_tmc\_com\_spi.py                             |       28 |        7 |     75% |     48-60 |
| src/tmc\_driver/com/\_tmc\_com\_spi\_base.py                       |       56 |       13 |     77% |75, 77, 79, 81, 150-159 |
| src/tmc\_driver/com/\_tmc\_com\_spi\_circuitpython.py              |       40 |       40 |      0% |    10-113 |
| src/tmc\_driver/com/\_tmc\_com\_spi\_ftdi.py                       |       13 |       13 |      0% |      7-48 |
| src/tmc\_driver/com/\_tmc\_com\_spi\_micropython.py                |       31 |       31 |      0% |     11-99 |
| src/tmc\_driver/com/\_tmc\_com\_uart.py                            |       46 |       12 |     74% |41-59, 62, 68, 85 |
| src/tmc\_driver/com/\_tmc\_com\_uart\_base.py                      |      166 |       85 |     49% |81, 83, 93, 120, 122, 128, 140, 147, 171, 173, 189-190, 218, 227-230, 235, 252-347, 363-386 |
| src/tmc\_driver/com/\_tmc\_com\_uart\_circuitpython.py             |       45 |       45 |      0% |    11-127 |
| src/tmc\_driver/com/\_tmc\_com\_uart\_micropython.py               |       43 |       43 |      0% |    12-115 |
| src/tmc\_driver/enable\_control/\_\_init\_\_.py                    |       16 |       12 |     25% |30-31, 36-48 |
| src/tmc\_driver/enable\_control/\_tmc\_ec.py                       |       22 |        1 |     95% |        40 |
| src/tmc\_driver/enable\_control/\_tmc\_ec\_pin.py                  |       26 |        1 |     96% |        17 |
| src/tmc\_driver/enable\_control/\_tmc\_ec\_toff.py                 |       12 |        0 |    100% |           |
| src/tmc\_driver/motion\_control/\_\_init\_\_.py                    |       40 |       36 |     10% |45-46, 52-96 |
| src/tmc\_driver/motion\_control/\_tmc\_mc.py                       |      137 |       12 |     91% |61, 66, 87, 92-93, 98, 113, 118, 123, 128, 158, 236 |
| src/tmc\_driver/motion\_control/\_tmc\_mc\_int\_ramp\_generator.py |      118 |       92 |     22% |34-37, 42-45, 50-53, 58-61, 65-66, 74-76, 85-118, 122, 131-141, 145-164, 183-218 |
| src/tmc\_driver/motion\_control/\_tmc\_mc\_step\_dir.py            |      194 |       23 |     88% |42, 47-50, 55, 76, 81-90, 95, 100, 105, 110, 173, 233, 274, 288, 383, 397 |
| src/tmc\_driver/motion\_control/\_tmc\_mc\_step\_pwm\_dir.py       |       37 |       21 |     43% |22, 27-29, 43-44, 50-70, 76-78 |
| src/tmc\_driver/motion\_control/\_tmc\_mc\_step\_reg.py            |       17 |        0 |    100% |           |
| src/tmc\_driver/motion\_control/\_tmc\_mc\_vactual.py              |       83 |       35 |     58% |28, 37-38, 115, 118, 131-162, 183, 185, 203, 212, 221 |
| src/tmc\_driver/platform\_utils.py                                 |       10 |        2 |     80% |    13, 15 |
| src/tmc\_driver/reg/\_\_init\_\_.py                                |        0 |        0 |    100% |           |
| src/tmc\_driver/reg/\_tmc220x\_reg.py                              |       61 |        1 |     98% |       197 |
| src/tmc\_driver/reg/\_tmc224x\_reg.py                              |       98 |       12 |     88% |71-81, 315 |
| src/tmc\_driver/reg/\_tmc2209\_reg.py                              |       14 |        0 |    100% |           |
| src/tmc\_driver/reg/\_tmc5160\_reg.py                              |      121 |        8 |     93% |71-77, 457 |
| src/tmc\_driver/reg/\_tmc\_reg.py                                  |       98 |       21 |     79% |72, 77, 82, 103, 119-120, 127-134, 138-140, 154-155, 182-183 |
| src/tmc\_driver/reg/\_tmc\_shared\_regs.py                         |       40 |        0 |    100% |           |
| src/tmc\_driver/tmc\_220x.py                                       |      121 |       24 |     80% |111-112, 130-131, 153-154, 167-177, 311-312, 350-353, 361-362, 370-371, 382-383 |
| src/tmc\_driver/tmc\_2208.py                                       |        3 |        0 |    100% |           |
| src/tmc\_driver/tmc\_2209.py                                       |       15 |        0 |    100% |           |
| src/tmc\_driver/tmc\_2240.py                                       |      120 |       17 |     86% |258-265, 273-274, 293-296, 304-305, 313-314, 322-323, 338-340 |
| src/tmc\_driver/tmc\_5160.py                                       |      131 |       60 |     54% |142-148, 156-157, 177-224, 242-247, 255-256, 275-278, 286-287, 310-326, 333-335, 341-344 |
| src/tmc\_driver/tmc\_gpio/\_\_init\_\_.py                          |       46 |       24 |     48% |30-33, 35-38, 72-73, 87-105, 112-116 |
| src/tmc\_driver/tmc\_gpio/\_tmc\_gpio\_board\_base.py              |       48 |        0 |    100% |           |
| src/tmc\_driver/tmc\_gpio/\_tmc\_gpio\_board\_circuitpython.py     |       52 |       52 |      0% |     6-124 |
| src/tmc\_driver/tmc\_gpio/\_tmc\_gpio\_board\_ftdi.py              |       66 |       66 |      0% |     7-162 |
| src/tmc\_driver/tmc\_gpio/\_tmc\_gpio\_board\_gpiozero.py          |       72 |       72 |      0% |    14-135 |
| src/tmc\_driver/tmc\_gpio/\_tmc\_gpio\_board\_micropython.py       |       49 |       49 |      0% |     6-108 |
| src/tmc\_driver/tmc\_gpio/\_tmc\_gpio\_board\_periphery.py         |       36 |       36 |      0% |     14-87 |
| src/tmc\_driver/tmc\_gpio/\_tmc\_gpio\_board\_rpi\_gpio.py         |       61 |       13 |     79% |81, 107, 121-124, 133-136, 172, 177, 182 |
| src/tmc\_driver/tmc\_logger/\_\_init\_\_.py                        |        8 |        1 |     88% |        13 |
| src/tmc\_driver/tmc\_logger/\_tmc\_logger\_base.py                 |       41 |        6 |     85% |31, 36, 41, 46, 64, 69 |
| src/tmc\_driver/tmc\_logger/\_tmc\_logger\_cpython.py              |       67 |       14 |     79% |30, 94-97, 105, 121-125, 135-137, 140 |
| src/tmc\_driver/tmc\_logger/\_tmc\_logger\_micropython.py          |       23 |       23 |      0% |      5-52 |
| **TOTAL**                                                          | **3084** | **1162** | **62%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/Chr157i4n/PyTmcStepper/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/Chr157i4n/PyTmcStepper/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Chr157i4n/PyTmcStepper/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/Chr157i4n/PyTmcStepper/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2FChr157i4n%2FPyTmcStepper%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/Chr157i4n/PyTmcStepper/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.