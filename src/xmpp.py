# -*- coding: UTF-8 -*-


import logging
import sys
import Queue
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout


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
        self._q = Queue.Queue()

        self.register_plugin("xep_0030")  # Service Discovery
        self.register_plugin('xep_0004')  # Data Forms
        self.register_plugin('xep_0060')  # PubSub
        self.register_plugin('xep_0199')  # XMPP Ping

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)

    def get_queue():
        """ Return a Queue object where received messages are stores """
        return self._q

    def connect():
        if self._server == ():
            self._logger.info(
                "Connecting to XMPP server, using JID information")
            con = super().connect()
        else:
            self._logger.info("Connection to {}:{}".format(
                self._server[0], self._server[1]))
            con = super().connect(self._server)

        if not con:
            self._logger.error("Unable to connect")
        else:
            self._logger.info("Connexion established")
            self.process()

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
        self._logger.debug(
            "Receiving message from {}: {}".format(msg['from'], msg['body']))
        self._q.put(msg)

