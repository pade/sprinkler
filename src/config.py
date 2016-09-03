# -*- coding: UTF-8 -*-
'''
Created on 30 août 2016

@author: dassierp
'''

import json
import stime


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
        self.cfg = ()
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

    def setNewCfg(self, pNbChannel, pDay, pSTime):
        '''
        Set New configuration
        @param pNbChannel: channel number
        @param pDay: day of week: 'Mon', 'Tue', 'Wed',
                    'Thu', 'Fri', 'Sat' or'Sun'
        @param pSTime: STime object
        '''
        self.cfg[pNbChannel].setCfg(pDay, pSTime)

    def getCfg(self, pNbChannel, pDay=None):
        '''
        Get configuration from channel number
        @param pNbChannel: channel number
        @param pDay: if not set, return configuration for all days,
            otherwise, return configuration of the day
        @return: ChannelConfig object, or list of STime objects
        '''
        if pDay is None:
            return self.cfg[pNbChannel]
        else:
            return self.cfg[pNbChannel].day[pDay]


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
