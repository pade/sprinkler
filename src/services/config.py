from configparser import ConfigParser
from pathlib import Path
from .slogging import Logging
import os

logger = Logging(__name__)

DEFAULT_CONFIG = """
[main]
debug = false
hw_conf = {hwConf}
db_file = {dbFile}
"""

defaultConfigDir = Path.home() / Path('.config/sprinkler')
configFile = Path('sprinkler.ini')

def readConfig() -> ConfigParser:
    if not os.environ.get('SPRINKLER_CONFIG_DIR', None):
        logger.info('Environment variable "SPRINKLER_CONFIG_DIR" not set, use default location inside')
        configDir = defaultConfigDir
    else:
        configDir = Path(os.environ.get('SPRINKLER_CONFIG_DIR', ''))
    parser = ConfigParser()
    configFilePath = configDir / configFile
    if configFilePath.exists():
        parser.read(configFilePath.as_posix())
        logger.info(f'Configuration read from "{configFilePath.as_posix()}"')
    else:
        logger.info(f'Config file "{configFilePath.as_posix()}" not found, create it with default values')
        hwConf = configDir / Path('hw.conf')
        dbFile = configDir / Path('database.db')
        parser.read_string(DEFAULT_CONFIG.format(hwConf=hwConf.as_posix(), dbFile=dbFile.as_posix()))
        
        configFilePath.parent.mkdir(parents=True, exist_ok=True)
        with open(configFilePath.as_posix(), 'w') as fd:
            parser.write(fd)
    return parser
            
config = readConfig()
