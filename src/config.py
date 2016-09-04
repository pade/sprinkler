# -*- coding: UTF-8 -*-
'''
Created on 30 août 2016

@author: dassierp
'''

import json
import stime
import datetime


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
        self.activate = False

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
        self.cfg = []
        for i in range(pNbOfChannel):
            self.cfg.append(ChannelConfig(i))

    def save(self):
        '''
        Save configuration into file
        '''
        pass

    def load(self):
        '''
        Load configuration from file
        '''
        pass

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
                self.cfg[pNbChannel].setCfg(pDay, pSTime)
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
        return self.cfg[pNbChannel]


class ConfigEncoder(json.JSONEncoder):
    '''
    Encode configuration into JSON format
    '''
    def default(self, pObj):
        if isinstance(pObj, Config):
            # TODO: return JSON structure to fill
            pass
        return json.JSONEncoder.default(self.pObj)


class ConfigDecoder(json.JSONDecoder):
    '''
    Decode configuration from JSON format
    '''
    def default(self, pStr):
        # TODO: return a 'Config' instance with attribute read from JSON string pStr
        pass
