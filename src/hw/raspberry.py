from .gpio import BaseGpio
import os
import RPi.GPIO as GPIO
import json


class RaspberryGpio(BaseGpio):
    '''
    GPIO management for Raspberry
    '''
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        self.__channel = {}
        self.__waterPin = {'pin': None, 'inverted': False}
        
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "raspberry.json"), "r") as fd:
            config = json.load(fd)
            for channel in config['channels']:
                self.__channel[channel['channel']] = channel['pin']
                GPIO.setup(channel['pin'], GPIO.out)
            self.__waterPin['pin'] = config['water_level']['pin']
            self.__waterPin['inverted'] = config['water_level']['inverted']
            GPIO(self.__waterPin['pin'], GPIO.IN)
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

    def isWater(self):
        pinValue = GPIO.input(self.__waterPin['pin'])
        if self.__waterPin['inverted']:
            return  not pinValue
        else:
            return pinValue
