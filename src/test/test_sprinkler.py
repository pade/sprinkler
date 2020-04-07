# -*- coding: UTF-8 -*-

import sys
import os
from threading import Thread
import json
import pytest
from pathlib import Path
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener
import logging

# Set parent directory in path, to be able to import module
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from sprinkler import MainApp

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

UPDATE_CHANNEL = """
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
}
"""

@pytest.fixture
def launcher(confdir):
    app = MainApp(confdir, ['-d'])
    app_th = Thread(target=app.run)
    app_th.start()
    yield app
    app.stop_all()
    app_th.join()

@pytest.fixture
def pubnub_bot(setenv):
    pnconfig = PNConfiguration()
    pnconfig.subscribe_key = os.environ['SUBKEY']
    pnconfig.publish_key = os.environ['PUBKEY']
    pnconfig.subscribe_timeout = 20
    pnconfig.uuid = "d301009f-f274-435d-b2bb-40735d944392"
    pnconfig.ssl = True
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
def test_1(launcher, confdir, pubnub_bot, setenv):
    """ Test 'get program' command """
    logger = logging.getLogger('test')
    logger.setLevel(logging.DEBUG)
    pubnub_bot.publish().channel("sprinkler").message({"content": '{"command": "get program"}'}).sync()
    logger.info('SEND: {"command": "get program"}')


    msg = pubnub_bot.listener.message_queue.get(20)
    if msg.publisher == pubnub_bot.uuid:
        msg = pubnub_bot.listener.message_queue.get(20)
    
    json_msg = json.loads(msg.message['content'])

    assert (json_msg['channels'][0]['progdays'][0]['stime']['hour'] == 5),\
        "Received message is: {}".format(msg['body'])


@pytest.mark.functional
def test_2(launcher, confdir, caplog, pubnub_bot, setenv):
    """ Test forced a channel ON """
    pubnub_bot.publish().channel("sprinkler").message({"content": '{"command": "force channel", "nb": "0", "action": "ON", "duration": "1"}'}).sync()
    msg = pubnub_bot.listener.message_queue.get(20)
    if msg.publisher == pubnub_bot.uuid:
        msg = pubnub_bot.listener.message_queue.get(20)

    assert (msg.message['content'] == '{"status": "OK"}')
    assert "Channel Jardin (0) ON" in caplog.text

@pytest.mark.functional
def test_3(launcher, confdir, pubnub_bot, setenv):
    """ Send a new program and
    check that it is correctly take into account """

    pubnub_bot.publish().channel("sprinkler").message({"content": '{"command": "get program"}'}).sync()
    msg = pubnub_bot.listener.message_queue.get(20)
    if msg.publisher == pubnub_bot.uuid:
        msg = pubnub_bot.listener.message_queue.get(20)
    json_msg = json.loads(msg.message['content'])

    assert (json_msg['channels'][0]['progdays'][0]['stime']['hour'] == 5),\
        "Received message is: {}".format(msg.message['content'])

    pubnub_bot.publish().channel("sprinkler").message({"content": '{{"command": "new program", "program": {}}}'.format(NEW_CHANNEL_DB)}).sync()

    msg = pubnub_bot.listener.message_queue.get(20)
    if msg.publisher == pubnub_bot.uuid:
        msg = pubnub_bot.listener.message_queue.get(20)
    json_msg = json.loads(msg.message['content'])

    assert (msg.message['content'] == '{"status": "OK"}'),\
        "Received message is: {}".format(msg.message['sender'])

    pubnub_bot.publish().channel("sprinkler").message({"content": '{"command": "get program"}'}).sync()

    msg = pubnub_bot.listener.message_queue.get(20)
    if msg.publisher == pubnub_bot.uuid:
        msg = pubnub_bot.listener.message_queue.get(20)
    json_msg = json.loads(msg.message['content'])

    assert (json_msg['channels'][0]['progdays'][0]['stime']['hour'] == 6),\
        "Received message is: {}".format(msg.message['content'])

@pytest.mark.functional
def test_4(launcher, confdir, pubnub_bot, setenv):
    """ Send a new channel and
    check that it is correctly take into account """

    pubnub_bot.publish().channel("sprinkler").message({"content": '{"command": "get program"}'}).sync()
    msg = pubnub_bot.listener.message_queue.get(20)
    if msg.publisher == pubnub_bot.uuid:
        msg = pubnub_bot.listener.message_queue.get(20)
    json_msg = json.loads(msg.message['content'])

    assert (json_msg['channels'][0]['progdays'][0]['stime']['hour'] == 5),\
        "Received message is: {}".format(msg.message['content'])

    pubnub_bot.publish().channel("sprinkler").message({"content": '{{"command": "new channel", "program": {}}}'.format(UPDATE_CHANNEL)}).sync()

    msg = pubnub_bot.listener.message_queue.get(20)
    if msg.publisher == pubnub_bot.uuid:
        msg = pubnub_bot.listener.message_queue.get(20)
    json_msg = json.loads(msg.message['content'])

    assert (msg.message['content'] == '{"status": "OK"}'),\
        "Received message is: {}".format(msg.message['sender'])

    pubnub_bot.publish().channel("sprinkler").message({"content": '{"command": "get program"}'}).sync()

    msg = pubnub_bot.listener.message_queue.get(20)
    if msg.publisher == pubnub_bot.uuid:
        msg = pubnub_bot.listener.message_queue.get(20)
    json_msg = json.loads(msg.message['content'])

    assert (json_msg['channels'][0]['progdays'][0]['stime']['hour'] == 6),\
        "Received message is: {}".format(msg.message['content'])
