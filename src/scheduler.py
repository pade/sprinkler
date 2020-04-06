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
        self._stop = False
        self._sched = Thread(target=self._run, args=(target, args))
        self._sched.start()
        self._logger = logging.getLogger('sprinkler')

    def _run(self, target, args):
        '''
        Execute target function every minutes
        @param target: function to execute
        @param args: argument to pass to function
        '''
        oldtime = datetime.datetime.now()
        while not self._stop:
            newtime = datetime.datetime.now()
            if(newtime.minute != oldtime.minute):
                self._logger.debug("Scheduler fires now...")
                if isinstance(args, tuple):
                    target(*args)
                else:
                    target(args)
                oldtime = newtime

    def stop(self):
        """
        Stop execution
        """
        self._stop = True

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
