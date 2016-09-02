# -*- coding: UTF-8 -*-
'''
Created on 30 août 2016

@author: dassierp
'''


class BaseGpio(object):
    '''
    GPIO interface class
    '''

    def __init__(self, pConfig):
        '''
        Constructor
        @param pConfig: HW configuration parameter
        '''
        self.hwcfg = pConfig

    def write(self, pchannel, pvalue):
        raise NotImplementedError

    def read(self, pchannel):
        raise NotImplementedError


class RaspberryGpio(BaseGpio):
    '''
    GPIO management for Raspberry
    '''
    def __init__(self, pConfig):
        super(RaspberryGpio, self).__init__(pConfig)

    def write(self, pchannel, pvalue):
        pass

    def read(self, pchannel):
        pass
