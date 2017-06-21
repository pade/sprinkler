# -*- coding: UTF-8 -*-
'''
Created on 30 août 2016

@author: dassierp
'''

import os.path
import sys
import stime
import datetime
import jsonpickle

# Constant
DAYLIST = {'Mon': 0, 'Tue': 1, 'Wed': 2, 'Thu': 3, 'Fri': 4, 'Sat': 5, 'Sun': 6}


class ProgramError(Exception):
    pass


class FileNotExist(ProgramError):
    def __init__(self, pFilename,):
        self.filename = pFilename
        Exception.__init__(self, 'File %s not found.' % self.filename)


class LoadError(ProgramError):
    def __init__(self, pFilename, pTrace):
        self.filename = pFilename
        self.type = pTrace[0]
        self.value = pTrace[1]


class SaveError(ProgramError):
    def __init__(self, pFilename, pTrace):
        self.filename = pFilename
        self.type = pTrace[0]
        self.value = pTrace[1]


class ProgramId(object):
    '''
    To store a program
    '''
    DAYNAME = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')

    def __init__(self, day, progid, progtime):
        '''
        Constructor
        '''
        self.day = day
        self.progid = progid
        self.progtime = progtime

    def get_day(self):
        return self.__day

    def get_progid(self):
        return self.__progid

    def get_progtime(self):
        return self.__progtime

    def set_day(self, value):
        if value in self.DAYNAME:
            self.__day = value
        else:
            raise ValueError

    def set_progid(self, value):
        self.__progid = value

    def set_progtime(self, value):
        if isinstance(value, stime.STime):
            self.__progtime = value
        else:
            raise ValueError

    day = property(get_day, set_day, None, None)
    progid = property(get_progid, set_progid, None, None)
    progtime = property(get_progtime, set_progtime, None, None)


class ChannelProgram(object):
    '''
    Configuration of one channel
    '''

    def __init__(self, pChannel):
        '''
        Constructor
        @param pChannel: Channel number
        '''
        self.number = pChannel
        self.prog = []
        self._activate = False

    def getCfg(self, day):
        '''
        Get configuration from given day
        @param day: given day
        @return: list of STime object
        '''
        retval = []
        for p in self.prog:
            if p.day == day:
                retval.append(p)
        return retval

    def setCfg(self, day, progid, pSTime):
        '''
        Set configuration for given day
        @param day: given day
        @param progid: config id to set
        @param pSTime: STime object
        '''
        p = ProgramId(day=day, progid=progid, progstime=pSTime)
        self.prog.append(p)

    def enable(self, active):
        '''
        Activate/deactivate the channel
        @param active: True to _activate, False to deactivate
        '''
        if active:
            self._activate = True
        else:
            self._activate = False

    def isenable(self):
        '''
        Return the state of the channel
        '''
        return self._activate

    def findCfg(self, day, pDateTime):
        '''
        Try to find a configuration for the given day that match the time
        Configuration is return when pDateTime is between STime and STime + duration
        @paramd day: day to looking for
        @param pDataTime: datetime object
        @return: None or a list of STime object matching the search
        '''
        retval = []
        for p in self.getCfg(day):
            # Check if day's of the week are corresponding
            if pDateTime.weekday() == DAYLIST[day]:
                start = p.progstime.startDate(pDateTime)
                end = p.progstime.endDate(pDateTime)
                if start <= pDateTime and end > pDateTime:
                    retval.append(p.progstime)

        if len(retval) == 0:
            # Nothing found
            return None
        else:
            return retval


class Program(object):
    '''
    Configuration management class
    '''

    def __init__(self, pNbOfChannel, pFileName):
        '''
        Constructor
        @param pNbOfChannel: Number of physical channel
        @param pFileName: Filename with path to store configuration
        '''
        self._filename = pFileName
        self._cfg = []
        jsonpickle.set_preferred_backend('json')
        jsonpickle.set_encoder_options('json', sort_keys=True, indent=4)

        for i in range(pNbOfChannel):
            self._cfg.append(ChannelProgram(i))

    def save(self):
        '''
        Save configuration into file
        '''
        try:
            f = open(self._filename, 'w')
            json_obj = jsonpickle.encode(self._cfg)
            f.write(json_obj)
            f.close()
        except:
            err = sys.exc_info()
            raise SaveError(self._filename, err)

    def load(self):
        '''
        Load configuration from file
        '''
        if os.path.isfile(self._filename):
            try:
                f = open(self._filename, 'r')
                json_str = f.read()
                self._cfg = jsonpickle.decode(json_str)
                f.close()
            except:
                err = sys.exc_info()
                raise LoadError(self._filename, err)
        else:
            raise FileNotExist(self._filename)

    def addCfg(self, pNbChannel, pDay, pSTime):
        '''
        Set New configuration
        @param pNbChannel: channel number
        @param pDay: day of week: 'Mon', 'Tue', 'Wed',
                    'Thu', 'Fri', 'Sat' or'Sun'
        @param pSTime: STime object
        '''
        if pDay in ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'):
            if isinstance(pSTime, stime.STime):
                self._cfg[pNbChannel].setCfg(pDay, pSTime)
            else:
                raise ValueError
        else:
            raise ValueError

    def getCfg(self, pNbChannel):
        '''
        Get configuration from channel number
        @param pNbChannel: channel number
        @return: ChannelProgram object
        '''
        return self._cfg[pNbChannel]

    def enable(self, pNbChannel, pActive):
        '''
        Activate/deactivate the channel
        @param pNbChannel: Channel number
        @param pActive: True to _activate, False to deactivate
        '''
        if pActive:
            self._cfg[pNbChannel].enable(True)
        else:
            self._cfg[pNbChannel].enable(False)

    def isenable(self, pNbChannel):
        '''
        Return the state of the channel
        '''
        return self._cfg[pNbChannel].isenable()
