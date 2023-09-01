#type: ignore
import unittest
from colour_runner import runner

import test_planning
import test_stime
import test_config

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTest(loader.loadTestsFromModule(test_planning))
suite.addTest(loader.loadTestsFromModule(test_stime))
suite.addTest(loader.loadTestsFromModule(test_config))

runner = runner.ColourTextTestRunner(verbosity=2)
runner.run(suite)
