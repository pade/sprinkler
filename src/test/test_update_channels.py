# -*- coding: UTF-8 -*-

import unittest
import logging
import sys
import os

# Set parent directory in path, to be able to import module
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import update_channels


class TestUpdateChannels(unittest.TestCase):

    def setUp(self):
        self._curpath = os.path.dirname(os.path.abspath(__file__))

    def tearDown(self):
        pass

    def test_update(self):
        """ Test update channels """

        upd = update_channels.UpdateChannels(
            os.path.join(self._curpath, "json_ok_2.js"))

        channels = upd.channels()

        self.assertTrue(len(channels) == 4)

        ch0 = channels[0]

        self.assertTrue(ch0.nb == 0)
        self.assertTrue(ch0.name == "Channel 0")
        self.assertTrue(ch0.isenable)
        self.assertTrue(len(ch0.progs) == 2)
        self.assertTrue(ch0.progs[0].isactive)
        self.assertTrue(ch0.progs[0].get_one_day(1))
        self.assertFalse(ch0.progs[0].get_one_day(0))
        self.assertTrue(ch0.progs[0].stime.hour == 10)
        self.assertTrue(ch0.progs[0].stime.minute == 15)
        self.assertTrue(ch0.progs[0].stime.duration == 30)

        ch1 = channels[1]

        self.assertTrue(ch1.nb == 1)
        self.assertTrue(ch1.name == "Channel 1")
        self.assertFalse(ch1.isenable)

