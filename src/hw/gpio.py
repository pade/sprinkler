import logging


class BaseGpio(object):
    '''
    GPIO interface class
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self._log = logging.getLogger('sprinkler')

    def write(self, channel: int, value: bool) -> None:
        # pchannel from 0 to 3
        raise NotImplementedError

    def read(self, channel: int) -> bool:
        # pchannel from 0 to 3
        raise NotImplementedError


