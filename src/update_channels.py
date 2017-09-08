# -*- coding: UTF-8 -*-

from channel import Channel
from progdays import Progdays
from stime import STime
from jsonvalidate import Validate
import json
from hw.gpio import RaspberryGpio


class UpdateChannels():
    """ Create Channels from database definition """

    def __init__(self, database):
        """ Initilisation
        @param database: Database class instance to access to DB
        """
        self._db = database.read()

    def channels(self):
        """ Create new Channel object according to database
        @return: list of channel
        """
        ch_list = []
        for channel in self._db["channels"]:
            ch = Channel(pName=channel["name"],
                         pChNumber=channel["nb"],
                         pHwInterface=RaspberryGpio())
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
