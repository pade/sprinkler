'''
Created on 12 sept. 2016

@author: dassierp
'''

import sys
import os
import unittest

# Set parent directory in path, to be able to import module
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import meteo


class TestMeteo(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_meteo(self):
        m = meteo.Meteo(url="http://www.meteofrance.com/mf3-rpc-portlet/rest/pluie/870500")


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestMeteo))

    return suite

if __name__ == "__main__":
    suite = suite()
    unittest.TextTestRunner(verbosity=2).run(suite)
