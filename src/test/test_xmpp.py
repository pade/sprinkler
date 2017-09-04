# -*- coding: UTF-8 -*-

import unittest
import logging
import sys
import os
from threading import Thread

from xmppbot import SendMsgBot


# Set parent directory in path, to be able to import module
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import xmpp


class TestXMPP(unittest.TestCase):
    """docstring for TestXMPP"""

    def setUp(self):
        self._logger = logging.getLogger()

        self.code_to_test = {
            'server': ("server.jabber.hot-chilli.net", 80),
            'login': "sprinkler-tu@jabber.hot-chilli.net",
            'password': "!s20p21!"
        }

        self.tester = {
            'server': ("server.jabber.hot-chilli.net", 80),
            'login': "sprinkler-test@jabber.hot-chilli.net",
            'password': "!s20p21!"
        }

    def tearDown(self):
        pass

    def test_1(self):
        """ Test XMPP connexion """
        xmpp_con = xmpp.XMPPData(login=self.code_to_test['login'],
                            password=self.code_to_test['password'],
                            server=self.code_to_test['server'])

        msgbot = SendMsgBot(self.code_to_test['login'], self.tester)
        msgbot.send_message("Hello my friend :)!")

        msg = xmpp_con.get_message() # wait until message is received
        xmpp_con.disconnect()
        msgbot.disconnect()

        self.assertTrue(msg['body'] == "Hello my friend :)!")
