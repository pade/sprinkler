from configparser import ConfigParser
from .singleton import Singleton
from .slogging import SLogging

logger = SLogging(__name__)

class Config(Singleton, ConfigParser):
    """ Configuration management class """
    
    def __init__(self, configFilename: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.configFilename = configFilename
        try:
            self.read_file(open(configFilename))
            logger.info(f'Configuration read from "{configFilename}"')
        except FileNotFoundError:
            logger.info(f'Config file "{configFilename}" not found, create it with default values')
            self['DEFAULT'] = {
                'debug': 'false'
            }
            with open(configFilename, 'w') as configfile:
                self.write(configfile)
            
    