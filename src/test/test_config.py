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
import tempfile

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

    def test_findCfg2(self):
        '''
        Test find configuration around midnight
        '''
        t1 = stime.STime(23, 30, 120)
        # Following date is a monday
        d1 = datetime.datetime(year=2016, month=9, day=5, hour=23, minute=45)
        ch = config.ChannelConfig(0)
        ch.setCfg('Mon', t1)
        l = ch.findCfg('Mon', d1)
        self.assertIsNotNone(l)


class TestConfig(unittest.TestCase):

    def setUp(self):
        fhandler, self.fname = tempfile.mkstemp(text=True)
        print ("Config file: %s" % self.fname)

    def tearDown(self):
        #os.remove(self.fname)
        pass

    def test_addCfg(self):
        '''
        Test add new configuration
        '''
        cfg = config.Config(4, self.fname)
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

    def test_save(self):
        '''
        Test save configuration into json
        '''
        cfg = config.Config(4, self.fname)
        t1 = stime.STime(1, 0, 30)
        t2 = stime.STime(20, 10, 120)
        cfg.addCfg(0, 'Mon', t1)
        cfg.addCfg(0, 'Mon', t2)
        cfg.addCfg(0, 'Tue', t1)
        cfg.addCfg(0, 'Fri', t2)
        cfg.active(0, True)

        cfg.save()

        cfg2 = config.Config(4, self.fname)
        cfg2.load()

        ch0 = cfg2.getCfg(0)
        monday = ch0.getCfg('Mon')
        self.assertTrue(len(monday) == 2)
        if monday[0].hour == 1:
            self.assertTrue(monday[0].hour == 1 and monday[0].minute == 0 and
                             monday[0].duration == 30)
            self.assertTrue(monday[1].hour == 20 and monday[1].minute == 10 and
                             monday[1].duration == 120)
        else:
            self.assertTrue(monday[1].hour == 1 and monday[1].minute == 0 and
                             monday[1].duration == 30)
            self.assertTrue(monday[0].hour == 20 and monday[0].minute == 10 and
                             monday[0].duration == 120)
        tuesday = ch0.getCfg('Tue')
        self.assertTrue(tuesday[0].hour == 1 and tuesday[0].minute == 0 and
                         tuesday[0].duration == 30)

        self.assertTrue(cfg2.isactive(0))
        self.assertFalse(cfg2.isactive(1))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestChannelConfig))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestConfig))

    return suite

if __name__ == "__main__":
    suite = suite()
    unittest.TextTestRunner(verbosity=2).run(suite)
