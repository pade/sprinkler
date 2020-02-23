# -*- coding: UTF-8 -*-

from jsonvalidate import Validate
import json
import os


class Database():
    """ program database interface"""

    def __init__(self, dbfile):
        """
        @param dbfile: full path of database file
        """
        self.dbfile = dbfile
        self.iscached = False
        self.validator = Validate()
        self.data = None

    def read(self):
        if not self.iscached:
            with open(self.dbfile, 'r') as fd:
                data = fd.read()
                self.data = self.validator.validate_string(data)
            self.iscached = True
        return self.data

    def write(self, data):
        self.iscached = False
        with open(self.dbfile, 'w') as fd:
            self.data = self.validator.validate_json(data)
            fd.write(json.dumps(data))
            self.iscached = True

    def update_channels(self, ch):
        prog = self.read()
        ch = self.validator.validate_channel(ch)
        nb = ch['nb']
        i = 0
        for channel in prog["channels"]:
            if channel["nb"] == nb:
                prog["channels"][i] = ch
                break
            i +=1
        self.write(prog)


        

    def file_exists(self):
        return os.path.isfile(self.dbfile)
