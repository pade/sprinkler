# -*- coding: UTF-8 -*-

from slixmpp import ClientXMPP
from threading import Thread
from queue import Queue, Empty
import os
import tempfile
import pytest


class SendMsgBot(ClientXMPP):

    def __init__(self, recipient, xmpp_info):
        super(SendMsgBot, self).__init__(jid=xmpp_info['login'],
                                         password=xmpp_info['password'])
 
        self.recipient = recipient
        self.messages = Queue()
        self.th = Thread(target=self.process)
 
        self._server = xmpp_info['server']
 
        self.add_event_handler('session_start', self.start)
        self.add_event_handler("message", self.message)
 
        self.connect()

    def start(self, event):
        self.send_presence()
        self.get_roster()

    def connect(self):
        super(SendMsgBot, self).connect(self._server)
        self.th.start()

    def message(self, msg):
        if msg['type'] in ('normal', 'chat'):
            self.messages.put(msg)

    def get_message(self):
        try:
            return self.messages.get(block=True, timeout=30)
        except Empty:
            return None

    def is_message(self):
        return not self.messages.empty()

    def send_message(self, msg):
        super(SendMsgBot, self).send_message(mto=self.recipient, mbody=msg)

    def disconnect(self):
        super(SendMsgBot, self).disconnect(wait=False)

    def process(self):
        super(SendMsgBot, self).process(forever=True)


@pytest.fixture(scope='module')
def xmppbot(request):
    """ Create a bot to send XMPP message to sprinkler application """
    recipient = getattr(request.module, "xmpp_recipient")
    info = getattr(request.module, "xmpp_info")

    # xmppbot = SendMsgBot(recipient, info)
    # # Delete all pending message (if any)
    # while xmppbot.is_message():
    #     xmppbot.get_message()
    # yield xmppbot
    # xmppbot.disconnect()


@pytest.fixture
def confdir(request):
    """ Fixture to create the configuration directory used
    by sprinkler application """
    default_conf = getattr(request.module, "SPRINKLER_CONF")
    default_db = getattr(request.module, "CHANNEL_DB")

    with tempfile.TemporaryDirectory() as tmpdir:
        sprinkler_conf = os.path.join(tmpdir, "sprinkler.conf")
        channel_db = os.path.join(tmpdir, "channel.db")

        with open(sprinkler_conf, "w") as fd:
            fd.write(default_conf)
        with open(channel_db, "w") as fd:
            fd.write(default_db)
        yield tmpdir


@pytest.fixture
def tmpfile():
    """ Define a names temporary file """
    import tempfile
    with tempfile.NamedTemporaryFile() as tmpf:
        yield tmpf
