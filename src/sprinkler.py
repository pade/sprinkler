# -*- coding: UTF-8 -*-

'''
Created on 9 sept. 2016

@author: dassierp
'''

from update_channels import UpdateChannels
from engine import Engine
from messages import Messages
from database import Database

import sys
import os
import os.path
import argparse
import logging
import logging.handlers
import configparser
import signal
import json
import cmdparser
from uuid import uuid4
import threading
import time
import waitevents

__VERSION__ = "1.0.0"

CONFIG_DIRECTORY = os.path.join(os.path.expanduser("~"), ".sprinkler")
CHANNEL_NB = 4

DEFAULT_DATABASE = """
{
    "channels": [
        {
            "nb": 0,
            "name": "Channel 0",
            "is_enable": false,
            "progdays": [
                {
                    "is_active": false,
                    "days": [false, false, false,
                             false, false, false, false],
                    "stime":
                    {
                        "hour": 0,
                        "minute": 0,
                        "duration": 0
                    }
                },
                {
                    "is_active": false,
                    "days": [false, false, false,
                             false, false, false, false],
                    "stime":
                    {
                        "hour": 0,
                        "minute": 0,
                        "duration": 0
                    }
                }
            ]
        },
        {
            "nb": 1,
            "name": "Channel 1",
            "is_enable": false,
            "progdays": [
                {
                    "is_active": false,
                    "days": [false, false, false,
                             false, false, false, false],
                    "stime":
                    {
                        "hour": 0,
                        "minute": 0,
                        "duration": 0
                    }
                },
                {
                    "is_active": false,
                    "days": [false, false, false,
                             false, false, false, false],
                    "stime":
                    {
                        "hour": 0,
                        "minute": 0,
                        "duration": 0
                    }
                }
            ]
        },
        {
            "nb": 2,
            "name": "Channel 2",
            "is_enable": false,
            "progdays": [
                {
                    "is_active": false,
                    "days": [false, false, false,
                             false, false, false, false],
                    "stime":
                    {
                        "hour": 0,
                        "minute": 0,
                        "duration": 0
                    }
                },
                {
                    "is_active": false,
                    "days": [false, false, false,
                             false, false, false, false],
                    "stime":
                    {
                        "hour": 0,
                        "minute": 0,
                        "duration": 0
                    }
                }
            ]
        },
        {
            "nb": 3,
            "name": "Channel 3",
            "is_enable": false,
            "progdays": [
                {
                    "is_active": false,
                    "days": [false, false, false,
                             false, false, false, false],
                    "stime":
                    {
                        "hour": 0,
                        "minute": 0,
                        "duration": 0
                    }
                },
                {
                    "is_active": false,
                    "days": [false, false, false,
                             false, false, false, false],
                    "stime":
                    {
                        "hour": 0,
                        "minute": 0,
                        "duration": 0
                    }
                }
            ]
        }
    ]
}
"""


class MainApp(object):
    """ Main application """
    def exit_safe(self, signal_nb, stack):
        """ Safe exit: stop all thread before exiting """
        if signal_nb == 15:
            sig = "SIGTERM"
        elif signal_nb == 2:
            sig = "SIGINT"
        else:
            sig = "OTHER SIGNAL"
        self.logger.info(f"Terminated by user ({sig})")
        self.stop_all()

    def stop_all(self):
        self.stop_event.set()

    def __init__(self, confdir, *argv):
        """
        Constructor
        :param confdir: Configuration directory path
        :param argv: Command line argument
        """
        # Create configuration directory if it does not exists
        if not os.path.isdir(confdir):
            try:
                os.mkdir(confdir)
            except Exception:
                print(
                    "Impossible to create configuration directory %s" % confdir
                )
                sys.exit(1)

        self._configfile = os.path.join(confdir, "sprinkler.conf")
        self._database = Database(os.path.join(confdir, "channel.db"))
        logfile = os.path.join(confdir, "sprinkler.log")
        self.engine = None
        self.messages = None
        self.stop_event = waitevents.WaitableEvent()

        # Logging configuration
        self.logger = logging.getLogger('sprinkler')
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(filename)s [%(levelname)s] %(message)s')
        streamhandler = logging.StreamHandler(sys.stdout)
        streamhandler.setFormatter(formatter)
        self.logger.addHandler(streamhandler)

        parser = argparse.ArgumentParser(
            description=f"Automatic sprinkler management - V{__VERSION__}")
        parser.add_argument('-d', '--debug',
                            help='activate debug messages on output',
                            action="store_true")
        if argv:
            args = parser.parse_args(*argv)
        else:
            args = parser.parse_args([])

        if args.debug:
            self.logger.setLevel(logging.DEBUG)
            self.logger.debug("Debug mode activated")

        signal.signal(signal.SIGINT, self.exit_safe)
        # signal.signal(signal.SIGQUIT, self.exit_safe)
        signal.signal(signal.SIGTERM, self.exit_safe)
        # Create default configuration file if it does not exists
        self.config = configparser.ConfigParser()
        try:
            self.config.read_file(open(self._configfile))
        except Exception:
            # File does not exist: must create one with default parameters
            self.logger.info(
                "Create default configuration file %s" % self._configfile)
            self.config['meteo'] = {
                'url':
                    'http://www.meteofrance.com/mf3-rpc-portlet/rest/pluie/870500'}
            self.config['messages'] = {
                'pubnub_subkey': 'sub-...',
                'pubnub_pubkey': 'pub-...',
                'id': str(uuid4()),
            }
            with open(self._configfile, 'w') as configfile:
                self.config.write(configfile)

        # Create channel data base if not exists
        if not self._database.file_exists():
            try:
                with open(self._database.dbfile, 'w') as f:
                    f.write(DEFAULT_DATABASE)
            except Exception:
                self.logger.info("FATAL ERROR", exc_info=True)
                sys.exit(1)

        # Create log file
        fdh = logging.handlers.RotatingFileHandler(logfile,
                                                   maxBytes=10000000,
                                                   backupCount=5)
        fdh.setFormatter(formatter)
        self.logger.addHandler(fdh)

        # Create channels from database
        try:
            upd = UpdateChannels(self._database)
            ch_list = upd.channels()
            self.engine = Engine(ch_list)
            self.messages = Messages(subkey=self.config['messages']['pubnub_subkey'],
                                     pubkey=self.config['messages']['pubnub_pubkey'],
                                     id=self.config['messages']['id'])

            self.th_msg = threading.Thread(target=self.send_channel_state)
            self.th_msg.start()

        except Exception:
            self.logger.info("FATAL ERROR", exc_info=True)
            self.stop_all()
            sys.exit(1)

    def send_channel_state(self):
        engine_event = self.engine.get_event_new_state()
        multievent = waitevents.MultiEventWait()
        multievent.register(engine_event, "New channel status")
        multievent.register(self.stop_event, "Stop")
        keep_running = True
        while keep_running:
            ev = multievent.select()
            if ev.data == "Stop":
                keep_running = False
            else:
                self.messages.send(json.dumps({"channelstate": self.engine.get_channel_state()}))
                ev.fileobj.clear()
        self.logger.debug("Stop send message thread")

    def run(self):
        th = threading.Thread(target=self._run)
        th.start()
        # Block until program finish
        th.join()
        print("Terminated")

    def _run(self):
        """ Main program """
        new_msg_event = waitevents.MultiEventWait()
        new_msg_event.register(self.messages.get_event_message(), "New message")
        new_msg_event.register(self.stop_event, "Stop")
        keep_running = True
        # Main loop
        while (keep_running):
            # Blocking call until a new message is present or stop event
            ev = new_msg_event.select()
            if ev.data == "New message":
                ev.fileobj.clear()
                msg = self.messages.get_message()
                try:
                    p = cmdparser.Parser(msg)
                    if p.get_command() == 'get program':
                        data = self._database.read()
                        self.messages.send(json.dumps(data))
                    elif p.get_command() == 'force channel':
                        nb = p.get_param()['nb']
                        action = p.get_param()['action']
                        duration = p.get_param()['duration']
                        self.engine.channel_forced(nb, action, duration)
                        self.messages.send('{"status": "OK"}')
                    elif p.get_command() == 'new program' or p.get_command() == 'new channel':
                        program = p.get_param()['program']
                        if p.get_command() == 'new program':
                            self._database.write(program)
                        else:
                            self._database.update_channels(program)
                        upd = UpdateChannels(self._database)
                        ch_list = upd.channels()
                        self.engine.stop()
                        self.engine = Engine(ch_list)
                        self.messages.send('{"status": "OK"}')
                    elif p.get_command() == 'get channels state':
                        self.messages.send(json.dumps({"channelstate": self.engine.get_channel_state()}))

                except BaseException:
                    self.logger.warning(f"Received unknown message: {msg}", exc_info=True)
            else:
                keep_running = False
        self.logger.debug("Stop main program")
        if self.engine is not None:
            self.engine.stop()
        if self.messages is not None:
            self.messages.stop()
        self.logger.debug("Main program is stopped")


if __name__ == '__main__':
    app = MainApp(CONFIG_DIRECTORY, sys.argv[1:])
    app.run()

