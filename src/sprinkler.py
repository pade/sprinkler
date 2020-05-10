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
import asyncio
import functools

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


async def exit_safe(signal_nb: int, cur_task: asyncio.Task) -> None:
    """ Safe exit: stop all tasks before exiting """
    logger = logging.getLogger("sprinkler")
    if signal_nb == 15:
        sig = "SIGTERM"
    elif signal_nb == 2:
        sig = "SIGINT"
    elif signal_nb == 255:
        sig = "KEYBOARD INTERRUPT"
    else:
        sig = "OTHER SIGNAL"
    logger.info(f"Terminated by signal ({sig})")
    cur_task.cancel()


class MainApp(object):
    """ Main application """
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
        # Set 'confdir' to env. variable to let it accessible to

        self._configfile = os.path.join(confdir, "sprinkler.conf")
        self._database = Database(os.path.join(confdir, "channel.db"))
        logfile = os.path.join(confdir, "sprinkler.log")
        self.engine = None
        self.messages = None

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
            self.debug = True
            self.logger.setLevel(logging.DEBUG)
            self.logger.debug("Debug mode activated")
        else:
            self.debug = False

        # Create default configuration file if it does not exists
        self.config = configparser.ConfigParser()
        try:
            self.config.read_file(open(self._configfile))
        except Exception:
            # File does not exist: must create one with default parameters
            self.logger.info(
                "Create default configuration file %s" % self._configfile)
            self.config['meteo'] = {
                'apikey': 'dummy-api-key',
                'citykey': '134979'}
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

    async def send_channel_state(self, event):
        keep_running = True
        while keep_running:
            await event.wait()
            await self.messages.send({"channelstate": self.engine.get_channel_state()})
            event.clear()

    def run(self):
        try:
            asyncio.run(self._run(), debug=self.debug)
        except KeyboardInterrupt:
            # Stop program (on Windows)
            pass
        finally:
            self.logger.info("Successfully shutdown program")

    async def _run(self):
        """ Main program """
        # Create channels from database
        try:
            loop = asyncio.get_event_loop()
            signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
            for s in signals:
                cur_task = asyncio.current_task()
                loop.add_signal_handler(s, lambda s=s: asyncio.create_task(exit_safe(s, cur_task)))
        except NotImplementedError:
            # Signal are not implemented on this platform (i.e.: windows), so do'nt use it
            pass
        try:
            upd = UpdateChannels(self._database)
            ch_list = upd.channels()
            self.engine = Engine(ch_list)
            task_msg = asyncio.create_task(self.send_channel_state(self.engine.get_event_new_state()))
            self.messages = Messages(subkey=self.config['messages']['pubnub_subkey'],
                                     pubkey=self.config['messages']['pubnub_pubkey'],
                                     id=self.config['messages']['id'])
        except Exception:
            self.logger.info("FATAL ERROR", exc_info=True)
            sys.exit(1)

        keep_running = True
        # Main loop
        while (keep_running):
            try:
                # Blocking call until a new message is present or stop event
                msg = await self.messages.get_message()
                try:
                    p = cmdparser.Parser(msg)
                    if p.get_command() == 'get program':
                        data = self._database.read()
                        await self.messages.send(data)
                    elif p.get_command() == 'force channel':
                        nb = p.get_param()['nb']
                        action = p.get_param()['action']
                        duration = p.get_param()['duration']
                        self.engine.channel_forced(nb, action, duration)
                        await self.messages.send({"status": "OK"})
                    elif p.get_command() == 'new program' or p.get_command() == 'new channel':
                        program = p.get_param()['program']
                        if p.get_command() == 'new program':
                            self._database.write(program)
                        else:
                            self._database.update_channels(program)
                        upd = UpdateChannels(self._database)
                        ch_list = upd.channels()
                        self.engine.stop()
                        task_msg.cancel()
                        self.engine = Engine(ch_list)
                        task_msg = asyncio.create_task(self.send_channel_state(self.engine.get_event_new_state()))
                        await self.messages.send({"status": "OK"})
                    elif p.get_command() == 'get channels state':
                        await self.messages.send({"channelstate": self.engine.get_channel_state()})

                except BaseException:
                    self.logger.warning(f"Received unknown message: {json.loads(msg)}", exc_info=True)
            except asyncio.CancelledError:
                keep_running = False
        task_msg.cancel()
        if self.engine is not None:
            self.engine.stop()
        if self.messages is not None:
            self.messages.stop()
        self.logger.info("Sprinkler program is stopped")


if __name__ == '__main__':
    app = MainApp(CONFIG_DIRECTORY, sys.argv[1:])
    app.run()

