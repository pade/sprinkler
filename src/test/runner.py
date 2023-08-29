import unittest
from colour_runner import runner

import test_planning
import test_stime

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTest(loader.loadTestsFromModule(test_planning))
suite.addTest(loader.loadTestsFromModule(test_stime))

runner = runner.ColourTextTestRunner(verbosity=2)
runner.run(suite)
