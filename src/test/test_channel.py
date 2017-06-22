# -*- coding: UTF-8 -*-
'''
Created on 29 août 2016

@author: dassierp
'''

# Ignore PyDev pep8 analysis
#@PydevCodeAnalysisIgnore

import os
import sys
import unittest
import logging

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
        '''
        Test update of the channel status
        '''
        ch = channel.Channel("Ch1",0, self.hw)
        ch.isenable = True
        ch.running = True
        self.assertTrue(ch.running is True)

        ch.running = False
        self.assertTrue(ch.running is False)

    def testInit(self):
        '''
        On init, stop water
        '''
        ch = channel.Channel("Ch1",0, self.hw)
        self.assertTrue(ch.running is False)
    
    def testEnable(self):
        '''
        When disable channel never runs
        '''
        ch = channel.Channel("Citronnier",0, self.hw)
        self.assertTrue(ch.name is "Citronnier")
        ch.isenable = False
        self.assertTrue(ch.running is False)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestChannel))
    return suite

if __name__ == "__main__":
    logger = logging.getLogger()
    #logger.level = logging.DEBUG
    #formatter = logging.Formatter('%(asctime)s - %(name)s [%(levelname)s] %(message)s')
    handler = logging.NullHandler()
    #handler.setFormatter(formatter)
    logger.addHandler(handler)

    suite = suite()
    unittest.TextTestRunner(verbosity=2).run(suite)
