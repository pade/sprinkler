# -*- coding: UTF-8 -*-

import sys
import os
import json

# Set parent directory in path, to be able to import module
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import update_channels
import database


curpath = os.path.dirname(os.path.abspath(__file__))


def test_update(tmpfile):
    """ Test update channels """
    db = database.Database(tmpfile.name)
    with open(os.path.join(curpath, "json_ok_2.js"), 'r') as fd:
        jsok = json.loads(fd.read())
    db.write(jsok)
    upd = update_channels.UpdateChannels(db)

    channels = upd.channels()

    assert(len(channels) == 4)

    ch0 = channels[0]

    assert(ch0.nb == 0)
    assert(ch0.name == "Channel 0")
    assert(ch0.isenable)
    assert(len(ch0.progs) == 2)
    assert(ch0.progs[0].isactive)
    assert(ch0.progs[0].get_one_day(1))
    assert(not ch0.progs[0].get_one_day(0))
    assert(ch0.progs[0].stime.hour == 10)
    assert(ch0.progs[0].stime.minute == 15)
    assert(ch0.progs[0].stime.duration == 30)

    ch1 = channels[1]

    assert(ch1.nb == 1)
    assert(ch1.name == "Channel 1")
    assert(not ch1.isenable)

