# -*- coding: UTF-8 -*-

import sys
import os
from subprocess import call

# Set parent directory in path, to be able to import module
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import xmpp

code_to_test = {
    'server': ("server.jabber.hot-chilli.net", 443),
    'login': "sprinkler-tu@jabber.hot-chilli.net",
    'password': "!s20p21!"
}

tester = {
    'server': ("server.jabber.hot-chilli.net", 443),
    'login': "sprinkler-test@jabber.hot-chilli.net",
    'password': "!s20p21!"
}

xmpp_info = tester
xmpp_recipient = code_to_test['login']


def test_connexion():
    """ Test XMPP connexion """
    xmpp_con = xmpp.XMPPData(login=code_to_test['login'],
                             password=code_to_test['password'],
                             server=code_to_test['server'])

    # purge message pipe
    while xmpp_con.is_message():
        xmpp_con.get_message()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    xmpp_file_path = os.path.join(current_dir, "xmpp-send.py")
    call(["python3", xmpp_file_path, '-d', '-j', tester['login'], '-p', tester['password'],
          '-t', code_to_test['login'], '-m', 'Hello my friend :)!'])

    msg = xmpp_con.get_message(10)  # wait until message is received
    xmpp_con.stop()

    assert msg['body'] == "Hello my friend :)!"
