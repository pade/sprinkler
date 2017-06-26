# -*- coding: UTF-8 -*-


class StateMachineError(Exception):
    pass


class UnknownState(StateMachineError):

    def __init__(self, name):
        Exception.__init__(self, "State '{}' is not register".format(name))


class NoStateRegister(StateMachineError):

    def __init__(self):
        Exception.__init__(self, "No state are register")


class StateMachine():
    """dSimple state machine class"""

    def __init__(self):
        self._list = {}
        self._current = None

    def register(self, name, callback, args=[], kwargs={}):
        """ Register a new state
        @param name: state name (string)
        @param callback: function to call when state is active
        @param args: argume pass to the function
        @param kwargs: argument to pass to the function
        """

        self._list[name] = [callback, args, kwargs]

    def run(self):
        """ Run current state
        @param name: name of state to activate
        """
        if self._current is not None:
            self._list[self._current][0](*self._list[self._current][1],
                                         **self._list[self._current][2])
        else:
            raise NoStateRegister()

    def setState(self, name):
        """ Set current state
        @param n,ame: name of state to set
        """

        if name in self._list:
            self._current = name
        else:
            raise UnknownState(name)
