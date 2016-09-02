# -*- coding: UTF-8 -*-
'''
Created on 30 août 2016

@author: dassierp
'''
from datetime import datetime


class STime(object):
    '''
    Spinkler stime
    '''

    def __init__(self, hour=0, minute=0):
        '''
        Constructor
        @param hour: hour, from 0 to 23. Outside this range, set to range limit
        @param minute: minute, from 0 to 59. Outside this range, set to range limit
        '''
        if hour < 0:
            self.hour = 0
        elif hour > 23:
            self.hour = 23
        else:
            self.hour = hour
        if minute < 0:
            self.minute = 0
        elif minute > 59:
            self.minute = 59
        else:
            self.minute = minute

    def __str__(self):
        return "%02d:%02d" % (self.hour, self.minute)

    def intoMinutes(self):
        '''
        Return the time into minutes
        '''
        return self.hour * 60 + self.minute

    def __add__(self, pNbMinutes):
        '''
        Add STime object with a duration in minutes
        @param pNbMinutes: duration in minutes
        @return: a STimet instance class
        '''

        (nbhour, minute) = ((self.minute + pNbMinutes) // 60,
                            (self.minute + pNbMinutes) % 60)
        hour = (self.hour + nbhour) % 24
        return STime(hour=hour, minute=minute)

    def set(self, pStr):
        '''
        Set STime object with the string in argument
        @param pStr: Time string, format: "HH:MM"
        '''
        try:
            hour, minute = map(int, pStr.split(':'))
        except:
            raise ValueError

        self.hour, self.minute = hour, minute

    def toDateTime(self):
        '''
        Convert STime to datetime object
        with current day, month and year
        '''
        now = datetime.today()
        return datetime(now.year, now.month, now.day, self.hour, self.minute)

    @classmethod
    def now(cls):
        '''
        @return return a STime object with current TimeoutError
        '''
        t = datetime.now()
        return cls(hour=t.hour, minute=t.minute)
