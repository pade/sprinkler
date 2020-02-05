# -*- coding: UTF-8 -*-

from threading import Thread
from queue import Queue, Empty
import os
import sys
import tempfile
import pytest
import logging

@pytest.fixture
def confdir(request):
    """ Fixture to create the configuration directory used
    by sprinkler application """
    default_conf = getattr(request.module, "SPRINKLER_CONF")
    default_db = getattr(request.module, "CHANNEL_DB")

    with tempfile.TemporaryDirectory() as tmpdir:
        sprinkler_conf = os.path.join(tmpdir, "sprinkler.conf")
        channel_db = os.path.join(tmpdir, "channel.db")

        with open(sprinkler_conf, "w") as fd:
            fd.write(default_conf)
        with open(channel_db, "w") as fd:
            fd.write(default_db)
        yield tmpdir


@pytest.fixture
def tmpfile():
    """ Define a names temporary file """
    import tempfile
    with tempfile.NamedTemporaryFile() as tmpf:
        yield tmpf
