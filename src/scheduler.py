# -*- coding: UTF-8 -*-
'''
Created on 13 sept. 2016

@author: dassierp
'''

from threading import Thread, Event
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
        self._sched = Thread(target=self._run, args=(target, args))
        self._sched.start()
        self._logger = logging.getLogger('sprinkler')

    def _run(self, target, args):
        '''
        Execute target function every minutes
        @param target: function to execute
        @param args: argument to pass to function
        '''

        keep_running = True
        while keep_running:
            # Blocking call
            if self._stop.wait(timeout=60 - datetime.datetime.now().second):
                # Event is set, thread shall stop
                keep_running = False
            else:
                self._logger.debug("Scheduler fires now...")
                if isinstance(args, tuple):
                    target(*args)
                else:
                    target(args)
        self._logger.debug("Stop scheduler thread")

    def stop(self):
        """ Stop execution"""
        self._stop.set()

    def is_alive(self):
        """ Return True if target function is schedule every minute
        """
        return self._sched.is_alive()

    def start(self):
        """Start execution"""
        if not self.is_alive():
            self._sched.start()
