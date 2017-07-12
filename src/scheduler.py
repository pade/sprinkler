# -*- coding: UTF-8 -*-
'''
Created on 13 sept. 2016

@author: dassierp
'''

from threading import Event
from threading import Thread
import datetime
import logging


class Scheduler(object):
    '''
    Execute a function every minutes
    '''

    def __init__(self, target, args=()):
        '''
        Constructor
        @param target: function to execute every minute
        @param args: tuple of arguments to pass to target
        '''
        self._stop = Event()
        self._args = (target, args, self._stop)
        self._sched = Thread(target=self._run, args=self._args)
        self._sched.start()
        self._logger = logging.getLogger()

    def schedule(self):
        """ Force reschduling """
        if isinstance(self._args[1], tuple):
            self._args[0](*self._args[1])
        else:
            self._args[0](self._args[1])

    def _run(self, target, args, stop):
        '''
        Execute target function every minutes
        @param target: function to execute
        @param args: argument to pass to function
        @param stop: Event object that is set to stop the execution
        '''
        oldtime = datetime.datetime.now()
        while not stop.is_set():
            newtime = datetime.datetime.now()
            if(newtime.minute != oldtime.minute):
                self._logger.debug("Scheduler fires now...")
                if isinstance(args, tuple):
                    target(*args)
                else:
                    target(args)
                oldtime = newtime
        # stop execution
        stop.clear()

    def stop(self):
        """
        Stop execution
        """
        self._stop.set()

    def is_alive(self):
        """ Return True if target function is schedule every minute
        """
        return self._sched.is_alive()

    def start(self):
        """
        Start execution
        """
        if not self.is_alive():
            self._sched.start()
