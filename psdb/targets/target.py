# Copyright (c) 2018-2019 Phase Advanced Sensor Systems, Inc.
import collections


class MemRegion(object):
    def __init__(self, addrs, length):
        self.addrs = addrs
        self.len   = length


class Target(object):
    def __init__(self, db, max_tck_freq):
        self.db           = db
        self.max_tck_freq = max_tck_freq
        self.cpus         = self.db.cpus
        self.devs         = collections.OrderedDict()

    def set_max_tck_freq(self):
        '''
        Sets the debug probe to the target's maximum supported SWD frequency.
        Note that this frequency may need to be throttled under some conditions
        such as during flash writes.
        '''
        return self.db.set_tck_freq(self.max_tck_freq)

    def is_halted(self, cpus=None):
        cpus = cpus or self.cpus
        for c in cpus:
            if not c.is_halted():
                return False
        return True

    def halt(self, cpus=None):
        cpus = cpus or self.cpus
        for c in cpus:
            c.halt()

    def reset_halt(self, cpus=None):
        cpus = cpus or self.cpus
        for c in cpus:
            c.reset_halt()

    def resume(self, cpus=None):
        cpus = cpus or self.cpus
        for c in cpus:
            c.resume()