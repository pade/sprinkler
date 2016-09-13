# -*- coding: UTF-8 -*-
'''
Created on 13 sept. 2016

@author: dassierp
'''

from threading import Event
from threading import Thread
import datetime
import time


class Scheduler(object):
    '''
    Class to schedule an event every minute
    '''

    def __init__(self, stop_event):
        '''
        Constructor
        @pram stop_event: An Event object, that must be set by main application to stop the schduler
        '''
        self._event = Event()
        self._stop_event = stop_event
        self._sched = Thread(target=self._run, args=(self._event, self._stop_event))

    def _run(self, event, stop_event):
        '''
        scheduler
        @param event: Event is set every number of seconds
        @param stop_event: Event object that must be set to stop thread
        '''
        oldtime = datetime.datetime().now()
        while not stop_event.is_set():
            newtime = datetime.datetime().now()
            if(newtime.minutes != oldtime.minutes):
                event.set()
                oldtime = newtime
            # sleep a little
            time.sleep(1)

    def get_event(self):
        return self._event

    def is_alive(self):
        return self._sched.is_alive()
