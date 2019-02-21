# -*- coding: UTF-8 -*-

import json

command_list = ("get program", "force channel", "new program")
action_list = ("ON", "OFF", "AUTO")


class Parser(object):
    """ Parse XMPP message """

    def __init__(self, msg):
        self.message = msg
        self.command = None
        self.param = {}
        self._parse()

    def _parse(self):
        """ Parse incoming message """
        try:
            json_msg = json.loads(self.message)
            self.command = json_msg['command']
            if self.command not in command_list:
                raise ParserError("Unknown command '{}'"
                                  .format(self.command))
            elif self.command == "force channel":
                nb = int(json_msg['nb'])
                action = json_msg['action']
                if action not in action_list:
                    raise ParserError("Unknown action '{}'"
                                      .format(action))
                self.param = {'nb': nb, 'action': action}
            elif self.command == "new program":
                program = json_msg['program']
                self.param = {'program': program}
        except BaseException:
            raise ParserError(self.message)

    def get_command(self):
        return self.command

    def get_param(self):
        return self.param


class ParserError(Exception):

    def __init__(self, msg):
        super().__init__(self, "Unknown message '{}'".format(msg))