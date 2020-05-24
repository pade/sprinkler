from .gpio import BaseGpio
import os
import RPi.GPIO as GPIO


class RaspberryGpio(BaseGpio):
    '''
    GPIO management for Raspberry
    '''
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        self.__channel = {}
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "raspberry.conf"), "r") as fd:
           file_content = fd.readlines()
        for l in file_content:
            if l.startswith('#'):
                continue
            if ':' not in l:
                # Ignore invalid lines
                continue
            chnb, pinnb = l.split(":")
            self.__channel[int(chnb)] = int(pinnb)
            GPIO.setup(int(pinnb), GPIO.OUT)

        super(RaspberryGpio, self).__init__()

    def write(self, pchannel, pvalue):
        for key in self.__channel:
            if int(pchannel) == key:
                GPIO.output(self.__channel[key], pvalue)
                break

    def read(self, pchannel):
        for key in self.__channel:
            if int(pchannel) == key:
                return GPIO.input(self.__channel[key])
        self._log.error(f"Channel n°{pchannel} is not found in channel list")

