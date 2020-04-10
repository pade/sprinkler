# -*- coding: UTF-8 -*-

import sys
import os
import pytest
import json

# Set parent directory in path, to be able to import module
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import cmdparser


@pytest.fixture(params=['get program', 'force channel', 'new program', 'new channel', 'get channels state'])
def cmd_list(request):
    command = '{{"command": "{}"'.format(request.param)
    if request.param == "force channel":
        command = command + ', "nb": "1", "action": "ON" }'
    elif request.param == "new program" or request.param == "new channel":
        command = command + ', "program": {"channel": "0"}}'
    else:
        command = command + "}"
    return command


@pytest.fixture(params=["ON", "OFF", "AUTO"])
def action_list(request):
    command = '{{"command": "force channel", "nb": "3", "action": "{}"}}'.format(request.param)
    return command


def test_parser_get_program(cmd_list):
    p = cmdparser.Parser(cmd_list)
    json_msg = json.loads(cmd_list)
    assert(p.get_command() == json_msg['command'])


def test_force_channel(action_list):
    p = cmdparser.Parser(action_list)
    json_msg = json.loads(action_list)
    param = p.get_param()

    assert(param['nb'] == int(json_msg['nb']))
    assert(param['action'] == json_msg['action'])


def test_unknow_command():
    command = '{"command": "unknow"}'
    with pytest.raises(cmdparser.ParserError):
        p = cmdparser.Parser(command)


def test_unknow_action():
    command = '{"command": "force channel", "nb": "0", "action": "unknow"}'
    with pytest.raises(cmdparser.ParserError):
        p = cmdparser.Parser(command)
