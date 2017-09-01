# -*- coding: UTF-8 -*-

import unittest
import logging
import sys
import os
from threading import Thread
from sleekxmpp import ClientXMPP


# Set parent directory in path, to be able to import module
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import xmpp


class SendMsgBot(ClientXMPP):

    def __init__(self, recipient, msg, xmpp_info):
        super(SendMsgBot, self).__init__(xmpp_info['login'],
                                         xmpp_info['password'])

        self.recipient = recipient
        self.msg = msg
        self._server = xmpp_info['server']

        self.add_event_handler('session_start', self.start)

        self.connect()
        self.process(block=True)

    def start(self, event):
        self.send_presence()
        self.get_roster()
        self.send_message(mto=self.recipient, mbody=self.msg)
        self.disconnect(wait=True)

    def connect(self):
        super(SendMsgBot, self).connect(self._server)


class TestXMPP(unittest.TestCase):
    """docstring for TestXMPP"""

    def setUp(self):
        self._logger = logging.getLogger()

        self.client = {
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
        con = xmpp.XMPPData(login=self.client['login'],
                            password=self.client['password'],
                            server=self.client['server'])

        q = con.get_queue()

        xmpp_th = Thread(target=con.connect)
        xmpp_th.start()

        xmpp_tester = SendMsgBot(self.client['login'],
                                 "Hello my friend :)!", self.tester)

        msg = q.get()
        con.close_connexion()

        self.assertTrue(msg['body'] == "Hello my friend :)!")
