# -*- coding: UTF-8 -*-
'''
Created on 12 sept. 2016

@author: dassierp
'''


class Meteo(object):
    '''
    Get meteo information
    '''

    def __init__(self, url):
        '''
        Constructor
        @param url: URL to get information
        '''
        self._url = url
