from .gpio import BaseGpio
import smbus
import os
import configparser


class Relay(BaseGpio):
    DEVICE_ADDR = 0x10
    DEVICE_BUS = 1

    def __init__(self):
        self.bus = smbus.SMBus(Relay.DEVICE_BUS)
        super().__init__()

    def write(self, pchannel, pvalue):
        if pvalue:
            self.bus.write_byte_data(Relay.DEVICE_ADDR, pchannel+1, 0xFF)
        else:
            self.bus.write_byte_data(Relay.DEVICE_ADDR, pchannel+1, 0x00)

    def read(self,pchannel):
        return self.bus.read_byte_data(Relay.DEVICE_ADDR, pchannel+1)

