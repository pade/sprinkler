# -*- coding: UTF-8 -*-

import pytest
import sys
import os
from jsonschema import ValidationError

# Set parent directory in path, to be able to import module
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import jsonvalidate

curpath = os.path.dirname(os.path.abspath(__file__))

def test_ok():
    """Test a well formed JSON file"""
    jsv = jsonvalidate.Validate()
    jsv.validate_file(os.path.join(curpath, "json_ok.js"))

def test_ko_1():
    """Test a malformed JSON file"""
    jsv = jsonvalidate.Validate()
    with pytest.raises(ValidationError) as excinfo:
        jsv.validate_file(os.path.join(curpath, "json_ko_1.js"))
    excinfo.match('24 is greater')
