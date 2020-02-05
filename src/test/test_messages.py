# -*- coding: UTF-8 -*-

import sys
import os
import env_file
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener
import pubnub
from uuid import uuid4
from pathlib import Path
import logging
import pytest
from queue import Empty

# Set parent directory in path, to be able to import module
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import messages

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
    
    yield pubnub_bot
    pubnub_bot.unsubscribe_all()
    pubnub_bot.stop()

def test_receive(pubnub_bot, caplog):
    """ Test PubNub receive """

    caplog.set_level(logging.DEBUG)
    
    msg_con = messages.Messages(os.environ['SUBKEY'], os.environ['PUBKEY'], os.environ['PUBNUBID'])

    # purge message pipe
    while msg_con.is_message():
        msg_con.get_message()

    #pubnub.set_stream_logger('pubnub', logging.DEBUG)
    pubnub_bot.publish().channel("sprinkler").message({"sender": pubnub_bot.uuid, "content": "Hello my friend :)!"}).sync()

    msg = msg_con.get_message(20)  # wait until message is received
    assert msg == "Hello my friend :)!", f"Received {msg}"

    pubnub_bot.publish().channel("sprinkler").message({"sender": pubnub_bot.uuid, "content": '{"dummy": "data"}'}).sync()
    msg = msg_con.get_message(10)  # wait until message is received
    assert msg == '{"dummy": "data"}', f"Received {msg}"

    msg_con.stop()

def test_send(pubnub_bot, caplog):
    """ Test PubNub send """

    caplog.set_level(logging.DEBUG, logger="sprinkler")

    listener = SubscribeListener()
    pubnub_bot.add_listener(listener)
    pubnub_bot.subscribe().channels('sprinkler').execute()
    listener.wait_for_connect()

    # Empty message queue
    while not listener.message_queue.empty():
        listener.message_queue.get()

    msg_con = messages.Messages(os.environ['SUBKEY'], os.environ['PUBKEY'], os.environ['PUBNUBID'])
    msg_con.send("Test send message")

    msg = listener.message_queue.get(20)
    msg_con.stop()

    assert msg.message['content'] == "Test send message"


