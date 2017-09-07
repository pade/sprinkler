# -*- coding: UTF-8 -*-

import sys
import os
from threading import Thread

# Set parent directory in path, to be able to import module
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import xmpp

code_to_test = {
    'server': ("server.jabber.hot-chilli.net", 80),
    'login': "sprinkler-tu@jabber.hot-chilli.net",
    'password': "!s20p21!"
}

tester = {
    'server': ("server.jabber.hot-chilli.net", 80),
    'login': "sprinkler-test@jabber.hot-chilli.net",
    'password': "!s20p21!"
}

xmpp_info = tester
xmpp_recipient = code_to_test['login']

def test_connexion(xmppbot):
    """ Test XMPP connexion """
    xmpp_con = xmpp.XMPPData(login=code_to_test['login'],
                        password=code_to_test['password'],
                        server=code_to_test['server'])

    xmppbot.send_message("Hello my friend :)!")

    msg = xmpp_con.get_message() # wait until message is received
    xmpp_con.disconnect()

    assert msg['body'] == "Hello my friend :)!"


