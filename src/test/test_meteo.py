# -*- coding: UTF-8 -*-

import sys
import os
import asyncio
import json
from dotenv import load_dotenv

load_dotenv()

# Set parent directory in path, to be able to import module
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import meteo

SPRINKLER_CONF = f"""
[meteo]
apikey: {os.environ['APIKEY']}
citykey: 134979
"""

CHANNEL_DB = """
{
    "channels": [
        {
            "nb": 0,
            "name": "Jardin",
            "is_enable": true,
            "progdays": [
                {
                    "is_active": true,
                    "days": [false, false, false,
                             false, true, false, false],
                    "stime":
                    {
                        "hour": 5,
                        "minute": 0,
                        "duration": 45
                    }
                },
                {
                    "is_active": false,
                    "days": [false, false, false,
                             false, false, false, false],
                    "stime":
                    {
                        "hour": 0,
                        "minute": 0,
                        "duration": 0
                    }
                }
            ]
        },
        {
            "nb": 1,
            "name": "Channel 1",
            "is_enable": false,
            "progdays": [
                {
                    "is_active": false,
                    "days": [false, false, false,
                             false, false, false, false],
                    "stime":
                    {
                        "hour": 0,
                        "minute": 0,
                        "duration": 0
                    }
                },
                {
                    "is_active": false,
                    "days": [false, false, false,
                             false, false, false, false],
                    "stime":
                    {
                        "hour": 0,
                        "minute": 0,
                        "duration": 0
                    }
                }
            ]
        },
        {
            "nb": 2,
            "name": "Channel 2",
            "is_enable": false,
            "progdays": [
                {
                    "is_active": false,
                    "days": [false, false, false,
                             false, false, false, false],
                    "stime":
                    {
                        "hour": 0,
                        "minute": 0,
                        "duration": 0
                    }
                },
                {
                    "is_active": false,
                    "days": [false, false, false,
                             false, false, false, false],
                    "stime":
                    {
                        "hour": 0,
                        "minute": 0,
                        "duration": 0
                    }
                }
            ]
        },
        {
            "nb": 3,
            "name": "Channel 3",
            "is_enable": false,
            "progdays": [
                {
                    "is_active": false,
                    "days": [false, false, false,
                             false, false, false, false],
                    "stime":
                    {
                        "hour": 0,
                        "minute": 0,
                        "duration": 0
                    }
                },
                {
                    "is_active": false,
                    "days": [false, false, false,
                             false, false, false, false],
                    "stime":
                    {
                        "hour": 0,
                        "minute": 0,
                        "duration": 0
                    }
                }
            ]
        }
    ]
}
"""

def test_meteo_conf_ok(confdir, setenv):
    m = meteo.Meteo(os.path.join(confdir, "sprinkler.conf"))
    assert m.apikey == os.environ["APIKEY"]
    assert m.citykey == "134979"
    assert m.is_meteo


def test_meteo_update_conf(confdir):
    m1 = meteo.Meteo(os.path.join(confdir, "sprinkler.conf"))
    m1.set_city("123456")
    m2 = meteo.Meteo(os.path.join(confdir, "sprinkler.conf"))
    assert m1.citykey == "123456"
    assert m2.citykey == "123456"


async def _test_get_meteo(tmpdir):
    def callback(msg):
        assert not msg['error'], json.dumps(msg['message'])

    m = meteo.Meteo(os.path.join(tmpdir, "sprinkler.conf"))
    m.get_meteo(callback)
    await asyncio.sleep(3)
    m.get_meteo(callback)
    await asyncio.sleep(3)


def test_get_meteo(confdir):
    asyncio.run(_test_get_meteo(confdir))
