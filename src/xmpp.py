# -*- coding: UTF-8 -*-


import logging
import sys
from queue import Queue
from slixmpp import ClientXMPP
from threading import Thread
from slixmpp.exceptions import IqError, IqTimeout


class XMPPData(ClientXMPP):
    """Manage connexion with external device"""

    def __init__(self, login, password, server=()):
        """Class constructor
        :param server: tuple for server information:
        server[0] is server URL, and server [1] server port
        :param login: login on server
        :param password: associated password
        """
        self._logger = logging.getLogger()
        ClientXMPP.__init__(self, jid=login, password=password)
        self._server = server
        self.messages = Queue()
        self.th = Thread(target=self.process)

        self.register_plugin("xep_0030")  # Service Discovery
        self.register_plugin('xep_0004')  # Data Forms
        self.register_plugin('xep_0060')  # PubSub
        self.register_plugin('xep_0199')  # XMPP Ping

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)

        self.connect()

    def connect(self):
        self._logger.info("Connection to {}:{}".format(
            self._server[0], self._server[1]))
        super().connect()
        self.th.start()
        
    def session_start(self, event):
        self.send_presence()
        try:
            self.get_roster()
        except IqError as err:
            self._logger.error("Error when getting the roster")
            self._logger.error(err.iq['error']['condition'])
            self.disconnect()
        except IqTimeout:
            self._logger.error("XMPP server too long to answer")
            self.disconnect()

    def message(self, msg):
        if msg['type'] in ('normal', 'chat'):
            self._logger.debug(
                "Receiving message from {}: {}"
                .format(msg['from'], msg['body']))
            self.messages.put(msg)

    def stop(self):
        super().disconnect(wait=False)
        self.loop.stop()

    def get_message(self, timeout=None):
        return self.messages.get(timeout=timeout)

    def process(self):
        super().process(forever=True)

    def is_message(self):
        return not self.messages.empty()
