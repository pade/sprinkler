# -*- coding: UTF-8 -*-

'''
Created on 9 sept. 2016

@author: dassierp
'''

import sys
import os.path
import argparse
import logging
from multiprocessing import process
from config import Config, FileNotExist, LoadError, SaveError
from config import DAYLIST
from stime import STime

DEFAULT_CFG_FILE = os.path.join(os.path.expanduser("~"), ".sprinkler")
CHANNEL_NB = 4


def update_config(pCfg):
    '''
    Update configuration
    @param pCfg: Config object to update
    '''
    pass 


if __name__ == '__main__':

    # Logging configuration
    logger = logging.getLogger("sprinkler")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s [%(levelname)s] %(message)s')
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    parser = argparse.ArgumentParser(description="Automatic sprinkler management")
    parser.add_argument('-c', '--config', default=DEFAULT_CFG_FILE, dest="config",
                        help="Name of the file to store configuration")
    parser.add_argument('-d', '--debug', help='activate debug messages on output',
                        action="store_true")
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)

    logger.info("Using configuration file %s" % args.config)

    # Create configuration
    cfg = Config(CHANNEL_NB, args.config)
    try:
        cfg.load()
    except FileNotExist:
        # New configuration
        for i in range(CHANNEL_NB):
            for day in DAYLIST:
                t = STime()
                cfg.addCfg(i, day, t)
        try:
            cfg.save()
        except SaveError as e:
            logger.error("Impossible to save file %s, <%s>: %s" % (args.config, e.type, e.value))
            sys.exit(1)
    except LoadError as e:
        logger.error("Impossible to load file %s, <%s>: %s" % (args.config, e.type, e.value))
        sys.exit(1)
        
        
    
