# -*- coding: UTF-8 -*-

import pytest
import sys
import os
import json

# Set parent directory in path, to be able to import module
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import database


curpath = os.path.dirname(os.path.abspath(__file__))


def test_read_write(tmpfile):
    db = database.Database(tmpfile.name)
    with open(os.path.join(curpath, "json_ok.js"), 'r') as fd:
        jsok = json.loads(fd.read())
    db.write(jsok)

    db2 = database.Database(tmpfile.name)
    jsread = db2.read()

    assert(jsok == jsread)
