# Copyright (c) 2018-2019 Phase Advanced Sensor Systems, Inc.
from .target import (Target, MemRegion)
from .device import Reg, MemDevice
from . import msp432
from . import stm32h7
from . import stm32g4


__all__ = ['Target',
           'MemRegion',
           'Reg',
           'MemDevice',
           ]

TARGETS = [msp432.MSP432P401,
           stm32h7.STM32H7,
           stm32g4.STM32G4,
           ]


def probe(db):
    for t in TARGETS:
        device = t.probe(db)
        if device:
            return device
    return None