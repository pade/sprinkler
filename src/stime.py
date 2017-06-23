# -*- coding: UTF-8 -*-
'''
Created on 30 août 2016

@author: dassierp
'''
from datetime import datetime
from datetime import timedelta


class STime(object):
    '''
    Spinkler stime
    '''

    def __init__(self, hour=0, minute=0, duration=0):
        '''
        Constructor
        @param hour: hour, from 0 to 23. Outside this range, set to range limit
        @param minute: minute, from 0 to 59. Outside this range,
        set to range limit
        @param duration: duration of sprinkler, in minutes
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

        self.duration = duration

    def __str__(self):
        return "%02d:%02d [%d]" % (self.hour, self.minute, self.duration)

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

    def setTime(self, hour, minute):
        '''
        Set STime object with the string in argument
        @param hour: hour to set
        @param minute: minute to set
        Nota: duration is unchanged
        '''

        self.hour, self.minute = hour, minute

    def startDate(self, pDateTime):
        '''
        Convert STime to datetime object
        with day, month and year of pDateTime object
        @param pDateTime: Original datetime object to take into account
        '''
        return datetime(pDateTime.year, pDateTime.month, pDateTime.day,
                        self.hour, self.minute)

    def endDate(self, pDateTime):
        '''
        Convert STime to datetime object adding with duration
        with day, month and year of pDateTime object
        @param pDateTime: Original datetime object to take into account
        '''
        return self.startDate(pDateTime) + timedelta(minutes=self.duration)

    def setDuration(self, duration):
        '''
        Set duration (in minutes)
        '''
        self.duration = duration

    @classmethod
    def now(cls):
        '''
        @return return a STime object with current time
        '''
        t = datetime.now()
        return cls(hour=t.hour, minute=t.minute)
