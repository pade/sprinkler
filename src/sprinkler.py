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
from multiprocessing import Queue
from multiprocessing import Pool
from multiprocessing import Lock

from program import Program, FileNotExist, LoadError, SaveError
from program import DAYLIST
from stime import STime
from scheduler import Scheduler
from checkprogram import CheckProgram, ServerData

CONFIG_DIRECTORY = os.path.join(os.path.expanduser("~"), ".sprinkler")
CHANNEL_NB = 4

DAYNAME = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')


class MainApp(object):
    '''
    Main application
    '''

    def exit_safe(self, signal_nb, stack):
        '''
        Safe exit: stop all thread before exiting
        '''
        self.logger.info("Terminated by user (SIGINT)")
        #self.stop_event.set()
        #while self.sched.is_alive():
        #    pass
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

        #self.stop_event = Event()
        #self.sched = Scheduler(self.stop_event)

        signal.signal(signal.SIGINT, self.exit_safe)
        #signal.signal(signal.SIGQUIT, self.exit_safe)
        signal.signal(signal.SIGTERM, self.exit_safe)

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
        self.prog = Program(CHANNEL_NB, self._databse)
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

        # Create a lock to prevent concurrent access to program
        self._prog_lock = Lock()

    def update_config(self):
        '''
        Update configuration
        @param pCfg: Program object to update
        '''
        pass

    def _run(self, channel):
        '''
        Algorithm to manage a channel
        @param channel: Channel number to manage
        '''
        # Get configuration
        with self._prog_lock:
            channel_prog = self.prog.getCfg(channel)
        now = datetime.datetime.now()
        matching_progs = channel_prog.findCfg(DAYNAME[now.weekday()], now)
        if matching_progs is not None:
            # Normally only one matching program is possible, so keep only first one
            startdate = matching_progs[0].startDate(now)
            enddate = matching_progs[0].endDate(now)

    def run(self):
        '''
        Run application
        '''
        # Launch a Scheduler per channel
#         sched_prog = []
#         for i in range(CHANNEL_NB):
#             sched_prog.append(Scheduler(self._run, i))

        # Create pool of process: one per channel
        #processes = Pool(CHANNEL_NB)
        #processes.map(self._run, range(CHANNEL_NB))

        server = CheckProgram()

        while True:
            if server.is_new_prog():
                newprogs = server.get_newprog()
                with self._prog.lock:
                    for newprog in newprogs:
                        
                    

if __name__ == '__main__':
    app = MainApp(CONFIG_DIRECTORY)
    app.run()
