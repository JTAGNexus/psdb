# Copyright (c) 2018-2019 Phase Advanced Sensor Systems, Inc.
from ..device import Device, Reg32


ENABLE_BITS = {
    # AHB1
    'DMA1'    : (0x048,  0),
    'DMA2'    : (0x048,  1),
    'DMAMUX'  : (0x048,  2),
    'CORDIC'  : (0x048,  3),
    'FMAC'    : (0x048,  4),
    'FLASH'   : (0x048,  8),
    'CRC'     : (0x048, 12),

    # AHB2
    'GPIOA'   : (0x04C,  0),
    'GPIOB'   : (0x04C,  1),
    'GPIOC'   : (0x04C,  2),
    'GPIOD'   : (0x04C,  3),
    'GPIOE'   : (0x04C,  4),
    'GPIOF'   : (0x04C,  5),
    'GPIOG'   : (0x04C,  6),
    'ADC12'   : (0x04C, 13),
    'ADC345'  : (0x04C, 14),
    'DAC1'    : (0x04C, 16),
    'DAC2'    : (0x04C, 17),
    'DAC3'    : (0x04C, 18),
    'DAC4'    : (0x04C, 16),
    'AES'     : (0x04C, 24),
    'RNG'     : (0x04C, 26),

    # AHB3
    'FMC'     : (0x050,  0),
    'QSPI'    : (0x050,  8),

    # APB1.1
    'TIM2'    : (0x058,  0),
    'TIM3'    : (0x058,  1),
    'TIM4'    : (0x058,  2),
    'TIM5'    : (0x058,  3),
    'TIM6'    : (0x058,  4),
    'TIM7'    : (0x058,  5),
    'CRS'     : (0x058,  8),
    'RTCAPB'  : (0x058, 10),
    'WWDG'    : (0x058, 11),
    'SPI2'    : (0x058, 14),
    'SPI3'    : (0x058, 15),
    'USART2'  : (0x058, 17),
    'USART3'  : (0x058, 18),
    'USART4'  : (0x058, 19),
    'USART5'  : (0x058, 20),
    'I2C1'    : (0x058, 21),
    'I2C2'    : (0x058, 22),
    'USB'     : (0x058, 23),
    'FDCAN'   : (0x058, 25),
    'PWR'     : (0x058, 28),
    'I2C3'    : (0x058, 30),
    'LPTIM1'  : (0x058, 31),

    # APB1.2
    'LPUART1' : (0x05C,  0),
    'I2C4'    : (0x05C,  1),
    'UCPD1'   : (0x05C,  8),

    # APB2
    'SYSCFG'  : (0x060,  0),
    'TIM1'    : (0x060, 11),
    'SPI1'    : (0x060, 12),
    'TIM8'    : (0x060, 13),
    'USART1'  : (0x060, 14),
    'SPI4'    : (0x060, 15),
    'TIM15'   : (0x060, 16),
    'TIM16'   : (0x060, 17),
    'TIM17'   : (0x060, 18),
    'TIM20'   : (0x060, 20),
    'SAI1'    : (0x060, 21),
    'HRTIM1'  : (0x060, 26),
    }


class RCC(Device):
    '''
    Driver for the STM Reset and Clock Control (RCC) device.
    '''
    REGS = [Reg32('CR',         0x000),
            Reg32('ICSCR',      0x004),
            Reg32('CFGR',       0x008),
            Reg32('PLLCFGR',    0x00C),
            Reg32('CIER',       0x018),
            Reg32('CIFR',       0x01C),
            Reg32('CICR',       0x020),
            Reg32('AHB1RSTR',   0x028),
            Reg32('AHB2RSTR',   0x02C),
            Reg32('AHB3RSTR',   0x030),
            Reg32('APB1RSTR1',  0x038),
            Reg32('APB1RSTR2',  0x03C),
            Reg32('APB2RSTR',   0x040),
            Reg32('AHB1ENR',    0x048),
            Reg32('AHB2ENR',    0x04C),
            Reg32('AHB3ENR',    0x050),
            Reg32('APB1ENR1',   0x058),
            Reg32('APB1ENR2',   0x05C),
            Reg32('APB2ENR',    0x060),
            Reg32('AHB1SMENR',  0x068),
            Reg32('AHB2SMENR',  0x06C),
            Reg32('AHB3SMENR',  0x070),
            Reg32('APB1SMENR1', 0x078),
            Reg32('APB1SMENR2', 0x07C),
            Reg32('APB2SMENR',  0x080),
            Reg32('CCIPR',      0x088),
            Reg32('BDCR',       0x090),
            Reg32('CSR',        0x094),
            Reg32('CRRCR',      0x098),
            Reg32('CCIPR2',     0x09C),
            ]

    def __init__(self, target, name, addr):
        super(RCC, self).__init__(target, addr, name, RCC.REGS)

    def enable_device(self, name):
        offset, bit = ENABLE_BITS[name]
        if self._get_field(1, bit, offset) == 0:
            self._set_field(1, 1, bit, offset)