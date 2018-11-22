# -*- coding: UTF-8 -*-

import sys
import os
from threading import Thread
import json
import pytest


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
            "is_enable": true,
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

NEW_CHANNEL_DB = """
{
    "channels": [
        {
            "nb": 0,
            "name": "Jardin",
            "is_enable": true,
            "progdays": [
                {
                    "is_active": false,
                    "days": [false, false, false,
                             false, false, false, false],
                    "stime":
                    {
                        "hour": 6,
                        "minute": 10,
                        "duration": 30
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


code_to_test = {
    'server': ("server.jabber.hot-chilli.net", 443),
    'login': "sprinkler-tu@jabber.hot-chilli.net",
    'password': "!s20p21!"
}

tester = {
    'server': ("server.jabber.hot-chilli.net", 443),
    'login': "sprinkler-test@jabber.hot-chilli.net",
    'password': "!s20p21!"
}

xmpp_info = tester
xmpp_recipient = code_to_test['login']


@pytest.fixture(scope='function')
def launcher(confdir):
    app = MainApp(confdir, ['-d'])
    app_th = Thread(target=app.run)
    app_th.start()
    yield app
    app.stop_all()
    app_th.join()


@pytest.mark.functional
def test_1(launcher, xmppbot, confdir):
    """ Test 'get program' command """
    xmppbot.send_message('{"command": "get program"}')
    msg = xmppbot.get_message()
    json_msg = json.loads(msg['body'])

    assert (json_msg['channels'][0]['progdays'][0]['stime']['hour'] == 5),\
        "Received message is: {}".format(msg['body'])


@pytest.mark.functional
def test_2(launcher, xmppbot, confdir, caplog):
    """ Test forced a channel ON """
    xmppbot.send_message(
        '{"command": "force channel", "nb": "0", "action": "ON"}'
    )
    msg = xmppbot.get_message()
    assert (msg['body'] == '{"status": "OK"}')
    assert "Channel Jardin (0) ON" in caplog.text


@pytest.mark.functional
def test_3(launcher, xmppbot, confdir):
    """ Send a new program and
    check that it is correctly take into account """

    xmppbot.send_message('{"command": "get program"}')
    msg = xmppbot.get_message()
    json_msg = json.loads(msg['body'])

    assert (json_msg['channels'][0]['progdays'][0]['stime']['hour'] == 5),\
        "Received message is: {}".format(msg['body'])

    xmppbot.send_message('{{"command": "new program", "program": {}}}'
                         .format(NEW_CHANNEL_DB))
    msg = xmppbot.get_message()

    assert (msg['body'] == '{"status": "OK"}'),\
        "Received message is: {}".format(msg['body'])

    xmppbot.send_message('{"command": "get program"}')
    msg = xmppbot.get_message()
    json_msg = json.loads(msg['body'])

    assert (json_msg['channels'][0]['progdays'][0]['stime']['hour'] == 6),\
        "Received message is: {}".format(msg['body'])
