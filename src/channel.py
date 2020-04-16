# -*- coding: UTF-8 -*-
'''
Created on 29 août 2016

@author: dassierp
'''
import logging
from progdays import Progdays


class Channel():
    '''
    Control a water channel
    '''

    def __init__(self, pName, pChNumber, pHwInterface):
        '''
        Constructor
        @param pName: channel name
        @param pChNumber: channel number, from 0 to number
        of physical channel - 1
        @param pHwInterface: a class derived from BaseGpio
        '''
        self.__nb = pChNumber
        self.__hw = pHwInterface
        self.__logger = logging.getLogger('sprinkler')
        self.__is_enable = False
        self.__manual = "AUTO"
        self.__name = pName
        self.__progdays = [Progdays(), Progdays()]

        # On initialisation, stop water
        self.__running = False
        self.__logger.debug(
            "Initialisation channel {} ({})".format(self.__name, self.__nb))

    def _get_nb(self):
        return self.__nb

    def _set_enable(self, pEnable):
        '''
        @param pEnable: True to enable the channel (can be used)
        '''
        self.__is_enable = pEnable

        if pEnable:
            self.__logger.info(
                "Channel {} ({}) is enabled".format(self.__name, self.__nb))
        else:
            self.__logger.info(
                "Channel {} ({}) is disabled".format(self.__name, self.__nb))

    def _get_enable(self):
        return self.__is_enable

    def _get_name(self):
        return self.__name

    def _set_name(self, pName):
        self.__name = pName

    def _get_running(self):
        return self.__running

    def _set_running(self, pState):
        '''
        @param pState: boolean, if pState is True, then channel runs,
        otherwise channel is not running
        If channel is not enable, do nothing
        '''
        if self.isenable is True:
            if pState is True:
                self.__running = True
                self.__logger.debug(
                    "Channel {} ({}) ON".format(self.name, self.nb))
            else:
                self.__running = False
                self.__logger.debug(
                    "Channel {} ({}) OFF".format(self.name, self.nb))
            self.__hw.write(self.__nb, self.__running)

    def _get_prog(self):
        return self.__progdays

    def _set_prog(self, progs):
        '''
        Set a new program
        @param progs: Table of Progdays class
        '''
        self.__progdays = progs

    def _set_manual(self, action):
        """ Manual command, superseds program
        @param action: must be: "OFF", "ON", or "AUTO"
        """
        if action == "ON":
            self.__manual = "ON"
        elif action == "OFF":
            self.__manual = "OFF"
        else:
            self.__manual = "AUTO"

    def _get_manual(self):
        return self.__manual

    nb = property(_get_nb, None, None, None)
    running = property(_get_running, _set_running, None, None)
    isenable = property(_get_enable, _set_enable, None, None)
    name = property(_get_name, _set_name, None, None)
    progs = property(_get_prog, _set_prog, None, None)
    manual = property(_get_manual, _set_manual, None, None)
