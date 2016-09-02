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
        self.day = {'Mon': False, 'Tue': False, 'Wed': False,
                    'Thu': False, 'Fri': False, 'Sat': False, 'Sun': False}
        self.startTime = stime.STime()
        self.duration = stime.STime()
        self.activate = False


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
