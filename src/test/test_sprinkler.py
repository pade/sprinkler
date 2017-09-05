# -*- coding: UTF-8 -*-

import unittest
import logging
import sys
import os
from threading import Thread
from xmppbot import SendMsgBot
import tempfile


# Set parent directory in path, to be able to import module
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from sprinkler import MainApp

SPRINKLER_CONF = """
[xmpp]
server = server.jabber.hot-chilli.net
password = !s20p21!
login = sprinkler-tu@jabber.hot-chilli.net
port = 80
"""

CHANNEL_DB = """
{
    "channels": [
        {
            "nb": 0,
            "name": "Jardin",
            "is_enable": false,
            "progdays": [
                {
                    "is_active": true,
                    "days": [false, false, false,
                             false, true, false, false],
                    "stime":
                    {
                        "hour": 5,
                        "minute": 0,
                        "duration": 45
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
        },
        {
            "nb": 1,
            "name": "Channel 1",
            "is_enable": false,
            "progdays": [
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
        },
        {
            "nb": 2,
            "name": "Channel 2",
            "is_enable": false,
            "progdays": [
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
        },
        {
            "nb": 3,
            "name": "Channel 3",
            "is_enable": false,
            "progdays": [
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
    ]
}
"""


class TestXMPP(unittest.TestCase):
    """Functional test of sprinkler application"""

    def setUp(self):
        self._logger = logging.getLogger()

        self.code_to_test = {
            'server': ("server.jabber.hot-chilli.net", 80),
            'login': "sprinkler-tu@jabber.hot-chilli.net",
            'password': "!s20p21!"
        }

        self.tester = {
            'server': ("server.jabber.hot-chilli.net", 80),
            'login': "sprinkler-test@jabber.hot-chilli.net",
            'password': "!s20p21!"
        }

        self.tmpdir = tempfile.TemporaryDirectory()
        sprinkler_conf = os.path.join(self.tmpdir.name, "sprinkler.conf")
        channel_db = os.path.join(self.tmpdir.name, "channel.db")

        with open(sprinkler_conf, "w") as fd:
            fd.write(SPRINKLER_CONF)
        with open(channel_db, "w") as fd:
            fd.write(CHANNEL_DB)

    def tearDown(self):
        pass

    def test_1(self):
        app = MainApp(self.tmpdir.name, ['-d'])
        app_th = Thread(target=app.run)
        app_th.start()
        msgbot = SendMsgBot(self.code_to_test['login'],
                            self.tester)
        msgbot.send_message('{"command": "get program"}')
        msg = msgbot.get_message()

        msgbot.disconnect()
        app.stop_all()
        app_th.join()

        self.assertTrue(msg['body'] == CHANNEL_DB,
                        msg="Received message is: {}".format(msg['body']))
