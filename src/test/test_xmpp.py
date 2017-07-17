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
        self.server = "https://007jabber.com/"
        self.jid = "sprinkler-test@007jabber.com"
        self.password = "!s20p21!"

    def tearDown(self):
        pass

    def test_1(self):
        """ Test XMPP connexion """
        con = xmpp.XMPPData(self.jid, self.password)
        con.connect()
        con.process(block=False)

