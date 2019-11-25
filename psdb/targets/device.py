# Copyright (c) 2018-2019 Phase Advanced Sensor Systems, Inc.
import types


class Reg(object):
    READABLE  = (1 << 0)
    WRITEABLE = (1 << 1)

    def __init__(self, name, offset, size, flags):
        self.name   = name
        self.offset = offset
        self.size   = size
        self.flags  = flags


class Reg32(Reg):
    def __init__(self, name, offset):
        super(Reg32, self).__init__(name, offset, 4,
                                    Reg.READABLE | Reg.WRITEABLE)

    def read(self, dev):
        return dev._read_32(self.offset)

    def write(self, dev, v):
        dev._write_32(v, self.offset)


class Reg32R(Reg):
    def __init__(self, name, offset):
        super(Reg32R, self).__init__(name, offset, 4, Reg.READABLE)

    def read(self, dev):
        return dev._read_32(self.offset)


class Reg32W(Reg):
    def __init__(self, name, offset):
        super(Reg32W, self).__init__(name, offset, 4, Reg.WRITEABLE)

    def write(self, dev, v):
        dev._write_32(v, self.offset)


class Device(object):
    def __init__(self, target, dev_base, name, regs):
        self.target   = target
        self.dev_base = dev_base
        self.name     = name
        self.regs     = regs
        for r in regs:
            n = r.name.lower()
            if r.flags & Reg.READABLE:
                m = types.MethodType(lambda s, o=r.offset: s._read_32(o), self)
                self.__dict__['_read_' + n] = m
            if r.flags & Reg.WRITEABLE:
                m = types.MethodType(lambda s, v, o=r.offset: s._write_32(v, o),
                                     self)
                self.__dict__['_write_' + n] = m

        assert self.name not in self.target.devs
        self.target.devs[self.name] = self

    def _read_32(self, offset):
        return self.target.ahb_ap.read_32(self.dev_base + offset)

    def _write_32(self, v, offset):
        self.target.ahb_ap.write_32(v, self.dev_base + offset)

    def _set_field(self, v, width, shift, offset):
        assert width + shift <= 32
        mask = (1 << width) - 1
        assert ((v & ~mask) == 0)
        curr = self._read_32(offset)
        curr &= ~(mask << shift)
        curr |= (v << shift)
        self._write_32(curr, offset)

    def _get_field(self, width, shift, offset):
        assert width + shift <= 32
        mask = (1 << width) - 1
        curr = self._read_32(offset) >> shift
        return curr & mask

    def dump_registers(self):
        width = max(len(r.name) for r in self.regs if r.flags & Reg.READABLE)

        for r in self.regs:
            if r.flags & Reg.READABLE:
                print('%*s = 0x%0*X' % (width, r.name, 2*r.size, r.read(self)))

    def enable_device(self):
        self.target._enable_device(self)


class MemDevice(Device):
    '''
    Base class for memory-type devices (SRAM, Flash, etc.).
    '''
    def __init__(self, target, name, addr, size):
        super(MemDevice, self).__init__(target, addr, name, [])
        self.size = size

    def read_mem_block(self, addr, size):
        return self.target.ahb_ap.read_bulk(addr, size)