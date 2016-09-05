# -*- coding: UTF-8 -*-
'''
Created on 2 sept. 2016

@author: dassier
'''

# Ignore PyDev pep8 analysis
#@PydevCodeAnalysisIgnore

import os
import sys
import unittest
import datetime

# Set parent directory in path, to be able to import module
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import config
import stime


class TestChannelConfig(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_setcfg(self):
        '''
        Test setCfg and getCfg
        '''
        ch = config.ChannelConfig(0)
        t = stime.STime(2, 10, 120)
        ch.setCfg('Mon', t)
        ret = ch.getCfg('Mon')
        self.assertTrue(ret[0].hour == 2 and
                        ret[0].minute == 10 and
                        ret[0].duration == 120)

        t2 = stime.STime(5, 20, 240)
        t3 = stime.STime(1, 2, 3)

        ch.setCfg('Mon', t2)
        ch.setCfg('Tue', t3)
        ret = ch.getCfg('Mon')
        self.assertTrue(ret[0].hour == 2 and
                        ret[0].minute == 10 and
                        ret[0].duration == 120)
        self.assertTrue(ret[1].hour == 5 and
                        ret[1].minute == 20 and
                        ret[1].duration == 240)

        ret = ch.getCfg('Tue')
        self.assertTrue(ret[0].hour == 1 and
                        ret[0].minute == 2 and
                        ret[0].duration == 3)

    def test_findcfg(self):
        '''
        Test find a configuration
        '''
        t1 = stime.STime(1, 0, 120)
        ch = config.ChannelConfig(0)
        ch.setCfg('Mon', t1)
        ch.setCfg('Fri', t1)

        # Following date is a monday
        d = datetime.datetime(year=2016, month=9, day=5, hour=1, minute=30)
        l = ch.findCfg('Mon', d)
        self.assertIsNotNone(l)

        d = datetime.datetime(year=2016, month=9, day=5, hour=0, minute=30)
        l = ch.findCfg('Mon', d)
        self.assertIsNone(l)

        d = datetime.datetime(year=2016, month=9, day=5, hour=3, minute=0)
        l = ch.findCfg('Mon', d)
        self.assertIsNone(l)

        # next day
        d = datetime.datetime(year=2016, month=9, day=6, hour=1, minute=30)
        l = ch.findCfg('Mon', d)
        self.assertIsNone(l)


class TestConfig(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_addCfg(self):
        '''
        Test add new configuration
        '''
        cfg = config.Config(4, "/dev/null")
        t1 = stime.STime(1, 0, 30)
        cfg.addCfg(0, 'Mon', t1)

        t2 = stime.STime(2, 30, 120)
        cfg.addCfg(0, 'Mon', t2)

        ch = cfg.getCfg(0)
        lstime = ch.getCfg('Mon')

        self.assertTrue(len(lstime) == 2, "Expected 2, get %d" % len(lstime))
        self.assertTrue(lstime[0].hour == 1 and lstime[1].hour == 2)

        self.assertRaises(ValueError, cfg.addCfg, 0, 'ERR', t1)
        self.assertRaises(ValueError, cfg.addCfg, 0, 'Mon', 1234)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestChannelConfig))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestConfig))

    return suite

if __name__ == "__main__":
    suite = suite()
    unittest.TextTestRunner(verbosity=2).run(suite)
