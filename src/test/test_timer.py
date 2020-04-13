# -*- coding: UTF-8 -*-

import os
import sys
import time
import pytest
from datetime import datetime, timedelta
import time

import logging

# Set parent directory in path, to be able to import module
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import timer


def test_TimerSecond():
    def action(start):
        t.stop()
        assert((int(time.time())-start > 5.9) and (int(time.time())-start < 6.1))

    t = timer.Timer()
    t.program(1.0/60, action, argument=(int(time.time()),))
    t.start()

def test_SeveralTimer():
    nb_call = 0

    def action():
        nonlocal nb_call
        nb_call += 1

    t = timer.Timer()
    t.program(2.0/60.0, action)
    t.program(3.0/60.0, action)
    t.start()

    starttime = datetime.now()
    while(nb_call != 2 and  datetime.now() < starttime + timedelta(seconds=20)):
        pass
    t.stop()
    assert(nb_call == 2)

def test_ClearTimer():
    nb_call = 0

    def action():
        nonlocal nb_call
        nb_call += 1
    
    t = timer.Timer()
    t.program(1.0/60.0, action)
    t.program(2.0/60.0, action)
    t.start()
    t.clear()
    time.sleep(5)
    t.stop()
    assert(nb_call == 0)

def test_AddAndRemoveTimer():
    actionReached = [False, False]

    def action(nb):
        nonlocal actionReached
        actionReached[nb] = True

    t = timer.Timer()
    t.program(2.0/60.0, action, argument=(0,))
    t.start()
    t.clear()
    t.program(1.0/60.0, action, argument=(1,))
    time.sleep(5)
    t.stop()
    assert(actionReached[0] == False and actionReached[1] == True)



    