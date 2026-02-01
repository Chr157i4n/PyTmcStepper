# CHANGELOG

<!-- version list -->

## v0.21.1 (2026-02-01)

### Bug Fixes

- Remove unused state machine cleanup code in TmcMotionControlStepPio
  ([`8e71a47`](https://github.com/Chr157i4n/PyTmcStepper/commit/8e71a47d6b9844e555c1a236207fa378354d7530))

- Update coverage omit patterns to exclude additional pio files
  ([`84c17b1`](https://github.com/Chr157i4n/PyTmcStepper/commit/84c17b16fd3aded6a33e518b66eb2475c29f51c5))

### Chores

- Moved pyserial to optional dep and changed casing of optional-dependencies
  ([`b8de0ea`](https://github.com/Chr157i4n/PyTmcStepper/commit/b8de0ea16598f100f0ae55c6a9b9e04ef4655f12))

- Moved unittest files back into tests folder
  ([`4ef6c78`](https://github.com/Chr157i4n/PyTmcStepper/commit/4ef6c786b5982c1cc71fb6450a331700ed024e47))

### Documentation

- Update installation instructions for Raspberry Pi support
  ([`5d9dbaa`](https://github.com/Chr157i4n/PyTmcStepper/commit/5d9dbaade714926c45dfa710c5fcc3d46df8e747))

### Refactoring

- Changed pio implementation to easier add Circuitpython #143
  ([`76d075b`](https://github.com/Chr157i4n/PyTmcStepper/commit/76d075b97390d57062f618e197ac469c5b029329))

### Testing

- Add wait_for_movement_finished_threaded to run_to_position_steps_threaded
  ([`28ac61a`](https://github.com/Chr157i4n/PyTmcStepper/commit/28ac61ad2273100ce311297e0a6d9decdd5af081))

- Fix test path in workflow
  ([`5adb9b1`](https://github.com/Chr157i4n/PyTmcStepper/commit/5adb9b13e1263ddabae0820300466766002de6c6))


## v0.21.0 (2026-01-28)

### Bug Fixes

- Improve soft stop handling in PIO motion control
  ([`5e05fa6`](https://github.com/Chr157i4n/PyTmcStepper/commit/5e05fa667853514ff889d3336b24c993fc9a79eb))

- Reduce maximum block size for cruise steps in PIO motion control
  ([`13849a5`](https://github.com/Chr157i4n/PyTmcStepper/commit/13849a5b3cc84298261fc02dbe506680970fef66))

- Update logging levels for movement completion in PIO motion control
  ([`55c0e20`](https://github.com/Chr157i4n/PyTmcStepper/commit/55c0e20b954511744d3d3e318f15bfb3519ac84e))

### Chores

- Exclude *_pio.py from coverage report
  ([`85fd355`](https://github.com/Chr157i4n/PyTmcStepper/commit/85fd355ab6f3d652368dd68ea82d0fbeb753090a))

### Features

- Add PIO-based motion control for TMC stepper drivers (working, but not perfect) #143
  ([`f716439`](https://github.com/Chr157i4n/PyTmcStepper/commit/f716439477f4518b0b4da213ebde782b8be5d912))

### Refactoring

- Remove unused state machine tracking and related attributes in PIO motion control
  ([`c35a920`](https://github.com/Chr157i4n/PyTmcStepper/commit/c35a9209fc668c6f1a51599730407a52404faecd))

### Testing

- Added micropython (UNIX-Port) unittest
  ([`57e561c`](https://github.com/Chr157i4n/PyTmcStepper/commit/57e561ccbb1eacc45c2442e8bde084e8d2f66146))

- Update test description for TMC modules
  ([`b9d1a94`](https://github.com/Chr157i4n/PyTmcStepper/commit/b9d1a945dd392f32046b39c3bb470c42a84977a4))


## v0.20.0 (2026-01-25)

### Chores

- Remove outdated CHANGELOG.BAK.md file
  ([`7cadaba`](https://github.com/Chr157i4n/PyTmcStepper/commit/7cadaba4680d86f9c6e660d2f1e61c17c794fbe7))

- Update markdownlint configuration for improved formatting
  ([`ec410c6`](https://github.com/Chr157i4n/PyTmcStepper/commit/ec410c64664967362fc042f3886e4c5660f3aede))

### Features

- Test changelog updating
  ([`dfab353`](https://github.com/Chr157i4n/PyTmcStepper/commit/dfab3532b8bb1eac92d91a23ee536607fd427529))


## v0.19.0 (2026-01-25)

### Bug Fixes

- Correct speed_fullstep calculations in TmcMotionControl class
  ([`a0a4d04`](https://github.com/Chr157i4n/PyTmcStepper/commit/a0a4d04b96b0295ab71fb69692818209b5188ecb))

- Pylint
  ([`c4497a1`](https://github.com/Chr157i4n/PyTmcStepper/commit/c4497a1744df197dbfce2d8ccea763694116b3ab))

- Update import statement to use TmcComSpiMicroPython instead of TmcComUartMicroPython
  ([`c0c330d`](https://github.com/Chr157i4n/PyTmcStepper/commit/c0c330dc862786cdb93f78ab0cd9722a84eb08a6))

- Use direct import instead of __init__.py on micropython and circuitpython (__init__.py imports
  everything which needs to much ram)
  ([`19d7109`](https://github.com/Chr157i4n/PyTmcStepper/commit/19d7109974e09c0d9f05c3ec098b590639534850))

### Chores

- Renamed changelog, so python semantic release can create a new one (with the correct format)
  ([`b2d20cf`](https://github.com/Chr157i4n/PyTmcStepper/commit/b2d20cf8bf33d3bbf82bf26dff4451c628e31e2e))

- Set minimum coverage thresholds for code coverage comments
  ([`be3e152`](https://github.com/Chr157i4n/PyTmcStepper/commit/be3e152e408aee86de3a88bd38f05ce5bc0b5cf1))

### Features

- Moved run_to_position_revolutions method to TmcMotionControl class
  ([`420546b`](https://github.com/Chr157i4n/PyTmcStepper/commit/420546b9daf666908d67fad4c836ba76698f982e))

- Only validate submodule on CPython (not on Micropython/Circuitpython to save memory)
  ([`fe4a0ce`](https://github.com/Chr157i4n/PyTmcStepper/commit/fe4a0ce0d9a889c741ccfe5d7579c34a0a0501f0))

### Refactoring

- Remove unused speed_fullstep property from TmcMotionControlStepDir class
  ([`916d18f`](https://github.com/Chr157i4n/PyTmcStepper/commit/916d18fec88c18585df90feb4d3b8e837752436f))


## v0.18.4 (2026-01-22)

### Bug Fixes

- Correct GPIO pin reference in event detection methods in GpiozeroWrapper
  ([`1827ffe`](https://github.com/Chr157i4n/PyTmcStepper/commit/1827ffe208468a108b45c91a585fe37aa44eac1b))

### Chores

- Add coverage report omission for specific test files
  ([`e0aa951`](https://github.com/Chr157i4n/PyTmcStepper/commit/e0aa951a03078ac5827bc5fe7a579aeaf633ee7e))

- Remove version declaration from __init__.py
  ([`42e6ba7`](https://github.com/Chr157i4n/PyTmcStepper/commit/42e6ba79bb11576808f025ec4c0ee22a398ea3f9))

- Update coverage report configuration to exclude additional lines
  ([`2a073e2`](https://github.com/Chr157i4n/PyTmcStepper/commit/2a073e2ea6b4daed0c4b3652dd24b69ba9fe8a8c))

- Update coverage report to exclude additional test files and add new test for Tmc2209 with gpiozero
  ([`c429e30`](https://github.com/Chr157i4n/PyTmcStepper/commit/c429e304d20030e5eabb592e47589c78fae214f7))


## v0.18.3 (2026-01-21)

### Bug Fixes

- Remove redundant assignment in pin check logic
  ([`7293032`](https://github.com/Chr157i4n/PyTmcStepper/commit/7293032e60fe1b464b78791469220e6b2683c0b4))

- Remove unused lazy import for TmcEnableControl
  ([`b40bc08`](https://github.com/Chr157i4n/PyTmcStepper/commit/b40bc0853427eddda47fff4732bacaffa3c38c1c))

- Rename workflow from 'Test' to 'CI Pipeline'
  ([`4954905`](https://github.com/Chr157i4n/PyTmcStepper/commit/4954905402c0f0b1740f051ace66df0b7c96c47e))

- Update CI badge in README.md
  ([`368c292`](https://github.com/Chr157i4n/PyTmcStepper/commit/368c292977a9561ac6953d10470f787b32a928c8))

- Update coverage badge link in README.md
  ([`f3cd647`](https://github.com/Chr157i4n/PyTmcStepper/commit/f3cd6476b800e55e5bfa8bd7c17f759734978373))

### Continuous Integration

- Update Python version to 3.13 in CI workflow
  ([`b8300f1`](https://github.com/Chr157i4n/PyTmcStepper/commit/b8300f1a4dad52af3a7a96647031a93cad4b2c44))

### Testing

- Add unit test for TMC pin functionality and fake I/O class
  ([`8ae956c`](https://github.com/Chr157i4n/PyTmcStepper/commit/8ae956cf586b5b7cf48a6d5b346775c32f83e21d))

- Add unit test for TMC5160 set current RMS functionality
  ([`bbd3827`](https://github.com/Chr157i4n/PyTmcStepper/commit/bbd382714dca26e81d6cc8f85403a0f323aceb56))

- Add unit tests for different import methods
  ([`8f6126b`](https://github.com/Chr157i4n/PyTmcStepper/commit/8f6126bcaaabb5f8e8e991af639e763bf915450d))

- Add unit tests for TMC move (intramp)
  ([`d1ea07e`](https://github.com/Chr157i4n/PyTmcStepper/commit/d1ea07e3cb413a20cf21f8048e6e8d20726f72b4))

- Add unit tests for TMC move functionality in test_tmc_move_vactual.py
  ([`e616d02`](https://github.com/Chr157i4n/PyTmcStepper/commit/e616d02888254f0cbfefeeba431a6c08f1dc3731))

- Add unit tests for TMC move with step PWM direction and step register
  ([`9070ae0`](https://github.com/Chr157i4n/PyTmcStepper/commit/9070ae0f964fc846eddee7c4e46373899264690c))

- Update import statements in TMC test files
  ([`895f928`](https://github.com/Chr157i4n/PyTmcStepper/commit/895f928e415d0c9993a6f1e78fa7a53849f2ff89))


## v0.18.2 (2026-01-20)

### Bug Fixes

- Rename workflow file
  ([`df1b1de`](https://github.com/Chr157i4n/PyTmcStepper/commit/df1b1de8a4466ab230310dbf42f7ba6b6dae36fb))


## v0.18.1 (2026-01-20)

### Bug Fixes

- Readd token to pypi publish
  ([`3456775`](https://github.com/Chr157i4n/PyTmcStepper/commit/34567756bb668caed09b73bd27fb8353a95b7109))


## v0.18.0 (2026-01-20)

### Bug Fixes

- Add missing job names for grype-scan and release jobs in CI workflow
  ([`a05c286`](https://github.com/Chr157i4n/PyTmcStepper/commit/a05c286c2ebb231b4ff60c20a9ea352520b64e7c))

- Add Python setup and dependency installation steps for semantic release
  ([`821cc90`](https://github.com/Chr157i4n/PyTmcStepper/commit/821cc90c97b20f1677995245ede3f8037ff2f86d))

- Update build command in pyproject.toml and remove redundant steps in CI workflow
  ([`ccb5b2c`](https://github.com/Chr157i4n/PyTmcStepper/commit/ccb5b2ced98d7cfc25b9db2267678cf712e83144))

### Features

- Add fetch-depth option to checkout step in release job
  ([`db1f46e`](https://github.com/Chr157i4n/PyTmcStepper/commit/db1f46ee1b0303b35f7b4180104143e5e1172f9d))

- Implement semantic release and package publishing steps in CI workflow
  ([`c279abc`](https://github.com/Chr157i4n/PyTmcStepper/commit/c279abc6348f9cce720f20cb05e691fb7d422076))


## v0.17.0 (2026-01-20)

### Bug Fixes

- Split unittest and code coverage step
  ([`4e64ab9`](https://github.com/Chr157i4n/PyTmcStepper/commit/4e64ab985dced6530330de2a7e4b4a988cebd478))

- Update import statements for TMC2209 usage in README
  ([`7e75e6f`](https://github.com/Chr157i4n/PyTmcStepper/commit/7e75e6f72453b245539fb122412049b553b5ddc6))

- Update Python version matrix in unittest job (toml support needed for coverage)
  ([`9a15f1d`](https://github.com/Chr157i4n/PyTmcStepper/commit/9a15f1dd1e02bd85d871a5f54834ff8521201753))

### Documentation

- Update README to include test and code coverage badges Unittest and coverage badge
  ([`f30bd13`](https://github.com/Chr157i4n/PyTmcStepper/commit/f30bd1344e9450bab768f5ceec320907edb603fc))

### Features

- Add artifact upload step for coverage comment in unittest job
  ([`2cb9d6b`](https://github.com/Chr157i4n/PyTmcStepper/commit/2cb9d6b3ea43dc89550e3ac5b8df811977d50ff5))

- Add coverage configuration to pyproject.toml
  ([`ad90b4f`](https://github.com/Chr157i4n/PyTmcStepper/commit/ad90b4fadaaccab06ad44f3c87801a5641f40a3c))

- Add example for special register access with TMC2209 in README
  ([`cf1006f`](https://github.com/Chr157i4n/PyTmcStepper/commit/cf1006f6bba4d16784ba72e6019de63b8d78ffe5))

- Update unittest job to enable coverage reporting and adjust permissions
  ([`bf56353`](https://github.com/Chr157i4n/PyTmcStepper/commit/bf56353468bd2b2bd32b8307c0b25557dd874072))


## v0.16.0 (2026-01-18)

### Bug Fixes

- Add dummy _thread implementation for environments without threading support (CircuitPython) #141
  ([`dac75ad`](https://github.com/Chr157i4n/PyTmcStepper/commit/dac75adbc74c83bc11e9888439e081905c22ae82))

- Add missing classifiers for Python implementations in pyproject.toml
  ([`7e063b3`](https://github.com/Chr157i4n/PyTmcStepper/commit/7e063b3b88a7783ca5f0bbf6bfaa91fe94ece489))

- Add safety check before disabling motor in deinit method
  ([`f94a478`](https://github.com/Chr157i4n/PyTmcStepper/commit/f94a478c3aa9b71196f31927677a8f9e1ce4b928))

- Changed msres_ms setter to use a lookup table, because math.log2 is not available on CircuitPython
  #141
  ([`1646aad`](https://github.com/Chr157i4n/PyTmcStepper/commit/1646aad20253b9f17933d8e267facf02454e3ff3))

- Implement lazy import for FtdiWrapper to optimize module loading
  ([`760b224`](https://github.com/Chr157i4n/PyTmcStepper/commit/760b224db72b35511993a2a6647dbca793094535))

- Pylint
  ([`f154f97`](https://github.com/Chr157i4n/PyTmcStepper/commit/f154f97c5352e4938c2c2ca2ba6996323d2e78c8))

- Reorder reset check for consistency
  ([`95bac7d`](https://github.com/Chr157i4n/PyTmcStepper/commit/95bac7d0449d4b91beb5fcc73c7c8c5fe473c170))

- Simplify gpio_add_event_detect docstring and raise NotImplementedError for CircuitPython
  ([`6a099f5`](https://github.com/Chr157i4n/PyTmcStepper/commit/6a099f510a847434eaa22339e9cb4b07639df592))

### Features

- Add UART and SPI communication classes for CircuitPython #141
  ([`5daa241`](https://github.com/Chr157i4n/PyTmcStepper/commit/5daa24190cfa6d5d395255dc255c0895992a57e3))

- Enhance get_time_us function to support CircuitPython #141
  ([`6addc04`](https://github.com/Chr157i4n/PyTmcStepper/commit/6addc0450204fce20ae7a0a798922e6022004aa0))

### Testing

- Add assertions for motor position after movement in TestTMCModules
  ([`c04864e`](https://github.com/Chr157i4n/PyTmcStepper/commit/c04864ec349e86abe245e2d02d9133a95a524e5b))

- Enhance TMC2209 and TMC2240 tests with additional assertions for register checks
  ([`15b30a8`](https://github.com/Chr157i4n/PyTmcStepper/commit/15b30a81dfc26bfb3413b5570b08140645ffd370))

- Put Spi test in try-except block to prevent errors, if spidev is not available
  ([`4bcf206`](https://github.com/Chr157i4n/PyTmcStepper/commit/4bcf2061da9e08988654ac91060fabcc579d57cb))


## v0.15.0 (2026-01-17)

### Bug Fixes

- Change acceleration_fullstep calculation to use integer division
  ([`e3d3fda`](https://github.com/Chr157i4n/PyTmcStepper/commit/e3d3fdabb0632174115c5935c1ed79f86b781f5a))

- Change mres_ms type from bool to int in ChopConf class
  ([`834f07c`](https://github.com/Chr157i4n/PyTmcStepper/commit/834f07ce4971b34ff62b0ad9ae661915b5007842))

- TmcStepperDriver init docstring
  ([`dde9be1`](https://github.com/Chr157i4n/PyTmcStepper/commit/dde9be18c6d99fd9789bb1b6c7186480fa404fe6))

- Update max_speed_fullstep calculation to use integer division
  ([`37e6c9d`](https://github.com/Chr157i4n/PyTmcStepper/commit/37e6c9d5fb8ebcaa307d774ed007181dfe07a15f))

### Chores

- Update action versions in python-publish workflow
  ([`14a31fa`](https://github.com/Chr157i4n/PyTmcStepper/commit/14a31fad64554f2ad29defb7bc2de086e252ba32))

### Features

- Add current_pos_fullstep property for fullstep position handling
  ([`5c51150`](https://github.com/Chr157i4n/PyTmcStepper/commit/5c5115066d0d3bd79d0ee5c6b21357e2f7305cb3))

- Add dynamic attribute forwarding for TmcStepperDriver
  ([`5e8e873`](https://github.com/Chr157i4n/PyTmcStepper/commit/5e8e873e6748f0d2689dbadfcb16a118067c05af))

### Refactoring

- Consolidate microstepping resolution logic in TmcXXXX class
  ([`8a1d619`](https://github.com/Chr157i4n/PyTmcStepper/commit/8a1d6190ba07b5f571bcfcc83bc8e1e6359cf8b9))

### Testing

- Add assertions for microstepping resolution and motor speed in TestTMCModules
  ([`75aa164`](https://github.com/Chr157i4n/PyTmcStepper/commit/75aa164ff30a570f1faa05a870a43d5759f3d310))


## v0.14.0 (2026-01-17)

### Bug Fixes

- Add missing import for Gpio in TmcXXXX driver module
  ([`f598955`](https://github.com/Chr157i4n/PyTmcStepper/commit/f598955691eb44867303bc677c8eb2229e6af3db))

- Add missing import for MovementPhase in demo script
  ([`cd07408`](https://github.com/Chr157i4n/PyTmcStepper/commit/cd0740805e2426d5539666077c5d4fdc16edde2f))

- Pass ioin argument to test_com method in TmcXXXX class
  ([`1456cd6`](https://github.com/Chr157i4n/PyTmcStepper/commit/1456cd6ed243e1b4695df904f61cdedfa2df5d6b))

- Pylint
  ([`a1a16aa`](https://github.com/Chr157i4n/PyTmcStepper/commit/a1a16aa090b06d9a68e79de1d1b9417e77df319c))

- Pylint
  ([`d6c6620`](https://github.com/Chr157i4n/PyTmcStepper/commit/d6c662065f19e7e25e56bd1ca5606e57b2dd61a9))

- Pylint
  ([`f52ca2a`](https://github.com/Chr157i4n/PyTmcStepper/commit/f52ca2a3bd26c6d7ee2b01f67b9d35e262c53db4))

### Refactoring

- Added __init__.py in tmc_drvier module
  ([`4d38270`](https://github.com/Chr157i4n/PyTmcStepper/commit/4d382700b8bf50c5e6d6d78071294b20777b9bef))

- Clean up unused imports and reorganize exception imports in driver files
  ([`90657bf`](https://github.com/Chr157i4n/PyTmcStepper/commit/90657bf907029e8082b0c1ac3b6f4044091e71fa))

- Remove empty demo module files for tmc2240 and main demo
  ([`19e4186`](https://github.com/Chr157i4n/PyTmcStepper/commit/19e4186755ace28d416ebf3d143902addd84c4b1))

- Remove unused imports
  ([`9c121ef`](https://github.com/Chr157i4n/PyTmcStepper/commit/9c121efff629e573e382908f7acd188c4b7f8c69))

- Remove unused tmc_com property and imports from motion control modules
  ([`c5c5e8e`](https://github.com/Chr157i4n/PyTmcStepper/commit/c5c5e8e3150d7734cc41f1215e1d8010d0e9bf94))

- Update demo script descriptions for clarity
  ([`a4eabd4`](https://github.com/Chr157i4n/PyTmcStepper/commit/a4eabd4ea73ed57ff9cb36281b0095e304b3fe26))

- Update import statements and remove wildcard imports
  ([`78a5484`](https://github.com/Chr157i4n/PyTmcStepper/commit/78a548418aff98d38c5481340f9240b9f40629fb))


## v0.13.0 (2026-01-11)

### Bug Fixes

- Changed get_bit_width method to calculate bit width manually (micropython compatibility)
  ([`c2689b7`](https://github.com/Chr157i4n/PyTmcStepper/commit/c2689b7800d50fce56a424d9ab2e5e84e06ef168))

- Cleaned up demo scripts
  ([`93f88d5`](https://github.com/Chr157i4n/PyTmcStepper/commit/93f88d566065fca0bf64b7d28aea46d51373aa8f))

- Correct duration calculation from milliseconds to microseconds in set_vactual_dur method
  ([`185d96f`](https://github.com/Chr157i4n/PyTmcStepper/commit/185d96fe53c555d067fa50c350e663cef40982c7))

- Moved gpiozero pwm switching into _tmc_gpio_board_gpiozero.py
  ([`c580131`](https://github.com/Chr157i4n/PyTmcStepper/commit/c5801313f3742c382231fee96fbef8082687ea2a))

- Pylint
  ([`d2254a3`](https://github.com/Chr157i4n/PyTmcStepper/commit/d2254a306a965496451c2a935ca14e50738da6a9))

- Remove unnecessary cs_count parameter from SPI configuration
  ([`22277eb`](https://github.com/Chr157i4n/PyTmcStepper/commit/22277eb64e15c953fd6b28abed81e49b83f8d164))

- Remove unnecessary loglevel and movement settings from demo script
  ([`f28f71a`](https://github.com/Chr157i4n/PyTmcStepper/commit/f28f71ad1a858ce1c7c44a0af3db5a16965d0f9c))

- Streamline movement handling in motion control classes
  ([`ef02b52`](https://github.com/Chr157i4n/PyTmcStepper/commit/ef02b52aa7535872dc4627bd0aecca7fc2e72795))

- Update motion control to use TmcMotionControlVActual in demo script
  ([`09b6fa9`](https://github.com/Chr157i4n/PyTmcStepper/commit/09b6fa954602231772ca4d4d1e03b35d2d2d202c))

- Update SGT threshold to be signed
  ([`a3e7224`](https://github.com/Chr157i4n/PyTmcStepper/commit/a3e72241c7093fe9811b5bb31633ee3b9c43ddca))

- Update VActual register to support signed values for vactual
  ([`3462873`](https://github.com/Chr157i4n/PyTmcStepper/commit/3462873169da0f7b7569fc00b85d3e7dd44bd647))

### Features

- Add clear_rampstat method to reset ramp status after stall
  ([`997b16c`](https://github.com/Chr157i4n/PyTmcStepper/commit/997b16ceedcda1d4c4bcc22e6c0518e27d71f6cc))

- Add demo script for TMC5160 internal ramp generator homing
  ([`ddd1b61`](https://github.com/Chr157i4n/PyTmcStepper/commit/ddd1b6169f81255bd54712e04f76f1a5c2d8dff1))

- Add PWM class protocol to GPIOModuleProtocol
  ([`138a9bb`](https://github.com/Chr157i4n/PyTmcStepper/commit/138a9bbba935ab655c94d556e21ec38d8ac6bcb6))

- Add reset_positions method to reset position counters
  ([`aa14d29`](https://github.com/Chr157i4n/PyTmcStepper/commit/aa14d29c1b4ee6b23bb6a5dd0f68a5b99300ec14))

- Add stallguard and limit switch event handling in ramp generator
  ([`0b43224`](https://github.com/Chr157i4n/PyTmcStepper/commit/0b43224a21ff2dacb8141591e4bc4d8e30d2435d))

- Added method to set hybrid threshold speed in TmcXXXX class for hybrid switching between
  Stealthchop and Spreadcycle
  ([`81e6f11`](https://github.com/Chr157i4n/PyTmcStepper/commit/81e6f11a2ba6a1448bf06cde1d1605acb75e7df6))

- Implement target position property and update current position handling
  ([`e7dc520`](https://github.com/Chr157i4n/PyTmcStepper/commit/e7dc520d25c724844224499ad87f28b309c8d6d7))

- Unify position reset method naming and functionality across drivers
  ([`ccd9999`](https://github.com/Chr157i4n/PyTmcStepper/commit/ccd9999209365734755fe8b40a1bac2605714e62))

### Refactoring

- Consolidate stallguard setup logic in TMC drivers
  ([`9498d36`](https://github.com/Chr157i4n/PyTmcStepper/commit/9498d36bb677a7c56e47de2d3c24b7dec7630b75))

- Streamline GPIO handling and error checking across wrappers
  ([`b20faab`](https://github.com/Chr157i4n/PyTmcStepper/commit/b20faab01cdcec96f989cb869180636b617f41fa))


## v0.12.0 (2026-01-06)

### Documentation

- Update installation instructions in README.md for editable install
  ([`5686580`](https://github.com/Chr157i4n/PyTmcStepper/commit/5686580bde862c75a92976a0388d64f7a448aadd))

### Refactoring

- Add setter for speed_fullstep in TmcMotionControl class
  ([`418028f`](https://github.com/Chr157i4n/PyTmcStepper/commit/418028f88bf1e07f5f11b44dc0014f33d111b68d))

- Centralize initialization logic in TmcXXXX class
  ([`a806283`](https://github.com/Chr157i4n/PyTmcStepper/commit/a806283db9f3489c40ae5add2879284cedb88a91))

- Enhance TmcStepperDriver properties with type hints and error handling
  ([`e0d585d`](https://github.com/Chr157i4n/PyTmcStepper/commit/e0d585dcf68affd6de6792883d4c3c9421e8265f))

- Implement clear_gstat_verify method for GSTAT register management #118
  ([`326ba4b`](https://github.com/Chr157i4n/PyTmcStepper/commit/326ba4bdc6bcf8f8dbe055b58bb6202d684dfd89))


## v0.11.0 (2026-01-01)

### Bug Fixes

- TMC2240: fixed THigh reg addr

### Features

- added support for TMC5160
- changed set_current to set_current_rms and set_current_peak
- added typehints
- refactor logger (split micropython and cpython implementation into their own files)
- added clear function for regs
- added str function for regs
- added demo script for homing
- replaced individual register read function with unified read_register method
- TMC5160: added reg defs
- TMC5160: added MotionControl for internal Ramp Generator

### Refactoring

- Remove sys dependency and centralize time function for MicroPython compatibility
  ([`2be9b80`](https://github.com/Chr157i4n/PyTmcStepper/commit/2be9b8056fcfaac980ef31d5ee40acc71457e489))

- Replace individual register read functions with a unified read_register method
  ([`1e8e41a`](https://github.com/Chr157i4n/PyTmcStepper/commit/1e8e41a8ff849ce15f1979da3fca2bcaa8a26656))


## v0.10.0 (2025-12-30)

### Bug Fixes

- fixed pwm cleanup
- fixed reg definition (seimin in Coolconf of TMC2209)

### Features

- added unittests for submodule combinations
- renamed drv_enn to enn in reg def for consistency
- added class TmcXXXX for code shared between all TMC drivers
- changed reg definitions (Tuple of TmcRegFields instead of Array of Arrays)
- moved do_homing() to_tmc_stallguard.py
- do_homing -> added args cb_success and cb_failure
- do_homing now uses tmc_mc instead of static internal motion controller
- removed do_homing2()
- removed driver_address from constructor of COM submodules
- removed _deinit_finished

## v0.9.3 (2025-12-27)

### Bug Fixes

- fixed reg access in submodules (with callback)

## v0.9.2 (2025-12-27)

### Bug Fixes

- fixed wrong reg access (TMC2209 iholddelay and en_spreadcycle)

### Features

- added validation of submodules
- enhanced TMC2240 set_current function (added rref as argument)

### Refactoring

- Changed TmcCom classes, so i does not know the exakt reg defintions and added more Exceptions
  ([`12fdd47`](https://github.com/Chr157i4n/PyTmcStepper/commit/12fdd470178497d1da60a1e9f63b45ada8653d83))
- formatting and linting
- added typehints for register definitions


## v0.9.1 (2025-12-22)

### Refactoring

- refactored tmc_gpio modules
- refactored tmc_com modules
- dropped support for python 3.9 and older
- added more typehints
- added MicroPico project files for better Micropython support
- moved all project metadata into pyproject.toml

## v0.9.0 (2025-12-20)

### Features

- added support for MicroPython
- added support for relative movements in TmcMotionControlVActual
- added TmcMotionControlException in TmcMotionControlVActual if the VActual reg is not available (TMC2240)
- removed statistics dependency
- added property current_pos_fullstep

## v0.8.0 (2025-12-13)

### Features

- added support for FT232H (can be used on Windows; currently only with TMC2240 and SPI)
- added missing deinit in TmcEnableControl

## v0.7.8 (2025-11-23)

### Bug Fixes

- fixed RPi4 using wrong gpio lib
- changed init/deinit of classes

## v0.7.7 (2025-11-09)

### Bug Fixes

- fixed wrong reg adress of IOIN for TMC220X

## v0.7.6 (2025-05-17)

### Bug Fixes

- fixed driver addr in demo/demo_script_06_multiple_drivers.py
- fixed doubled log output when using multiple drivers
- fixed VActual bit mask

### Features

- added PwmConf reg
- added initial value to gpio_setup when using gpiozero (RPi5)

## v0.7.5 (2025-05-01)

### Bug Fixes

- fixed gstat Exception on TMC2240

### Refactoring

- removed spidev dependency from TMC220X
- added TPwmThrs reg

## v0.7.4 (2025-04-12)

### Features

- added custom exceptions
- added TmcMotionControlStepPwmDir
- fixed homing

## v0.7.3 (2025-03-15)

### Features

- increased SPI speed (from 5khz to 8mhz)
- added SPI speed to TmcComSpi constructor
- return status flags as dict received with every SPI read access

## v0.7.2 (2025-03-14)

### Features

- moved StallGuard code into own mixin class
- renamed sgresult and sgthrs reg values in order to have them consistend between drivers

### Bug Fixes

- fixed StallGuard on TMC2240 (diag0_pushpull and diag0_stall needed to be activated)

## v0.7.1 (2025-03-10)

### Features

- added Support for TMC2240
- changed registers to be initialized as Lists (Bitmasks and Bitpositions)
- added Support for SPI
- Split code for EnableControl and MotionControl into their own classes
- added Classes for EnableControl TmcEnableControlPin
- added Classes for EnableControl TmcEnableControlToff
- added Classes for MotionControl TmcMotionControlStepDir
- added Classes for MotionControl TmcMotionControlStepReg
- added Classes for MotionControl TmcMotionControlVActual
- added support for coolstep
- changed library name to PyTmcStepper
- refactored deserialisation and serialisation of register values to use classes
- changed file names according to PEP8
- changed class names according to PEP8

## v0.5.7 (2025-02-05)

### Bug Fixes

- fixed print output in test_uart()
- use mapping table for mapping gpio library to the board
- make fullsteps_per_rev configurable in constructor

### Refactoring

- refactored GPIO access to use inherited classes

## v0.5.6 (2024-12-19)

### Bug Fixes

- Return status instead of hardcoded True in test_uart
  ([`5e57e2c`](https://github.com/Chr157i4n/PyTmcStepper/commit/5e57e2c0fb265511c30c4863f9cef3877ce88553))
- fixed links in readme
- switched to python 3.13 in unittests

### Refactoring

- refactored test_dir_step_en function

## v0.5.5 (2024-10-06)

### Features

- changed Nvidia Jetson detection

## v0.5.4 (2024-08-31)

### Features

- added Orange Pi Support

## v0.5.3 (2024-08-25)

### Features

- added math function constrain
- added function set_speed
- added function set_speed_fullstep
- added demo_script_11_continous_movement
- reworked github actions pipeline (one multi-staged-pipeline)

## v0.5.2 (2024-08-01)

### Features

- added extra error handling for when the UART serial is not set

## v0.5.1 (2024-07-23)

### Features

- added toff setting
- added support for controlling direction during movement over UART
- added demo script for motor movement using only the STEP pin
- decoupled gpio access from gpio library
- added support for Raspberry Pi5 (gpiozero)
- added support for Luckfox Pico (python-periphery)

## v0.4.5 (2024-04-17)

### Features

- enhancement of logging module

### Bug Fixes

- small bugfix

## v0.4.4 (2024-04-13)

### Features

- change logger to use logging module

## v0.4.3 (2024-02-09)

### Bug Fixes

- small bugfix

## v0.4.2 (2024-01-15)

### Features

- added support for Nvidia Jetson
- added seperate file for GPIO board imports
- changed min python version to 3.7

## v0.4.1 (2023-11-26)

### Features

- removed dependency enum34
- removed dependency bitstring
- changed min python version to 3.6
- changed docstring format to google
- split code into different files
- added logger class
- moved demo scripts into demo folder
- added unittest
- switched all string to f-strings

## v0.3.4 (2023-11-13)

### Features

- fixed do_homing()
- added minspeed to do_homing()
- added TMC_2209_math.py

## v0.3.3 (2023-11-11)

### Features

- added correct StallGuard min_speed calculation

## v0.3.2 (2023-11-07)

### Features

- add pylint github action
- fixed code to pass pylint check

## v0.3.1

### Features

- Added threaded movement
- Added test_script_07_threads.py
- Added softstop
- Added get_movement_phase()

## v0.3.0

### Refactoring

- Change code to snake_case

## v0.2.2

### Features

- Added set_deinitialize_true
- Fixed ifcnt wrap around from 255 to 0

## v0.2.1

### Features

- Added setPDNdisable
- Added setMaxSpeed_fullstep and setAcceleration_fullstep

## v0.2.0

### Features

- Pin parameter order in constructor changed to EN, STEP, DIR
- STEP and DIR pins are optional parameters
- CRC check for read access reply datagrams
- If only zeroes are received an error will be thrown
- Added ignore_delay to StallGuard callback
- Implemented write access retry
- Implemented velocity ramping with VActual
- Add ability to print StallGuard results and TStep in VActual
- If write or read access fails, GSTAT will be checked for driver errors
- Added CHANGELOG.md

## v0.1.7

### Features

- Updated README
- Added number of revolutions as parameter for doHoming
- Added output whether doHoming was successful or not

## v0.1.6

### Features

- Added ability to invert direction in setVActual_rps with negative revolutions
