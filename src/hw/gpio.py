# -*- coding: UTF-8 -*-
'''
Created on 30 août 2016

@author: dassierp
'''

import logging

try:
    import RPi.GPIO as GPIO
except:
    # RPi.GPIO not installed: we are not running on a Raspberry
    # Simulate GPIO
    class GPIO():
        OUT = None
        BOARD = None
        def setmode(self, mode):
            pass

        def setup(self, pinnb, mode):
            pass

        def output(self, pinnb, value):
            pass

        def input(self, pinnb):
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
    def __init__(self, pConfig="raspberry.conf"):
        try:
        GPIO.setmode(GPIO.BOARD)
        self.__channel = {}
        with open(pConfig, "r") as fd:
            for l in fd.readline():
                if l.startswith("#"):
                    continue
                chnb, pinnb = l.split(":")
                self.__channel[int(chnb)] = int(pinnb)
                GPIO.setup(pinnb, GPIO.OUT)

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
