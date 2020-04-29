# -*- coding: UTF-8 -*-

import sys
import os
from pubnub.pubnub_asyncio import PubNubAsyncio, SubscribeListener
from pubnub.pnconfiguration import PNConfiguration
import logging
import pytest
import aiohttp

# Set parent directory in path, to be able to import module
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import messages


@pytest.fixture(scope="function")
async def pubnub_bot(setenv):
    pnconfig = PNConfiguration()
    pnconfig.subscribe_key = os.environ['SUBKEY']
    pnconfig.publish_key = os.environ['PUBKEY']
    pnconfig.subscribe_timeout = 20
    pnconfig.uuid = "d301009f-f274-435d-b2bb-40735d944392"
    pnconfig.ssl = True

    pubnub_bot = PubNubAsyncio(pnconfig)

    yield pubnub_bot
    pubnub_bot.unsubscribe_all()
    await pubnub_bot.stop()

async def send(msg):
    """ Send a JSON object
    :param: msg: JSON object to send
    """
    pubkey = os.environ['PUBKEY']
    subkey = os.environ['SUBKEY']
    id = "d301009f-f274-435d-b2bb-40735d944392"
    channel = "sprinkler"
    full_url = f"https://ps.pndsn.com/publish/{pubkey}/{subkey}/0/{channel}/0?uuid={id}"

    async with aiohttp.ClientSession() as session:
        async with session.post(full_url, json=msg) as resp:
            assert resp.status == 200, f"Received {await resp.text()}"


@pytest.mark.asyncio
async def test_receive(caplog):
    """ Test PubNub receive """
    caplog.set_level(logging.DEBUG)
    msg_con = messages.Messages(os.environ['SUBKEY'], os.environ['PUBKEY'], os.environ['PUBNUBID'])
    # purge message pipe
    while msg_con.is_message():
        await msg_con.get_message()

    await send({"content": "Hello my friend :)!"})
    msg = await msg_con.get_message()  # wait until message is received
    assert msg == "Hello my friend :)!", f"Received {msg}"

    await send({"content": '{"dummy": "data"}'})
    msg = await msg_con.get_message()  # wait until message is received
    assert msg == '{"dummy": "data"}', f"Received {msg}"

    await msg_con.stop()


@pytest.mark.asyncio
async def test_send(pubnub_bot, caplog):
    """ Test PubNub send """

    caplog.set_level(logging.DEBUG, logger="sprinkler")

    listener = SubscribeListener()
    pubnub_bot.add_listener(listener)
    pubnub_bot.subscribe().channels('sprinkler').execute()
    listener.wait_for_connect()

    # Empty message queue
    while not listener.message_queue.empty():
        await listener.message_queue.get()

    msg_con = messages.Messages(os.environ['SUBKEY'], os.environ['PUBKEY'], os.environ['PUBNUBID'])
    await msg_con.send("Test send message")

    msg = await listener.message_queue.get()
    await msg_con.stop()

    assert msg.message['content'] == "Test send message"
