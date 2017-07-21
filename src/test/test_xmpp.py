# -*- coding: UTF-8 -*-

import unittest
import logging
import sys
import os

# Set parent directory in path, to be able to import module
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import xmpp


class TestXMPP(unittest.TestCase):
    """docstring for TestXMPP"""

    def setUp(self):
        self.server = ("server.jabber.hot-chilli.net", 80)
        self.jid = "sprinkler-test@jabber.hot-chilli.net"
        self.password = "!s20p21!"
        self._logger = logging.getLogger()

    def tearDown(self):
        pass

    def test_1(self):
        """ Test XMPP connexion """
        con = xmpp.XMPPData(login=self.jid,
                            password=self.password, server=self.server)

        con.connect()

        # Send a message manually
        #msg = con.messages.get()

        #con.send_message(mto=msg['from'], mbody="Received: {}".format(msg['body']))
        con.disconnect(wait=True)

