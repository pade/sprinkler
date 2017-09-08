# -*- coding: UTF-8 -*-

'''
Created on 9 sept. 2016

@author: dassierp
'''


from update_channels import UpdateChannels
from engine import Engine
from xmpp import XMPPData
from database import Database

import sys
import os.path
import argparse
import logging
import configparser
import signal
import json
import cmdparser


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
    '''
    Main application
    '''

    def exit_safe(self, signal_nb, stack):
        '''
        Safe exit: stop all thread before exiting
        '''
        self.logger.info("Terminated by user (SIGINT)")
        self.stop_all()
        sys.exit()

    def stop_all(self):
        if self.engine is not None:
            self.engine.stop()
        if self.xmpp is not None:
            self.xmpp.disconnect()
        self.stop = True

    def __init__(self, confdir, *argv):
        '''
        Constructor
        @param confdir: Configuration directory path
        @param *argv: Command line argument
        '''

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
        self.engine = None
        self.xmpp = None
        self.stop = False

        # Logging configuration
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(filename)s [%(levelname)s] %(message)s')
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        parser = argparse.ArgumentParser(
            description="Automatic sprinkler management - V{}"
            .format(__VERSION__))
        parser.add_argument('-d', '--debug',
                            help='activate debug messages on output',
                            action="store_true")
        if(argv):
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
            self.config['xmpp'] = {
                'server': 'https://...',
                'port': '443',
                'login': '<put login here>',
                'password': '<put password here>'
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

    def run(self):
        '''
        Main program
        '''
        # Create channels from database
        try:
            upd = UpdateChannels(self._database)
            ch_list = upd.channels()
            self.engine = Engine(ch_list)
            self.xmpp = XMPPData(login=self.config['xmpp']['login'],
                                 password=self.config['xmpp']['password'],
                                 server=(self.config['xmpp']['server'],
                                         self.config['xmpp']['port']))
        except Exception:
            self.logger.info("FATAL ERROR", exc_info=True)
            self.stop_all()
            sys.exit(1)

        # Main loop
        while(not self.stop):
            if self.xmpp.is_message():
                msg = self.xmpp.get_message()
                try:
                    p = cmdparser.Parser(msg['body'])
                    self.logger.debug("Received command '{}'"
                                      .format(p.get_command()))
                    if p.get_command() == 'get program':
                        data = self._database.read()
                        msg.reply(json.dumps(data)).send()
                    elif p.get_command() == 'force channel':
                        nb = p.get_param()['nb']
                        action = p.get_param()['action']
                        self.logger.debug("Parameters: nb={}, action={}"
                                          .format(nb, action))
                        self.engine.channel_forced(nb, action)
                        msg.reply('{"status": "OK"}').send()
                    elif p.get_command() == 'new program':
                        program = p.get_param()['program']
                        self.logger.debug(
                            "Parameter: program={}".format(program))
                        self._database.write(program)
                        upd = UpdateChannels(self._database)
                        ch_list = upd.channels()
                        self.engine.stop()
                        self.engine = Engine(ch_list)
                        msg.reply('{"status": "OK"}').send()

                except:
                    self.logger.warning("Received unknown message: {}"
                                        .format(msg['body']))


if __name__ == '__main__':
    app = MainApp(CONFIG_DIRECTORY, sys.argv[1:])
    app.run()
