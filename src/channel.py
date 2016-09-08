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
        self.__nb = pChNumber
        self.__hw = pHwInterface
        self.__logger = logging.getLogger(__name__)

        # On initialisation, stop water
        self.__state = False
        self.activate(False)
        self.__logger.debug("Initialisation channel %s" % self.__nb)

    def get_nb(self):
        return self.__nb

    def get_state(self):
        return self.__state

    def activate(self, pState):
        '''
        @param pState: boolean, if pState is True, then ac_activatehe channel,
        otherwise channel is deactivated
        '''
        if pState is True:
            self.__state = True
            self.__logger.debug("Channel %s ON" % self.__nb)
        else:
            self.__state = False
            self.__logger.debug("Channel %s OFF" % self.__nb)
        self.__hw.write(self.__nb, self.__state)

    nb = property(get_nb, None, None, None)
    state = property(get_state, None, None, None)
