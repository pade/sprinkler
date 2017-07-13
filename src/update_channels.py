# -*- coding: UTF-8 -*-

from channel import Channel
from progdays import Progdays
from stime import STime
from jsonvalidate import Validate
import json


class UpdateChannels():
    """ Create Channels from database definition """

    def __init__(self, database):
        """ Initilisation
        @param database: file descriptor or filename of database
        """
        self.read_db(database)

    def read_db(self, database):
        """ Read database
        @param database: file descriptor or filename of database
        raise an error in case of malformed JSON
        """
        if hasattr(database, "read"):
            # database parameter is a file descriptor
            self._db = database.read()
        else:
            with open(database, "r") as fd:
                self._db = fd.read()

        validate = Validate()
        validate.validate_string(self._db)
        self._json = json.loads(self._db)

    def channels(self):
        """ Create new Channel object according to database
        @return: list of channel
        """
        ch_list = []
        for channel in self._json["channels"]:
            ch = Channel(pName=channel["name"],
                         pChNumber=channel["nb"],
                         pHwInterface=None)
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
