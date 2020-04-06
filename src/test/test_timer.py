# -*- coding: UTF-8 -*-

import os
import sys
import time
import pytest

# Set parent directory in path, to be able to import module
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import timer

def testSingleton():
    t1 = timer.Timer()
    t2 = timer.Timer()
    assert(id(t1) == id(t2))

def testTimerSecond():
    def action(start):
        t.stop()
        assert(int(time.time())-start == 6.0)

    t = timer.Timer()
    t.program(0.1, action, argument=(int(time.time()),))
    t.start()
