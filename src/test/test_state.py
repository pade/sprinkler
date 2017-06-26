# -*- coding: UTF-8 -*-

import unittest
import sys
import os

# Set parent directory in path, to be able to import module
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import state


class TestState(unittest.TestCase):

    def setUp(self):
        class Stubfct():

            def __init__(self):
                self.result = 0

            def fct1(self):
                self.result = 1

            def fct2(self):
                self.result = 2

            def fct3(self, param1):
                self.result = param1


        self.fct = Stubfct()

    def test_UnknowState(self):
        """ Test when trying to call an unknown state"""
        s = state.StateMachine()
        s.register("fct1", self.fct.fct1)
        s.register("fct2", self.fct.fct2)

        self.assertRaises(state.UnknownState, s.setState, "dummy")

    def test_NoRegister(self):
        """ Test when no state is register """
        s = state.StateMachine()

        self.assertRaises(state.NoStateRegister, s.run)

    def test_ChangeState(self):
        """ Test change between two state """
        s = state.StateMachine()
        s.register("fct1", self.fct.fct1)
        s.register("fct2", self.fct.fct2)
        self.assertTrue(self.fct.result == 0)

        s.setState("fct1")
        s.run()
        self.assertTrue(self.fct.result == 1)

        s.setState("fct2")
        s.run()
        self.assertTrue(self.fct.result == 2)

    def test_WithParam(self):
        """ Test function with arguments """
        s = state.StateMachine()
        s.register("fct1", self.fct.fct1)
        s.register("fct3", self.fct.fct3, "3")

        s.setState("fct3")
        s.run()
        self.assertTrue(self.fct.result == "3")


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestState))
    return suite


if __name__ == "__main__":

    suite = suite()
    unittest.TextTestRunner(verbosity=2).run(suite)
