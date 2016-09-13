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
from threading import Event

from config import Config, FileNotExist, LoadError, SaveError
from config import DAYLIST
from stime import STime
from scheduler import Scheduler

DEFAULT_CFG_DIR = os.path.join(os.path.expanduser("~"), ".sprinkler")
DATABASE_FILE = os.path.join(DEFAULT_CFG_DIR, "program.db")
CONFIG_FILE = os.path.join(DEFAULT_CFG_DIR, "config")
CHANNEL_NB = 4


# ceate an event to stop all thread at the end
stop_event = Event()

# Launch a schedule every minutes to check configuration change
sched = Scheduler(stop_event)


def update_config(pCfg):
    '''
    Update configuration
    @param pCfg: Config object to update
    '''
    pass


def exit_safe():
    '''
    Safe exit: stop all thread before exiting
    '''
    stop_event.set()
    while sched.is_alive():
        pass
    sys.exit()

if __name__ == '__main__':

    signal.signal(signal.SIGINT, exit_safe)
    # Logging configuration
    logger = logging.getLogger("sprinkler")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s [%(levelname)s] %(message)s')
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    parser = argparse.ArgumentParser(description="Automatic sprinkler management")
    parser.add_argument('-d', '--debug', help='activate debug messages on output',
                        action="store_true")
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)

    # Create configuration directory if it does not exists
    if not os.path.isdir(DEFAULT_CFG_DIR):
        os.mkdir(DEFAULT_CFG_DIR)

    # Create default configuration file if it does not exists
    config = configparser.ConfigParser()
    try:
        config.read_file(open(CONFIG_FILE))
    except:
        # File does not exist: must create one with default parameters
        logger.info("Create default configuration file %s" % CONFIG_FILE)
        config['meteo'] = {'url': 'http://www.meteofrance.com/mf3-rpc-portlet/rest/pluie/870500'}
        with open(CONFIG_FILE, 'w') as configfile:
            config.write(configfile)

    # Create program
    prog = Config(CHANNEL_NB, DATABASE_FILE)
    try:
        prog.load()
    except FileNotExist:
        # New configuration
        for i in range(CHANNEL_NB):
            for day in DAYLIST:
                t = STime()
                prog.addCfg(i, day, t)
        try:
            prog.save()
        except SaveError as e:
            logger.error("Impossible to save file %s, <%s>: %s" % (DATABASE_FILE, e.type, e.value))
            sys.exit(1)
    except LoadError as e:
        logger.error("Impossible to load file %s, <%s>: %s" % (DATABASE_FILE, e.type, e.value))
        sys.exit(1)

    minutes_event = sched.get_event()

    while True:
        # core engine
        minutes_event.wait()
        minutes_event.clear()
