import logging
import sys


class SLogging(logging.getLoggerClass()):
    
    def __init__(self, name: str, level: str | int = 0) -> None:
        super().__init__(name, level)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s (line %(lineno)s) [%(levelname)s]: %(message)s'
        )
        streamhandler = logging.StreamHandler(sys.stdout)
        streamhandler.setFormatter(formatter)
        self.addHandler(streamhandler)
        
    def logCall(self, func):
        def wrapper(*args, **kwargs):
            self.debug(f'Calling: {func.__name__}({args}, {kwargs})')
            return func(*args, **kwargs)
        return wrapper
 