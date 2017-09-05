# -*- coding: UTF-8 -*-

from sleekxmpp import ClientXMPP
from threading import Thread
from queue import Queue


class SendMsgBot(ClientXMPP):

    def __init__(self, recipient, xmpp_info):
        super(SendMsgBot, self).__init__(xmpp_info['login'],
                                         xmpp_info['password'])

        self.recipient = recipient
        self.messages = Queue()
        self.th = Thread(target=self.process)

        self._server = xmpp_info['server']

        self.add_event_handler('session_start', self.start)
        self.add_event_handler("message", self.message)

        self.connect()
        self.th.start()

    def start(self, event):
        self.send_presence()
        self.get_roster()

    def connect(self):
        super(SendMsgBot, self).connect(self._server)

    def message(self, msg):
        if msg['type'] in ('normal', 'chat'):
            self.messages.put(msg)

    def get_message(self):
        return self.messages.get()

    def is_message(self):
        return not self.messages.empty()

    def send_message(self, msg):
        super(SendMsgBot, self).send_message(mto=self.recipient, mbody=msg)

    def disconnect(self):
        super(SendMsgBot, self).disconnect(wait=True)

    def process(self):
        super(SendMsgBot, self).process(block=True)

