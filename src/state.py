# -*- coding: UTF-8 -*-


class StateMachineError(Exception):
    pass


class UnknownState(StateMachineError):
    def __init__(self, name):
        Exception.__init__(self, "State '{}' is not register".format(name))


class StateMachine():
    """docstring for StateMachine"""
    def __init__(self):
        self._list = {}

    def register(self, name, callback):
        """ Register a new state
        @param name: state name (string)
        @param callback: function to call when state is active
        """
        self._list[name] = callback

    def state(self, name):
        """ Activate state
        @param name: name of state to activate
        """
        if name in self._list:
            self._list[name]
        else:
            raise UnknownState(name)
