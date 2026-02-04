# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/Chr157i4n/PyTmcStepper/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                               |    Stmts |     Miss |   Cover |   Missing |
|------------------------------------------------------------------- | -------: | -------: | ------: | --------: |
| src/tmc\_driver/\_\_init\_\_.py                                    |       17 |        0 |    100% |           |
| src/tmc\_driver/\_tmc\_exceptions.py                               |        5 |        0 |    100% |           |
| src/tmc\_driver/\_tmc\_math.py                                     |       26 |        0 |    100% |           |
| src/tmc\_driver/\_tmc\_stallguard.py                               |      123 |       23 |     81% |67, 71-78, 87, 152-162, 203, 251, 253, 283, 297, 334 |
| src/tmc\_driver/\_tmc\_stepperdriver.py                            |       72 |       10 |     86% |16-17, 147, 183, 200, 206-210 |
| src/tmc\_driver/\_tmc\_validation.py                               |        7 |        0 |    100% |           |
| src/tmc\_driver/\_tmc\_xxxx.py                                     |      175 |       52 |     70% |146-150, 161, 177, 204-205, 213, 221-222, 230, 238-239, 247, 274, 319-322, 352-353, 366-373, 379-390, 398-399, 418, 422, 426, 428, 430, 441, 449, 460, 464, 483-489 |
| src/tmc\_driver/com/\_\_init\_\_.py                                |       28 |       18 |     36% |33-34, 48-68 |
| src/tmc\_driver/com/\_tmc\_com.py                                  |       38 |        2 |     95% |    38, 88 |
| src/tmc\_driver/com/\_tmc\_com\_spi.py                             |       28 |        7 |     75% |     46-58 |
| src/tmc\_driver/com/\_tmc\_com\_spi\_base.py                       |       50 |       13 |     74% |76, 78, 80, 82, 155-164 |
| src/tmc\_driver/com/\_tmc\_com\_uart.py                            |       46 |       12 |     74% |39-59, 62, 68, 86 |
| src/tmc\_driver/com/\_tmc\_com\_uart\_base.py                      |      156 |       85 |     46% |82, 84, 94, 122, 124, 130, 142, 149, 174, 176, 192-193, 222, 231-234, 239, 256-355, 371-394 |
| src/tmc\_driver/enable\_control/\_\_init\_\_.py                    |       13 |        3 |     77% | 30-31, 44 |
| src/tmc\_driver/enable\_control/\_tmc\_ec.py                       |       20 |        1 |     95% |        38 |
| src/tmc\_driver/enable\_control/\_tmc\_ec\_pin.py                  |       26 |        0 |    100% |           |
| src/tmc\_driver/enable\_control/\_tmc\_ec\_toff.py                 |       12 |        0 |    100% |           |
| src/tmc\_driver/motion\_control/\_\_init\_\_.py                    |       43 |       10 |     77% |46-47, 54-56, 86-88, 97-101 |
| src/tmc\_driver/motion\_control/\_tmc\_mc.py                       |      135 |       13 |     90% |59, 64, 85, 90-91, 96, 111, 116, 121, 126, 156, 235, 283 |
| src/tmc\_driver/motion\_control/\_tmc\_mc\_int\_ramp\_generator.py |      117 |       31 |     74% |40-43, 48-51, 130-140, 154-166, 212 |
| src/tmc\_driver/motion\_control/\_tmc\_mc\_step\_dir.py            |      186 |       18 |     90% |40, 45-48, 53, 74, 79-88, 162, 234, 248, 343, 357 |
| src/tmc\_driver/motion\_control/\_tmc\_mc\_step\_pwm\_dir.py       |       37 |        6 |     84% |20, 41-42, 47, 52, 71 |
| src/tmc\_driver/motion\_control/\_tmc\_mc\_step\_reg.py            |       17 |        0 |    100% |           |
| src/tmc\_driver/motion\_control/\_tmc\_mc\_vactual.py              |       82 |       17 |     79% |35-36, 124, 126-130, 132-134, 136-138, 142, 146, 192, 200, 204 |
| src/tmc\_driver/platform\_utils.py                                 |       14 |        5 |     64% |16, 18, 27-30 |
| src/tmc\_driver/reg/\_\_init\_\_.py                                |        0 |        0 |    100% |           |
| src/tmc\_driver/reg/\_tmc220x\_reg.py                              |       61 |        1 |     98% |       195 |
| src/tmc\_driver/reg/\_tmc224x\_reg.py                              |       98 |       12 |     88% |69-79, 313 |
| src/tmc\_driver/reg/\_tmc2209\_reg.py                              |       14 |        0 |    100% |           |
| src/tmc\_driver/reg/\_tmc5160\_reg.py                              |      121 |        8 |     93% |69-75, 455 |
| src/tmc\_driver/reg/\_tmc\_reg.py                                  |       98 |       17 |     83% |70, 75, 80, 100, 124-131, 135-137, 179-180 |
| src/tmc\_driver/reg/\_tmc\_shared\_regs.py                         |       40 |        0 |    100% |           |
| src/tmc\_driver/tmc\_220x.py                                       |      124 |       24 |     81% |115-116, 135-136, 160-161, 175-185, 321-322, 363-366, 374-375, 383-384, 396-397 |
| src/tmc\_driver/tmc\_2208.py                                       |        3 |        0 |    100% |           |
| src/tmc\_driver/tmc\_2209.py                                       |       15 |        0 |    100% |           |
| src/tmc\_driver/tmc\_2240.py                                       |      123 |       17 |     86% |263-270, 278-279, 298-301, 309-310, 318-319, 327-328, 345-347 |
| src/tmc\_driver/tmc\_5160.py                                       |      134 |       25 |     81% |261-262, 281-284, 292-293, 316-332, 340-342, 349-352 |
| src/tmc\_driver/tmc\_gpio/\_\_init\_\_.py                          |       46 |       24 |     48% |31-34, 36-39, 73-74, 88-106, 113-117 |
| src/tmc\_driver/tmc\_gpio/\_tmc\_gpio\_board\_base.py              |       26 |        0 |    100% |           |
| src/tmc\_driver/tmc\_gpio/\_tmc\_gpio\_board\_gpiozero.py          |       72 |       12 |     83% |68-69, 73-76, 82, 84, 109, 126, 133, 140 |
| src/tmc\_driver/tmc\_gpio/\_tmc\_gpio\_board\_rpi\_gpio.py         |       58 |        7 |     88% |81, 107, 123, 135, 172, 177, 182 |
| src/tmc\_driver/tmc\_logger/\_\_init\_\_.py                        |        8 |        1 |     88% |        11 |
| src/tmc\_driver/tmc\_logger/\_tmc\_logger\_base.py                 |       28 |        5 |     82% |29, 34, 39, 44, 62 |
| src/tmc\_driver/tmc\_logger/\_tmc\_logger\_cpython.py              |       67 |       14 |     79% |28, 91-94, 98, 114-118, 128-130, 133 |
| **TOTAL**                                                          | **2609** |  **493** | **81%** |           |


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