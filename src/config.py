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


class ConfigError(Exception):
    pass


class FileNotExist(ConfigError):
    def __init__(self, pFilename,):
        self.filename = pFilename
        Exception.__init__(self, 'File %s not found.' % self.filename)


class LoadError(ConfigError):
    def __init__(self, pFilename, pTrace):
        self.filename = pFilename
        self.type = pTrace[0]
        self.value = pTrace[1]


class SaveError(ConfigError):
    def __init__(self, pFilename, pTrace):
        self.filename = pFilename
        self.type = pTrace[0]
        self.value = pTrace[1]


class ChannelConfig(object):
    '''
    Configuration of one channel
    '''

    def __init__(self, pChannel):
        '''
        Constructor
        @param pChannel: Channel number
        '''
        self.number = pChannel
        self.day = {'Mon': [], 'Tue': [], 'Wed': [],
                    'Thu': [], 'Fri': [], 'Sat': [], 'Sun': []}
        self._activate = False

    def getCfg(self, pDay):
        '''
        Get configuration from given day
        @param pDay: given day
        @return: list of STime object
        '''
        return self.day[pDay]

    def setCfg(self, pDay, pSTime):
        '''
        Set configuration for given day
        @param pDay: given day
        @param pSTime: STime object
        '''
        self.day[pDay].append(pSTime)

    def enable(self, pActive):
        '''
        Activate/deactivate the channel
        @param pActive: True to _activate, False to deactivate
        '''
        if pActive:
            self._activate = True
        else:
            self._activate = False

    def isenable(self):
        '''
        Return the state of the channel
        '''
        return self._activate

    def findCfg(self, pDay, pDateTime):
        '''
        Try to find a configuration for the given day that match the time
        Configuration is return when pDateTime is between STime and STime + duration
        @param pDay: day to looking for
        @param pDataTime: datetime object
        @return: None or a list of STime object matching the search
        '''
        ret_val = []
        for t in self.day[pDay]:
            # Check if day's of the week are corresponding
            if pDateTime.weekday() == DAYLIST[pDay]:
                start = t.toDateTime(pDateTime)
                end = start + datetime.timedelta(minutes=t.duration)
                if start <= pDateTime and end > pDateTime:
                    ret_val.append(t)

        if len(ret_val) == 0:
            # Nothing found
            return None
        else:
            return ret_val


class Config(object):
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
            self._cfg.append(ChannelConfig(i))

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
        @return: ChannelConfig object
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
