# -*- coding: UTF-8 -*-
'''
Created on 30 août 2016

@author: dassierp
'''

import logging
import os

class DummyGPIO():
    OUT = None
    BOARD = None
    def __init__(self):
        self.__channel = {}

    def setmode(self, mode):
        pass

    def setup(self, pinnb, mode):
        self.__channel[pinnb] = False

    def output(self, pinnb, value):
        self.__channel[pinnb] = value

    def input(self, pinnb):
        try:
            return self.__channel[pinnb]
        except KeyError:
            return False

class BaseGpio(object):
    '''
    GPIO interface class
    '''

    def __init__(self, pConfig):
        '''
        Constructor
        @param pConfig: HW configuration parameter
        '''
        self.hwcfg = pConfig
        self._log = logging.getLogger()

    def write(self, pchannel, pvalue):
        raise NotImplementedError

    def read(self, pchannel):
        raise NotImplementedError


class RaspberryGpio(BaseGpio):
    '''
    GPIO management for Raspberry
    '''
    def __init__(self, pConfig=os.path.join(os.path.dirname(os.path.abspath(__file__)), "raspberry.conf")):
        try:
            import RPi.GPIO as GPIO
        except:
            # RPi.GPIO not installed: we are not running on a Raspberry
            # Simulate GPIO
            GPIO = DummyGPIO()
        GPIO.setmode(GPIO.BOARD)
        self.__channel = {}
        with open(pConfig, "r") as fd:
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

        super(RaspberryGpio, self).__init__(pConfig)

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
