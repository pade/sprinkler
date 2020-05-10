# -*- coding: UTF-8 -*-
import configparser
import logging
import aiohttp
import asyncio
import datetime
from dateutil import parser


class Meteo(object):
    """
    Get meteo information
    """
    ACCTUWHEATER_URL = "http://dataservice.accuweather.com/forecasts/v1/daily/5day"

    def __init__(self, conf):
        """
        Constructor
        :param conf: configuration file path
        """
        self._file = conf
        config = configparser.ConfigParser()
        config.read_file(open(conf))
        self._log = logging.getLogger("sprinkler")
        self._withmeteo = True
        self._cached = {}
        try:
            self._apikey = config['meteo']['apikey']
            self._citykey = config['meteo']['citykey']
        except KeyError:
            self._log.warning("Missing meteo configuration")
            self._withmeteo = False

    @property
    def apikey(self):
        return self._apikey

    @property
    def citykey(self):
        return self._citykey

    @property
    def is_meteo(self):
        return self._withmeteo

    def set_city(self, key):
        config = configparser.ConfigParser()
        config.read_file(open(self._file))
        config['meteo']['citykey'] = self._citykey = key
        with open(self._file, 'w') as configfile:
            config.write(configfile)

    async def __get_meteo(self):
        if (len(self._cached) != 0 and self._cached['expiry'] < datetime.datetime.now()) or len(self._cached) == 0:
            url = self.ACCTUWHEATER_URL + "/" + self._citykey
            params = {'details': 'true', 'metric': 'true', 'apikey': self._apikey}
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as resp:
                    ret_code = resp.status
                    ret_value = await resp.json()
                    self._cached = {
                        'expiry': datetime.datetime.now() + datetime.timedelta(hours=6),
                        'data': (ret_code, ret_value)
                    }
                    return ret_code, ret_value
        else:
            return self._cached['data']

    def get_meteo(self, callback):
        def internal_callback(task):
            nonlocal callback
            ret_code, value = task.result()
            if ret_code != 200:
                callback({'error': True, 'message': value})
            else:
                try:
                    for forecast in value['DailyForecasts']:
                        d = parser.parse(forecast['Date'])
                        if d.date() == datetime.date.today() + datetime.timedelta(days=1):
                            precipitation = False
                            if forecast['Day']['HasPrecipitation'] or forecast['Night']['HasPrecipitation']:
                                if forecast['Day']['TotalLiquid']['Value'] + forecast['Night']['TotalLiquid'][
                                    'Value'] >= \
                                        10.0:
                                    precipitation = True
                            callback({'error': False, 'precipitation': precipitation})
                            return
                    callback({'error': True, 'message': 'Forecast not found'})
                except KeyError as e:
                    self._log.error(f"Error in forecast data: {str(e)} not found")
                    callback({'error': True, 'message': 'Forecast malformed'})

        if self._withmeteo:
            asyncio.create_task(self.__get_meteo()).add_done_callback(internal_callback)
        else:
            callback({'error': True, 'message': 'Meteo not configured'})
