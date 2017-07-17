# -*- coding: UTF-8 -*-

'''
Created on 9 sept. 2016

@author: dassierp
'''


from update_channels import UpdateChannels
from engine import Engine
import sys
import os.path
import argparse
import logging
import configparser
import signal


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
        if self.engine is not None:
            self.engine.stop()
        sys.exit()

    def __init__(self, confdir):
        '''
        Constructor
        @param confdir: Configuration directory path
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
        self._database = os.path.join(confdir, "channel.db")
        self.engine = None

        # Logging configuration
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s [%(levelname)s] %(message)s')
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        parser = argparse.ArgumentParser(
            description="Automatic sprinkler management")
        parser.add_argument('-d', '--debug',
                            help='activate debug messages on output',
                            action="store_true")
        args = parser.parse_args()
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
                'login': '<put login here>',
                'password': '<put password here>'
            }
            with open(self._configfile, 'w') as configfile:
                self.config.write(configfile)

        # Create channel data base if not exists
        if not os.path.isfile(self._database):
            try:
                with open(self._database, 'w') as f:
                    f.write(DEFAULT_DATABASE)
            except Exception:
                self.logger.info("FATAL ERROR", exc_info=True)
                sys.exit(1)

    def update_config(self):
        '''
        Update configuration
        '''
        pass

    def run(self):
        '''
        Main program
        '''
        # Create channels from database
        try:
            db = open(self._database, 'r')
            upd = UpdateChannels(db)
            ch_list = upd.channels()
            self.engine = Engine(ch_list)
        except Exception:
            self.logger.info("FATAL ERROR", exc_info=True)
            sys.exit(1)


if __name__ == '__main__':
    app = MainApp(CONFIG_DIRECTORY)
    app.run()
