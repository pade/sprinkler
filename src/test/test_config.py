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


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestChannelConfig))
    return suite

if __name__ == "__main__":
    suite = suite()
    unittest.TextTestRunner(verbosity=2).run(suite)
