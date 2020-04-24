# -*- coding: UTF-8 -*-

import json
import logging

command_list = ("get program", "force channel", "new program", "new channel", "get channels state")
action_list = ("ON", "OFF", "AUTO")


class Parser(object):
    """ Parse received message """

    def __init__(self, msg):
        self.message = msg
        self.command = None
        self.param = {}
        self.log = logging.getLogger('sprinkler')

        self._parse()

    def _parse(self):
        """ Parse incoming message """
        try:
            self.command = self.message['command']
            if self.command not in command_list:
                raise ParserError(f"Unknown command '{self.command}'")
            elif self.command == "force channel":
                nb = int(self.message['nb'])
                action = self.message['action']
                duration = int(self.message.get('duration', 0))
                if action not in action_list:
                    raise ParserError(f"Unknown action '{json.loads(action)}'")
                self.param = {'nb': nb, 'action': action, 'duration': duration}
                self.log.info(f"Received command '{self.command}' [nb={self.param['nb']}, action={self.param['action']}, duration={self.param['duration']}]")
            elif self.command == "new program" or self.command == "new channel":
                program = self.message['program']
                self.param = {'program': program}
                self.log.info(f"Received command '{self.command}' [program={self.param['program']}]")
            else:
                self.log.info(f"Received command '{self.command}'")
        except BaseException:
            raise ParserError(self.message)

    def get_command(self):
        return self.command

    def get_param(self):
        return self.param


class ParserError(Exception):

    def __init__(self, msg):
        super().__init__(self, f"Unknown message '{json.dumps(msg)}'")
