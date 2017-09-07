# -*- coding: UTF-8 -*-

import os
import sys
from datetime import datetime
import pytest

# Set parent directory in path, to be able to import module
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import stime


def test_init():
    '''Test STime initialisation'''
    t = stime.STime(hour=5, minute=10)
    assert(t.hour == 5 and t.minute == 10)

    t = stime.STime(hour=25, minute=10)
    assert(t.hour == 23 and t.minute == 10)

    t = stime.STime(hour=-1, minute=10)
    assert(t.hour == 0 and t.minute == 10)

    t = stime.STime(hour=5, minute=60)
    assert(t.hour == 5 and t.minute == 59)

    t = stime.STime(hour=5, minute=-1)
    assert(t.hour == 5 and t.minute == 0)

def test_intoMinutes():
    '''Convert into minutes'''

    t = stime.STime(hour=5, minute=20)
    assert(t.intoMinutes() == 320)

def test_str():
    '''Test print STime'''
    str_stime = "%s" % stime.STime(hour=12, minute=10, duration=5)
    assert(str_stime == "12:10 [5]")

    str_stime = "%s" % stime.STime(hour=1, minute=2, duration=320)
    assert(str_stime == "01:02 [320]")

def test_add():
    '''Test add function with STime class'''
    t1 = stime.STime(hour=2, minute=10)

    t = t1 + 130
    assert(t.hour == 4 and t.minute == 20)

    t2 = stime.STime(hour=23, minute=10)
    t = t2 + 60
    assert(t.hour == 0 and t.minute == 10)

    t3 = stime.STime(hour=23, minute=45)
    t = t3 + 150
    assert(t.hour == 2 and t.minute == 15),\
                    "Expected 02:15, get %s" % t

def test_set():
    '''Test set method'''
    t = stime.STime()
    t.setTime(hour=2, minute=3)
    assert(t.hour == 2 and t.minute == 3)
    t.setTime(hour=5, minute=2)
    assert(t.hour == 5 and t.minute == 2)

def test_startDate():
    '''Test startDate method'''
    now = datetime(2016, 9, 1, 20, 30)
    t = stime.STime(5, 20)
    dt = t.startDate(now)
    assert(dt.year == now.year and dt.month == now.month and
                    dt.day == now.day and
                    dt.hour == t.hour and dt.minute == t.minute)

def test_endDate():
    '''Test endDate method'''
    now = datetime(2016, 9, 1, 20, 30)
    t = stime.STime(20, 30, 60)
    dt = t.endDate(now)
    assert(dt.year == now.year and dt.month == now.month and
                    dt.day == now.day and
                    dt.hour == 21 and dt.minute == 30)

    now = datetime(2016, 9, 1, 23, 30)
    t = stime.STime(23, 30, 60)
    dt = t.endDate(now)
    assert(dt.year == now.year and dt.month == now.month and
                    dt.day == now.day + 1 and
                    dt.hour == 0 and dt.minute == 30)

    now = datetime(2016, 9, 1, 23, 30)
    t = stime.STime(23, 0, 60)
    dt = t.endDate(now)
    assert(dt.year == now.year and dt.month == now.month and
                    dt.day == now.day + 1 and
                    dt.hour == 0 and dt.minute == 0)

def test_setDuration():
    '''Test setDuration method'''
    t = stime.STime(hour=1, minute=2, duration=10)
    assert(t.duration == 10)

def test_now():
    '''Text 'now()' class method'''
    t = stime.STime.now()
    dt = datetime.now()
    assert(t.hour == dt.hour and t.minute == dt.minute),\
                    "Expected %02d:%02d, get %s" % (dt.hour, dt.minute, t)
