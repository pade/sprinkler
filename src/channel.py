# -*- coding: UTF-8 -*-
'''
Created on 29 ao�t 2016

@author: dassierp
'''
import logging

class Channel():
    '''
    Control a water channel
    '''
    def __init__(self, pChNumber, pHwInterface):
        '''
        Constructor
        @param pChNumber: channel number, from 0 to number of physical channel - 1
        @param pHwInterface: a class derived from BaseGpio
        '''
        self._nb = pChNumber
        self._hw = pHwInterface
        self._logger = logging.getLogger(__name__)
        
        # On initialisation, stop water
        self._state = False
        self.activate(False)
        self._logger.debug("Initialisation channel %s" % self._nb)        
        
    def activate(self, pState):
        '''
        @param pState: boolean, if pState is True, then activate the channel, otherwise channel is deactivated
        '''
        if pState is True:
            self._state = True
            self._logger.debug("Channel %s ON" % self._nb)
        else:
            self._state = False
            self._logger.debug("Channel %s OFF" % self._nb)
        self._hw.write(self._nb, self._state)

    
    def getState(self):
        '''
        @return: boolean, state of the channel
        '''
        return self._state
    
        