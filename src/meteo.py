# -*- coding: UTF-8 -*-
'''
Created on 12 sept. 2016

@author: dassierp
'''

import urllib.request

URL = "http://www.meteofrance.com/mf3-rpc-portlet/rest/pluie/870500"


class Meteo(object):
    '''
    Get meteo information
    '''

    def __init__(self, url=URL):
        '''
        Constructor
        @param url: URL to get information
        '''
        self._url = url

    def get_info(self):
        s = urllib.request.urlopen(self._url).read()
        return s
