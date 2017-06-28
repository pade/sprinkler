'''
Created on 28 sept. 2016

@author: dassierp
'''

import logging
from multiprocessing import Process
from multiprocessing import Event
from multiprocessing import Queue
from program import Program
from stime import STime


class ServerData(object):
    '''
    Class to get data sent by server
    '''

    DAYNAME = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')

    def __init__(self):
        self.__day = None
        self.__channel = None
        self.__time = STime()
        self.__forceOn = False
        self.__forceOff = False

    def get_day(self):
        return self.__day

    def get_channel(self):
        return self.__channel

    def get_time(self):
        return self.__time

    def get_force_on(self):
        return self.__forceOn

    def get_force_off(self):
        return self.__forceOff

    def set_day(self, value):
        if value in self.DAYNAME:
            self.__day = value
        else:
            raise ValueError

    def set_channel(self, value):
        if type(value) is int:
            self.__channel = value
        else:
            raise ValueError

    def set_time(self, value):
        if isinstance(value, STime):
            self.__time = value
        else:
            raise ValueError

    def set_force_on(self, value):
        if isinstance(value, bool):
            self.__forceOn = value
        else:
            raise ValueError

    def set_force_off(self, value):
        if isinstance(value, bool):
            self.__forceOff = value
        else:
            raise ValueError

    day = property(get_day, set_day, None, None)
    channel = property(get_channel, set_channel, None, None)
    time = property(get_time, set_time, None, None)
    forceOn = property(get_force_on, set_force_on, None, None)
    forceOff = property(get_force_off, set_force_off, None, None)


class CheckProgram(object):
    '''
    Manage program modification
    '''

    def __init__(self, server, prog):
        '''
        Constructor
        Create a process dedicated to get new program from server
        @param server: a Server class to retreive server information
        @param prog: a Progam object to get and store the program
        '''
        self._stop = Event()
        self._process = Process(
            target=self._run, args=(server, prog, self._stop))
        self.__logger = logging.getLogger()
        self._q = Queue()

    def stop(self, wait=False):
        '''
        Stop communication process
        @param wait: If True, then block until internal subprocess is finished (default: False)
        '''
        self._stop.set()
        if wait:
            while self.is_alive():
                pass

    def _run(self, server, prog, stop):
        '''
        Get programation from server
        '''
        while not stop.is_set():
            pass
        # TODO

    def is_alive(self):
        '''
        Return True if the communication process with server is running
        '''
        return self._process.is_alive()

    def start(self):
        '''
        Start communication with server
        '''
        if not self.is_alive():
            self._logger.info("Starting communication with server")
            self._process.start()

    def is_new_prog(self):
        '''
        Check if a new programation is available
        @return: True if there is a new programation, False otherwise
        '''
        return not self._q.empty()

    def get_newprog(self):
        '''
        Get new program send by server side
        @return: None or a list of ServerData object
        '''
        prg = []
        while self.is_new_prog():
            prg.append(self._q.get(False))
        return prg
