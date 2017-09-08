# -*- coding: UTF-8 -*-

from datetime import datetime, timedelta
from unittest.mock import MagicMock
import pytest
import sys
import os

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
        now = datetime.now()
        self.ch1.progs[0].stime = stime.STime(
            hour=now.hour, minute=now.minute + 2, duration=1)
        self.ch1.progs[0].isactive = True
        self.ch1.progs[0].set_days([True, True, True, True, True, True, True])


@pytest.fixture
def channel():
    return ChannelInit()


@pytest.mark.longtest
def test_long_time(channel):
    """ Long time test, using scheduler function
    """

    e = engine.Engine([channel.ch1])
    assert(not channel.hw1.cmd)

    now_plus_3 = datetime.now() + timedelta(minutes=3)
    while (not channel.hw1.cmd) and (now_plus_3 > datetime.now()):
        pass

    assert(channel.hw1.cmd)

    now_plus_3 = datetime.now() + timedelta(minutes=3)
    while (channel.hw1.cmd) and (now_plus_3 > datetime.now()):
        pass

    assert(not channel.hw1.cmd)

    e.stop()

# Set 'long_test' attribute to run this specific test
# without running others
test_long_time.long_test = True
