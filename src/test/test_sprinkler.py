# -*- coding: UTF-8 -*-

import sys
import os
from threading import Thread
import json
import pytest
import env_file
from pathlib import Path
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener
import logging

# Set parent directory in path, to be able to import module
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from sprinkler import MainApp

path = Path(os.path.dirname(os.path.abspath(__file__)))
env_file.load(os.path.join(path.parent.parent, ".env"))
# Now PUBKEY, SUBKEY and PUBNUBID are defined

SPRINKLER_CONF = f"""
[messages]
pubnub_subkey: {os.environ['SUBKEY']}
pubnub_pubkey: {os.environ['PUBKEY']}
id: {os.environ['PUBNUBID']}
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

@pytest.fixture(scope='function')
def launcher(confdir):
    app = MainApp(confdir, ['-d'])
    app_th = Thread(target=app.run)
    app_th.start()
    yield app
    app.stop_all()
    app_th.join()

@pytest.fixture
def pubnub_bot():
    path = Path(os.path.dirname(os.path.abspath(__file__)))
    env_file.load(os.path.join(path.parent.parent, ".env"))
    # Now PUBKEY, SUBKEY and PUBNUBID are defined
    pnconfig = PNConfiguration()
    pnconfig.subscribe_key = os.environ['SUBKEY']
    pnconfig.publish_key = os.environ['PUBKEY']
    pnconfig.subscribe_timeout = 20
    pnconfig.uuid = "d301009f-f274-435d-b2bb-40735d944392"
    pubnub_bot = PubNub(pnconfig)
    listener = SubscribeListener()
    pubnub_bot.add_listener(listener)
    pubnub_bot.subscribe().channels('sprinkler').execute()
    listener.wait_for_connect()
    pubnub_bot.listener = listener
    # Empty message queue
    while not listener.message_queue.empty():
        listener.message_queue.get()
    
    yield pubnub_bot
    
    pubnub_bot.unsubscribe_all()
    pubnub_bot.stop()

@pytest.mark.functional
def test_1(launcher, confdir, pubnub_bot):
    """ Test 'get program' command """
    logger = logging.getLogger('test')
    logger.setLevel(logging.DEBUG)
    pubnub_bot.publish().channel("sprinkler").message({"sender": pubnub_bot.uuid, "content": '{"command": "get program"}'}).sync()
    logger.info('SEND: {"command": "get program"}')


    msg = pubnub_bot.listener.message_queue.get(20)
    if msg.message['sender'] == pubnub_bot.uuid:
        msg = pubnub_bot.listener.message_queue.get(20)
    
    json_msg = json.loads(msg.message['content'])

    assert (json_msg['channels'][0]['progdays'][0]['stime']['hour'] == 5),\
        "Received message is: {}".format(msg['body'])


@pytest.mark.functional
def test_2(launcher, confdir, caplog, pubnub_bot):
    """ Test forced a channel ON """
    pubnub_bot.publish().channel("sprinkler").message({"sender": pubnub_bot.uuid, "content": '{"command": "force channel", "nb": "0", "action": "ON"}'}).sync()
    msg = pubnub_bot.listener.message_queue.get(20)
    if msg.message['sender'] == pubnub_bot.uuid:
        msg = pubnub_bot.listener.message_queue.get(20)

    assert (msg.message['content'] == '{"status": "OK"}')
    assert "Channel Jardin (0) ON" in caplog.text

@pytest.mark.functional
def test_3(launcher, confdir, pubnub_bot):
    """ Send a new program and
    check that it is correctly take into account """

    pubnub_bot.publish().channel("sprinkler").message({"sender": pubnub_bot.uuid, "content": '{"command": "get program"}'}).sync()
    msg = pubnub_bot.listener.message_queue.get(20)
    if msg.message['sender'] == pubnub_bot.uuid:
        msg = pubnub_bot.listener.message_queue.get(20)
    json_msg = json.loads(msg.message['content'])

    assert (json_msg['channels'][0]['progdays'][0]['stime']['hour'] == 5),\
        "Received message is: {}".format(msg.message['content'])

    pubnub_bot.publish().channel("sprinkler").message({"sender": pubnub_bot.uuid, "content": '{{"command": "new program", "program": {}}}'.format(NEW_CHANNEL_DB)}).sync()

    msg = pubnub_bot.listener.message_queue.get(20)
    if msg.message['sender'] == pubnub_bot.uuid:
        msg = pubnub_bot.listener.message_queue.get(20)
    json_msg = json.loads(msg.message['content'])

    assert (msg.message['content'] == '{"status": "OK"}'),\
        "Received message is: {}".format(msg.message['sender'])

    pubnub_bot.publish().channel("sprinkler").message({"sender": pubnub_bot.uuid, "content": '{"command": "get program"}'}).sync()

    msg = pubnub_bot.listener.message_queue.get(20)
    if msg.message['sender'] == pubnub_bot.uuid:
        msg = pubnub_bot.listener.message_queue.get(20)
    json_msg = json.loads(msg.message['content'])

    assert (json_msg['channels'][0]['progdays'][0]['stime']['hour'] == 6),\
        "Received message is: {}".format(msg.message['content'])
