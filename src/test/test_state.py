# -*- coding: UTF-8 -*-

import sys
import os
import pytest

# Set parent directory in path, to be able to import module
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import state

class Stubfct():

    def __init__(self):
        self.result = 0

    def fct1(self):
        self.result = 1

    def fct2(self):
        self.result = 2

    def fct3(self, param1, param2):
        self.result = param1
        self.result2 = param2

stubfct = Stubfct()

def test_UnknowState():
    """Test when trying to call an unknown state"""
    s = state.StateMachine()
    s.register("fct1", stubfct.fct1)
    s.register("fct2", stubfct.fct2)

    with pytest.raises(state.UnknownState):
        s.setState("dummy")

def test_NoRegister():
    """Test when no state is register """
    s = state.StateMachine()

    with pytest.raises(state.NoStateRegister):
        s.run()

def test_ChangeState():
    """Test change between two state """
    s = state.StateMachine()
    s.register("fct1", stubfct.fct1)
    s.register("fct2", stubfct.fct2)
    assert(stubfct.result == 0)

    s.setState("fct1")
    s.run()
    assert(stubfct.result == 1)

    s.setState("fct2")
    s.run()
    assert(stubfct.result == 2)

def test_WithParam():
    """Test function with arguments """
    s = state.StateMachine()
    s.register("fct1", stubfct.fct1)
    s.register("fct3", stubfct.fct3, [3, 4])

    s.setState("fct3")
    s.run()
    assert(stubfct.result == 3 and stubfct.result2 == 4)

