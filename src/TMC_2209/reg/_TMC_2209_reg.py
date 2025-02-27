#pylint: disable=invalid-name
"""
this file contains:
1. hexadecimal address of the different registers
2. bitposition and bitmasks of the different values of each register

Example:
the register IOIN has the address 0x06 and the first bit shows
whether the ENABLE (EN/ENN) Pin is currently HIGH or LOW
"""

from ._TMC_220X_reg import *

#addresses
SGTHRS          =   0x40
SG_RESULT       =   0x41

#SGTHRS
sgthrs              = 255<<0