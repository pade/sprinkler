# -*- coding: UTF-8 -*-

from datetime import datetime
from unittest.mock import MagicMock
import sys
import os
import time
import pytest
import logging

# Set parent directory in path, to be able to import module
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import engine
from channel import Channel
import progdays
import stime
from hw import gpio


class StubHw(gpio.BaseGpio):

    def __init__(self, pconfig):
        self.cfg = pconfig
        self.cmd = False

    def write(self, pchannel, pvalue):
        self.cmd = pvalue

    def read(self, pchannel):
        return self.cmd


class ChannelInit():

    def __init__(self):
        self.hw1 = StubHw(None)
        self.hw2 = StubHw(None)
        self.ch1 = Channel("Channel 1", 0, self.hw1)
        self.ch2 = Channel("Channel 2", 1, self.hw2)

        self.ch1.progs = [progdays.Progdays(), progdays.Progdays()]
        self.ch2.progs = [progdays.Progdays(), progdays.Progdays()]

        self.ch1.isenable = True
        self.ch1.progs[0].stime = stime.STime(hour=5, minute=0, duration=30)
        self.ch1.progs[0].isactive = True
        self.ch1.progs[0].set_days([True, True, True, True, True, True, True])


@pytest.fixture
def channel():
    return ChannelInit()


def test_1(channel):
    """When channel is not enable, do nothing"""
    channel.ch1.isenable = False

    e = engine.Engine([channel.ch1])
    # Stop scheduler, not used here
    e.stop()
    e.run()

    assert(not channel.hw1.cmd)

def test_2(channel):
    e = engine.Engine([channel.ch1])
    # Stop scheduler, not used here
    e.stop()

    # Mock engine function to force date and time
    e.get_datetime_now = MagicMock(
        return_value=datetime(2017, 6, 23, 5, 15))
    e.run()
    assert(channel.hw1.cmd)

    e.get_datetime_now = MagicMock(
        return_value=datetime(2017, 6, 23, 5, 31))
    e.run()
    assert(not channel.hw1.cmd)

def test_3(channel):
    """When prog is not active do nothing"""
    channel.ch1.progs[0].isactive = False

    e = engine.Engine([channel.ch1])
    # Stop scheduler, not used here
    e.stop()

    # Mock engine function to force date and time
    e.get_datetime_now = MagicMock(
        return_value=datetime(2017, 6, 23, 5, 15))

    e.run()
    assert(not channel.hw1.cmd)

def test_4(channel):
    """Deactivate channel outside time range"""
    e = engine.Engine([channel.ch1])
    # Stop scheduler, not used here
    e.stop()

    # Mock engine function to force date and time
    e.get_datetime_now = MagicMock(
        return_value=datetime(2017, 6, 23, 5, 31))

    e.run()
    assert(not channel.hw1.cmd)

    # Mock engine function to force date and time
    e.get_datetime_now = MagicMock(
        return_value=datetime(2017, 6, 23, 4, 59))

    e.run()
    assert(not channel.hw1.cmd)

def test_5(channel):
    """Deactivate channel when current day is not selected"""
    # Set Friday off
    channel.ch1.progs[0].set_one_day(4, False)

    e = engine.Engine([channel.ch1])
    # Stop scheduler, not used here
    e.stop()

    # Mock engine function to force date and time
    # 23 june 2017 is Friday
    e.get_datetime_now = MagicMock(
        return_value=datetime(2017, 6, 23, 5, 15))

    e.run()
    assert(not channel.hw1.cmd)

def test_6(channel):
    """Where some day are off, other days must runs"""

    channel.ch1.progs[0].set_one_day(0, False)
    channel.ch1.progs[0].set_one_day(1, False)
    channel.ch1.progs[0].set_one_day(2, False)
    channel.ch1.progs[0].set_one_day(3, False)
    channel.ch1.progs[0].set_one_day(4, False)
    channel.ch1.progs[0].set_one_day(6, False)

    e = engine.Engine([channel.ch1])
    # Stop scheduler, not used here
    e.stop()

    # 24 june 2017 is Saturday
    e.get_datetime_now = MagicMock(
        return_value=datetime(2017, 6, 24, 5, 15))

    e.run()
    assert(channel.hw1.cmd)

def test_7(channel):
    """ Test when time is around midnight """

    channel.ch1.progs[1].stime = stime.STime(hour=23, minute=50, duration=40)
    channel.ch1.progs[1].isactive = True
    channel.ch1.progs[1].set_days([True, True, True, True, True, True, True])

    e = engine.Engine([channel.ch1])
    # Stop scheduler, not used here
    e.stop()

    # Mock engine function to force date and time
    e.get_datetime_now = MagicMock(
        return_value=datetime(2017, 6, 23, 23, 55))
    e.run()
    assert(channel.hw1.cmd)

    # Mock engine function to force date and time
    e.get_datetime_now = MagicMock(
        return_value=datetime(2017, 6, 24, 0, 1))
    e.run()
    assert(channel.hw1.cmd)

    # Mock engine function to force date and time
    e.get_datetime_now = MagicMock(
        return_value=datetime(2017, 6, 24, 0, 31))
    e.run()
    assert(not channel.hw1.cmd)

def test_2Channels(channel):
    """ Test 2 channels in parallel"""
    channel.ch2.progs = [progdays.Progdays(), progdays.Progdays()]

    channel.ch2.isenable = True
    channel.ch2.progs[0].stime = stime.STime(hour=5, minute=15, duration=30)
    channel.ch2.progs[0].isactive = True
    channel.ch2.progs[0].set_days([True, True, True, True, True, True, True])

    e = engine.Engine([channel.ch1, channel.ch2])
    # Stop scheduler, not used here
    e.stop()

    # Mock engine function to force date and time
    e.get_datetime_now = MagicMock(
        return_value=datetime(2017, 6, 24, 4, 59))
    e.run()

    assert(not channel.hw1.cmd and not channel.hw2.cmd)

    e.get_datetime_now = MagicMock(
        return_value=datetime(2017, 6, 24, 5, 10))
    e.run()

    assert(channel.hw1.cmd and not channel.hw2.cmd)

    e.get_datetime_now = MagicMock(
        return_value=datetime(2017, 6, 24, 5, 20))
    e.run()

    assert(channel.hw1.cmd and channel.hw2.cmd)

    e.get_datetime_now = MagicMock(
        return_value=datetime(2017, 6, 24, 5, 31))
    e.run()

    assert(not channel.hw1.cmd and channel.hw2.cmd)

def test_forcedOff(channel):
    """ Forced OFF when  running """

    e = engine.Engine([channel.ch1])
    # Stop scheduler, not used here
    e.stop()

    # Force time into a running period
    e.get_datetime_now = MagicMock(
        return_value=datetime(2017, 6, 23, 5, 15))
    e.run()
    assert(channel.hw1.cmd)
    channel.ch1.manual = "OFF"
    e.run()
    assert(not channel.hw1.cmd)
    channel.ch1.manual = "AUTO"
    e.run()
    assert(channel.hw1.cmd)

def test_forcedOn(channel):
    """ Forced ON when not running """

    e = engine.Engine([channel.ch1])
    # Stop scheduler, not used here
    e.stop()

    # Force time outside a running period
    e.get_datetime_now = MagicMock(
        return_value=datetime(2017, 6, 23, 5, 45))
    e.run()
    assert(not channel.hw1.cmd)
    channel.ch1.manual = "ON"
    e.run()
    assert(channel.hw1.cmd)
    channel.ch1.manual = "AUTO"
    e.run()
    assert(not channel.hw1.cmd)

def test_forcedOn_2(channel):
    """ Forced ON when not running using Engine class """
    e = engine.Engine([channel.ch1])
    # Stop scheduler, not used here
    e.stop()

    # Force time outside a running period
    e.get_datetime_now = MagicMock(
        return_value=datetime(2017, 6, 23, 5, 45))
    e.run()
    assert(not channel.hw1.cmd)

    e.channel_forced(0, "ON", 0.1)
    assert(channel.hw1.cmd)

    e.channel_forced(0, "AUTO")
    assert(not channel.hw1.cmd)

def test_forcedOff_2(channel):
    """ Forced OFF when not running using Engine class """
    e = engine.Engine([channel.ch1])
    # Stop scheduler, not used here
    e.stop()

    # Force time into a running period
    e.get_datetime_now = MagicMock(
        return_value=datetime(2017, 6, 23, 5, 15))
    e.run()
    assert(channel.hw1.cmd)

    e.channel_forced(0, "OFF")
    assert(not channel.hw1.cmd)

    e.channel_forced(0, "AUTO")
    assert(channel.hw1.cmd)

@pytest.mark.longtest
@pytest.mark.functional
def test_forcedOnDuration(channel):
    """ Forced ch1 ON for 2 minutes """
    e = engine.Engine([channel.ch1])
    # Force time outside a running period
    e.get_datetime_now = MagicMock(
        return_value=datetime(2017, 6, 23, 5, 45))

    e.channel_forced(0, "ON", 2)
    assert(channel.hw1.cmd)
    time.sleep(3*60)
    assert(not channel.hw1.cmd)
    e.stop()

@pytest.mark.longtest
@pytest.mark.functional
def test_forcedOnDurationBoth(channel):
    """ Forced ch1 ON for 2 minutes and then for 1 minute """
    logger = logging.getLogger('test')
    logger.setLevel(logging.DEBUG)
    e = engine.Engine([channel.ch1])
    # Force time outside a running period
    e.get_datetime_now = MagicMock(
        return_value=datetime(2017, 6, 23, 5, 45))

    e.channel_forced(0, "ON", 2)
    assert(channel.hw1.cmd)
    e.channel_forced(0, "ON", 1)
    time.sleep(60+10)
    assert(not channel.hw1.cmd)
    e.stop()