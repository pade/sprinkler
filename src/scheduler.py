# -*- coding: UTF-8 -*-
'''
Created on 13 sept. 2016

@author: dassierp
'''

from threading import Thread, Event
import datetime
import logging
import asyncio


class Scheduler:
    '''
    Execute a function every minutes
    '''

    def __init__(self, target, args=()):
        """Constructor
        :param target: function to execute every minute
        :param args: tuple of arguments to pass to target"""

        self._sched = asyncio.create_task(self._run(target, args))
        self._logger = logging.getLogger('sprinkler')
        self._keep_running = True

    async def _run(self, target, args):
        """Execute target function every minutes
        :param target: function to execute
        :param args: argument to pass to function"""

        while self._keep_running:
            # Blocking call
            await asyncio.sleep(60 - datetime.datetime.now().second)
            self._logger.debug("Scheduler fires now...")
            if isinstance(args, tuple):
                target(*args)
            else:
                target(args)

    def cancel(self):
        self._sched.cancel()
