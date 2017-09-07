# -*- coding: UTF-8 -*-

import os
import sys
import pytest

# Set parent directory in path, to be able to import module
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import channel
from hw import gpio


@pytest.fixture
def stubhw():
    class StubHw(gpio.BaseGpio):

        def __init__(self, pconfig):
            pass

        def write(self, pchannel, pvalue):
            pass

        def read(self, pchannel):
            return False

    return StubHw(None)

def testChannel(stubhw):
    '''Test update of the channel status'''
    ch = channel.Channel("Ch1", 0, stubhw)
    ch.isenable = True
    ch.running = True
    assert(ch.running is True)

    ch.running = False
    assert(ch.running is False)

def testInit(stubhw):
    '''On init, stop water'''
    ch = channel.Channel("Ch1", 0, stubhw)
    assert(ch.running is False)

def testEnable(stubhw):
    '''When disable channel never runs'''
    ch = channel.Channel("Citronnier", 0, stubhw)
    assert(ch.name == "Citronnier")
    ch.isenable = False
    assert(ch.running is False)

def testManual(stubhw):
    """Forced ON, OFF or return to AUTO"""
    ch = channel.Channel("Citronnier", 0, stubhw)
    assert(ch.manual == "AUTO")
    ch.manual = "OFF"
    assert(ch.manual == "OFF")
    ch.manual = "ON"
    assert(ch.manual == "ON")
    ch.manual = "DUMMY"
    assert(ch.manual == "AUTO")
