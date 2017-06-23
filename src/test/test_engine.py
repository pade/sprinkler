# -*- coding: UTF-8 -*-

from datetime import datetime
import unittest
from unittest.mock import MagicMock
import logging
import sys
import os

# Set parent directory in path, to be able to import module
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import engine
import channel
import progdays
import stime
from hw import gpio


class TestEngine(unittest.TestCase):

    def setUp(self):
        class StubHw(gpio.BaseGpio):

            def __init__(self, pconfig):
                self.cfg = pconfig
                self.cmd = False

            def write(self, pchannel, pvalue):
                self.cmd = pvalue

            def read(self, pchannel):
                return self.cmd

        self.hw = StubHw(None)
        self.ch1 = channel.Channel("Channel 1", 0, self.hw)
        self.ch2 = channel.Channel("Channel 2", 1, self.hw)

        self.ch1.progs = [progdays.Progdays(), progdays.Progdays()]
        self.ch2.progs = [progdays.Progdays(), progdays.Progdays()]

    def tearDown(self):
        pass

    def test_1(self):
        """
        When channel is not enable, do nothing
        """
        self.ch1.isenable = False

        e = engine.Engine([self.ch1])
        # Stop scheduler, not used here
        e._sched.stop()

        e.run()

        self.assertFalse(self.hw.cmd)

    def test_2(self):
        """
        Activate channel when time is done
        """
        #logger = logging.getLogger()
        #logger.level = logging.DEBUG
        #stream_handler = logging.StreamHandler(sys.stdout)
        #logger.addHandler(stream_handler)
        self.ch1.isenable = True
        self.ch1.progs[0].stime = stime.STime(hour=5, minute=0, duration=30)
        self.ch1.progs[0].isactive = True
        self.ch1.progs[0].set_days([True, True, True, True, True, True, True])

        e = engine.Engine([self.ch1])
        # Stop scheduler, not used here
        e._sched.stop()

        # Mock engine function to force date and time
        e.get_datetime_now = MagicMock(
            return_value=datetime(2017, 6, 23, 5, 15))

        e.run()

        self.assertTrue(self.hw.cmd)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestEngine))
    return suite


if __name__ == "__main__":

    suite = suite()
    unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(suite)
