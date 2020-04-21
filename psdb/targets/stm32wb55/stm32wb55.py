# Copyright (c) 2020 by Terry Greeniaus.
import psdb
from .flash import FLASH
from .sram import SRAM
from .pwr import PWR
from ..device import MemDevice
from psdb.targets import Target


DEVICES = [(SRAM,   'SRAM1',    0x20000000, 0x00030000),
           (SRAM,   'SRAM2a',   0x20030000, 0x00008000),
           (SRAM,   'SRAM2b',   0x20038000, 0x00008000),
           (PWR,     'PWR',     0x58000400),
           (FLASH,  'FLASH',    0x58004000, 0x08000000, 3300000,
                                0x1FFF7000, 1024),
           ]


class STM32WB55(Target):
    def __init__(self, db):
        super(STM32WB55, self).__init__(db, 24000000)
        self.ahb_ap     = self.db.aps[0]
        self.uuid       = self.ahb_ap.read_bulk(0x1FFF7590, 12)
        self.flash_size = (self.ahb_ap.read_32(0x1FFF75E0) & 0x0000FFFF)*1024
        self.package    = self.ahb_ap.read_32(0x1FFF7500) & 0x0000001F
        self.mcu_idcode = self.ahb_ap.read_32(0xE0042000)

        for d in DEVICES:
            cls  = d[0]
            name = d[1]
            addr = d[2]
            args = d[3:]
            cls(self, self.ahb_ap, name, addr, *args)

        self.flash = self.devs['FLASH']
        MemDevice(self, self.ahb_ap, 'FBANKS', self.flash.mem_base,
                  self.flash.user_flash_size)
        MemDevice(self, self.ahb_ap, 'OTP', self.flash.otp_base,
                  self.flash.otp_len)
        self.devs['SRAM2a'].size = self.flash.user_sram2a_size
        self.devs['SRAM2b'].size = self.flash.user_sram2b_size

    def __repr__(self):
        return 'STM32WB55 MCU_IDCODE 0x%08X' % self.mcu_idcode

    @staticmethod
    def probe(db):
        # APSEL 0 and 1 should be populated and be AHB APs.
        for i in range(2):
            if i not in db.aps:
                print('%u not in db.aps' % i)
                return None

            ap = db.aps[i]
            if not isinstance(ap, psdb.access_port.AHBAP):
                print('%u not an AHBAP' % i)
                return None
        
        # Identify the STM32WB55 through the base component's CIDR/PIDR
        # registers.
        c = db.aps[0].base_component
        if not c or c.cidr != 0xB105100D or c.pidr != 0x00000000000A0495:
            print('Bad component')
            return None

        # While the STM32WB55 has two CPUs, the second one is inaccessible due
        # to ST security.
        if len(db.cpus) != 1:
            print('%u cpus' % len(db.cpus))
            return None

        return STM32WB55(db)