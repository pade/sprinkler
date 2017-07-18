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
        self.server = "jabber.hot-chilli.net"
        self.jid = "pade087@jabber.hot-chilli.net"
        self.password = "yw5r3aa9"

    def tearDown(self):
        pass

    def test_1(self):
        """ Test XMPP connexion """
        con = xmpp.XMPPData(self.jid, self.password)
        con.register_plugin('xep_0030') # Service Discovery
        con.register_plugin('xep_0004') # Data Forms
        con.register_plugin('xep_0060') # PubSub
        con.register_plugin('xep_0199') # XMPP Ping
        #if con.connect(("server.jabber.hot-chilli.net", 80)):
        if con.connect(("prout", 80)):
            con.process(block=True)
        else:
            logging.error("Unable to connect")
            assert False

