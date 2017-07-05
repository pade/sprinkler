# -*- coding: UTF-8 -*-
'''
Created on 29 août 2016

@author: dassierp
'''

# Ignore PyDev pep8 analysis
# @PydevCodeAnalysisIgnore

import os
import sys
import unittest

# Set parent directory in path, to be able to import module
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import channel
from hw import gpio


class TestChannel(unittest.TestCase):

    def setUp(self):
        class StubHw(gpio.BaseGpio):

            def __init__(self, pconfig):
                pass

            def write(self, pchannel, pvalue):
                pass

            def read(self, pchannel):
                return False

        self.hw = StubHw(None)

    def tearDown(self):
        pass

    def testChannel(self):
        '''Test update of the channel status'''
        ch = channel.Channel("Ch1", 0, self.hw)
        ch.isenable = True
        ch.running = True
        self.assertTrue(ch.running is True)

        ch.running = False
        self.assertTrue(ch.running is False)

    def testInit(self):
        '''On init, stop water'''
        ch = channel.Channel("Ch1", 0, self.hw)
        self.assertTrue(ch.running is False)

    def testEnable(self):
        '''When disable channel never runs'''
        ch = channel.Channel("Citronnier", 0, self.hw)
        self.assertTrue(ch.name is "Citronnier")
        ch.isenable = False
        self.assertTrue(ch.running is False)

    def testManual(self):
        """Forced ON, OFF or return to AUTO"""
        ch = channel.Channel("Citronnier", 0, self.hw)
        self.assertTrue(ch.manual is "AUTO")
        ch.manual = "OFF"
        self.assertTrue(ch.manual is "OFF")
        ch.manual = "ON"
        self.assertTrue(ch.manual is "ON")
        ch.manual = "DUMMY"
        self.assertTrue(ch.manual is "AUTO")
