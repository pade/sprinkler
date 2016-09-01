# -*- coding: UTF-8 -*-
'''
Created on 30 août 2016

@author: dassierp
'''
from datetime import datetime

DAYOFWEEK = ('-', 'Mon', 'Tue', 'Wen', 'Thu', 'Fri', 'Sat', 'Sun')

class STime(object):
    '''
    Spinkler stime
    '''

    def __init__(self, day=0, hour=0, minute=0):
        '''
        Constructor
        @param day: day of the week, from 1 (monday) to 7 sunday, 0 if day is not set
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
        if day < 0 or day > 7:
            day = 0
        self.day = day
        
    def __str__(self):
        return "[%s] %02d:%02d" % (DAYOFWEEK[self.day], self.hour, self.minute)
    
    def getTime(self):
        return "%02d:%02d" % (self.hour, self.minute)
    
    def intoMinutes(self):
        '''
        Return the time into minutes
        '''
        return self.hour * 60 + self.minute
    
    def __add__(self, obj):
        '''
        Add STime object with another STime object of a duration in minutes
        @param obj: STime class instance or duration in minutes
        @return: a STimet instance class
        '''        
        if isinstance(obj, STime):
            (nbhour, minute) = ((self.minute + obj.minute)//60, (self.minute + obj.minute)%60)
            hour = (self.hour + obj.hour + nbhour)%24
        elif type(obj is int):
            # parameter is a duration in minute
            (nbhour, minute) = ((self.minute + obj)//60, (self.minute + obj)%60)
            hour = (self.hour + nbhour)%24
        else:
            raise ValueError

        # day is set, must be kept
        if self.day != 0:
            # If new computed hour is less than original one,then we change of day
            if hour < self.hour:
                day = self.day + 1
                if day == 7:
                    day = 1
            else:
                # day not change
                day = self.day
        
        return STime(day=day, hour=hour, minute=minute)

    @classmethod
    def now(cls):
        '''
        @return return a STime object with current TimeoutError
        '''
        t = datetime.now()
        return cls(hour = t.hour, minute = t.minute)
    