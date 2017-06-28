# -*- coding: UTF-8 -*-

from datetime import datetime
import unittest
from unittest.mock import MagicMock
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

        self.hw1 = StubHw(None)
        self.hw2 = StubHw(None)
        self.ch1 = channel.Channel("Channel 1", 0, self.hw1)
        self.ch2 = channel.Channel("Channel 2", 1, self.hw2)

        self.ch1.progs = [progdays.Progdays(), progdays.Progdays()]
        self.ch2.progs = [progdays.Progdays(), progdays.Progdays()]

        self.ch1.isenable = True
        self.ch1.progs[0].stime = stime.STime(hour=5, minute=0, duration=30)
        self.ch1.progs[0].isactive = True
        self.ch1.progs[0].set_days([True, True, True, True, True, True, True])

    def tearDown(self):
        pass

    def test_1(self):
        """When channel is not enable, do nothing"""
        self.ch1.isenable = False

        e = engine.Engine([self.ch1])
        # Stop scheduler, not used here
        e.stop()

        e.run()

        self.assertFalse(self.hw1.cmd)

    def test_2(self):
        """Activate channel when time is done"""
        # logger = logging.getLogger()
        # logger.level = logging.DEBUG
        # stream_handler = logging.StreamHandler(sys.stdout)
        # logger.addHandler(stream_handler)

        e = engine.Engine([self.ch1])
        # Stop scheduler, not used here
        e.stop()

        # Mock engine function to force date and time
        e.get_datetime_now = MagicMock(
            return_value=datetime(2017, 6, 23, 5, 15))
        e.run()
        self.assertTrue(self.hw1.cmd)

        e.get_datetime_now = MagicMock(
            return_value=datetime(2017, 6, 23, 5, 31))
        e.run()
        self.assertFalse(self.hw1.cmd)

    def test_3(self):
        """When prog is not active do nothing"""
        self.ch1.progs[0].isactive = False

        e = engine.Engine([self.ch1])
        # Stop scheduler, not used here
        e.stop()

        # Mock engine function to force date and time
        e.get_datetime_now = MagicMock(
            return_value=datetime(2017, 6, 23, 5, 15))

        e.run()
        self.assertFalse(self.hw1.cmd)

    def test_4(self):
        """Deactivate channel outside time range"""
        e = engine.Engine([self.ch1])
        # Stop scheduler, not used here
        e.stop()

        # Mock engine function to force date and time
        e.get_datetime_now = MagicMock(
            return_value=datetime(2017, 6, 23, 5, 31))

        e.run()
        self.assertFalse(self.hw1.cmd)

        # Mock engine function to force date and time
        e.get_datetime_now = MagicMock(
            return_value=datetime(2017, 6, 23, 4, 59))

        e.run()
        self.assertFalse(self.hw1.cmd)

    def test_5(self):
        """Deactivate channel when current day is not selected"""
        # Set Friday off
        self.ch1.progs[0].set_one_day(4, False)

        e = engine.Engine([self.ch1])
        # Stop scheduler, not used here
        e.stop()

        # Mock engine function to force date and time
        # 23 june 2017 is Friday
        e.get_datetime_now = MagicMock(
            return_value=datetime(2017, 6, 23, 5, 15))

        e.run()
        self.assertFalse(self.hw1.cmd)

    def test_6(self):
        """Where some day are off, other days must runs"""

        self.ch1.progs[0].set_one_day(0, False)
        self.ch1.progs[0].set_one_day(1, False)
        self.ch1.progs[0].set_one_day(2, False)
        self.ch1.progs[0].set_one_day(3, False)
        self.ch1.progs[0].set_one_day(4, False)
        self.ch1.progs[0].set_one_day(6, False)

        e = engine.Engine([self.ch1])
        # Stop scheduler, not used here
        e.stop()

        # 24 june 2017 is Saturday
        e.get_datetime_now = MagicMock(
            return_value=datetime(2017, 6, 24, 5, 15))

        e.run()
        self.assertTrue(self.hw1.cmd)

    def test_7(self):
        """ Test when time is around midnight """

        self.ch1.progs[1].stime = stime.STime(hour=23, minute=50, duration=40)
        self.ch1.progs[1].isactive = True
        self.ch1.progs[1].set_days([True, True, True, True, True, True, True])

        e = engine.Engine([self.ch1])
        # Stop scheduler, not used here
        e.stop()

        # Mock engine function to force date and time
        e.get_datetime_now = MagicMock(
            return_value=datetime(2017, 6, 23, 23, 55))
        e.run()
        self.assertTrue(self.hw1.cmd)

        # Mock engine function to force date and time
        e.get_datetime_now = MagicMock(
            return_value=datetime(2017, 6, 24, 0, 1))
        e.run()
        self.assertTrue(self.hw1.cmd)

        # Mock engine function to force date and time
        e.get_datetime_now = MagicMock(
            return_value=datetime(2017, 6, 24, 0, 31))
        e.run()
        self.assertFalse(self.hw1.cmd)

    def test_2Channels(self):
        """ Test 2 channels in parallel"""
        self.ch2.progs = [progdays.Progdays(), progdays.Progdays()]

        self.ch2.isenable = True
        self.ch2.progs[0].stime = stime.STime(hour=5, minute=15, duration=30)
        self.ch2.progs[0].isactive = True
        self.ch2.progs[0].set_days([True, True, True, True, True, True, True])

        e = engine.Engine([self.ch1, self.ch2])
        # Stop scheduler, not used here
        e.stop()

        # Mock engine function to force date and time
        e.get_datetime_now = MagicMock(
            return_value=datetime(2017, 6, 24, 4, 59))
        e.run()

        self.assertTrue(not self.hw1.cmd and not self.hw2.cmd)

        e.get_datetime_now = MagicMock(
            return_value=datetime(2017, 6, 24, 5, 10))
        e.run()

        self.assertTrue(self.hw1.cmd and not self.hw2.cmd)

        e.get_datetime_now = MagicMock(
            return_value=datetime(2017, 6, 24, 5, 20))
        e.run()

        self.assertTrue(self.hw1.cmd and self.hw2.cmd)

        e.get_datetime_now = MagicMock(
            return_value=datetime(2017, 6, 24, 5, 31))
        e.run()

        self.assertTrue(not self.hw1.cmd and self.hw2.cmd)


# def suite():
#     suite = unittest.TestSuite()
#     suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestEngine))
#     return suite


# if __name__ == "__main__":

#     suite = suite()
#     unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(suite)
