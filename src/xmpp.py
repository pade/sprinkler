# -*- coding: UTF-8 -*-


import logging
import sys
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout


class XMPPData(ClientXMPP):
    """docstring for XMPPData"""
    def __init__(self, jid, password):
        self._logger = logging.getLogger()
        ClientXMPP.__init__(self, jid, password)
        self._logger.debug("ClientXMPP init done.")

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)

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

        self.send_message(mto="pade087@movim.eu", mbody="Bonjour !")
        self.disconnect(wait=True)

    def message(self, msg):
        self._logger.debug("Receiving message: {}".format(msg['body']))

