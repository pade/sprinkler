# -*- coding: UTF-8 -*-

from channel import Channel
from progdays import Progdays
from stime import STime
from jsonvalidate import Validate
import json
try:
    from hw.raspberry import RaspberryGpio as Gpio
except:
    from hw.dummy import DummyGpio as Gpio

class UpdateChannels():
    """ Create Channels from database definition """

    def __init__(self, database):
        """ Initilisation
        @param database: Database class instance to access to DB
        """
        self._db = database.read()
        self._gpio = Gpio()

    def channels(self):
        """ Create new Channel object according to database
        @return: list of channel
        """
        ch_list = []
        for channel in self._db["channels"]:
            ch = Channel(pName=channel["name"],
                         pChNumber=channel["nb"],
                         pHwInterface=self._gpio)
            ch.isenable = channel["is_enable"]
            ch.progs = self._progdays(channel["progdays"])
            ch_list.append(ch)
        return ch_list

    def _progdays(self, progdays):
        """ Create Progdays class """
        prg_list = []
        for progday in progdays:
            prg = Progdays()
            prg.isactive = progday["is_active"]
            prg.set_days(progday["days"])
            prg.stime = STime(hour=progday["stime"]["hour"],
                              minute=progday["stime"]["minute"],
                              duration=progday["stime"]["duration"])
            prg_list.append(prg)
        return prg_list
