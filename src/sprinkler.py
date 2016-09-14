# -*- coding: UTF-8 -*-

'''
Created on 9 sept. 2016

@author: dassierp
'''

import sys
import os.path
import argparse
import logging
import configparser
import signal
import datetime
from threading import Event

from config import Config, FileNotExist, LoadError, SaveError
from config import DAYLIST
from stime import STime
from scheduler import Scheduler

CONFIG_DIRECTORY = os.path.join(os.path.expanduser("~"), ".sprinkler")
CHANNEL_NB = 4


class MainApp(object):
    '''
    Main application
    '''

    def exit_safe(self):
        '''
        Safe exit: stop all thread before exiting
        '''
        self.logger.info("Terminated by user (SIGINT)")
        self.stop_event.set()
        while self.sched.is_alive():
            pass
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
            except:
                print ("Impossible to create configuration directory %s" % confdir)
                sys.exit(1)

        self._configfile = os.path.join(confdir, "sprinkler.conf")
        self._databse = os.path.join(confdir, "program.db")

        # Logging configuration
        self.logger = logging.getLogger("sprinkler")
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s [%(levelname)s] %(message)s')
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        parser = argparse.ArgumentParser(description="Automatic sprinkler management")
        parser.add_argument('-d', '--debug', help='activate debug messages on output',
                            action="store_true")
        args = parser.parse_args()
        if args.debug:
            self.logger.setLevel(logging.DEBUG)

        self.stop_event = Event()
        self.sched = Scheduler(self.stop_event)

        signal.signal(signal.SIGINT | signal.CTRL_C_EVENT, self.exit_safe)

        # Create default configuration file if it does not exists
        self.config = configparser.ConfigParser()
        try:
            self.config.read_file(open(self._configfile))
        except:
            # File does not exist: must create one with default parameters
            self.logger.info("Create default configuration file %s" % self._configfile)
            self.config['meteo'] = {'url': 'http://www.meteofrance.com/mf3-rpc-portlet/rest/pluie/870500'}
            with open(self._configfile, 'w') as configfile:
                self.config.write(configfile)

        # Create program
        self.prog = Config(CHANNEL_NB, self._databse)
        try:
            self.prog.load()
        except FileNotExist:
            # New configuration
            for i in range(CHANNEL_NB):
                for day in DAYLIST:
                    t = STime()
                    self.prog.addCfg(i, day, t)
            try:
                self.prog.save()
            except SaveError as e:
                self.logger.error("Impossible to save file %s, <%s>: %s" % (self._databse, e.type, e.value))
                sys.exit(1)
        except LoadError as e:
            self.logger.error("Impossible to load file %s, <%s>: %s" % (self._databse, e.type, e.value))
            sys.exit(1)

    def update_config(self):
        '''
        Update configuration
        @param pCfg: Config object to update
        '''
        pass

    def run(self):
        '''
        Run application
        '''
        while True:
            self.sched.get_event().wait()
            print ("[%s] - Event is set..." % datetime.datetime.now())
            self.sched.get_event().clear()


if __name__ == '__main__':
    app = MainApp(CONFIG_DIRECTORY)
    app.run()
