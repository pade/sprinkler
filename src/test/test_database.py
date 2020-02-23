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

new_channel = """
{
    "nb": 1,
    "name": "New channel 1",
    "is_enable": false,
    "progdays": [
        {
            "is_active": true,
            "days": [true, false, true,
                        false, true, false, true],
            "stime":
            {
                "hour": 8,
                "minute": 8,
                "duration": 8
            }
        },
        {
            "is_active": false,
            "days": [false, false, false,
                        false, false, false, false],
            "stime":
            {
                "hour": 0,
                "minute": 0,
                "duration": 0
            }
        }
    ]
}
"""

def test_update_channel(tmpfile):
    db = database.Database(tmpfile.name)
    with open(os.path.join(curpath, "json_ok.js"), 'r') as fd:
        jsok = json.loads(fd.read())
    db.write(jsok)
    db.update_channels(json.loads(new_channel))
    prog = db.read()
    for ch in prog["channels"]:
        if ch["nb"] == 1:
            assert(ch["name"] == "New channel 1")
            assert(ch["progdays"][0]["stime"]["hour"] == 8)

