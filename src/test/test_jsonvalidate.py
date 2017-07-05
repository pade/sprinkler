# -*- coding: UTF-8 -*-

import unittest
import pytest
import sys
import os
from jsonschema import ValidationError

# Set parent directory in path, to be able to import module
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import jsonvalidate


class TestJsonValidate(unittest.TestCase):

    def setUp(self):
        self._curpath = os.path.dirname(os.path.abspath(__file__))

    def tearDown(self):
        pass

    def test_ok(self):
        """Test a well formed JSON file"""
        jsv = jsonvalidate.Validate()
        jsv.validate_file(os.path.join(self._curpath, "json_ok.js"))
        assert True

    def test_ko_1(self):
        """Test a malformed JSON file"""
        jsv = jsonvalidate.Validate()
        with pytest.raises(ValidationError) as excinfo:
            jsv.validate_file(os.path.join(self._curpath, "json_ko_1.js"))
        excinfo.match('24 is greater')
