# -*- coding: UTF-8 -*-
'''
Created on 30 août 2016

@author: dassierp
'''

import logging

class BaseGpio(object):
    '''
    GPIO interface class
    '''

    def __init__(self, pConfig):
        '''
        Constructor
        :param pConfig: HW configuration parameter
        '''
        self.hwcfg = pConfig
        self._log = logging.getLogger('sprinkler')

    def write(self, pchannel, pvalue):
        # pchannel from 0 to 3
        raise NotImplementedError

    def read(self, pchannel):
        # pchannel from 0 to 3
        raise NotImplementedError


