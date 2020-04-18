from .gpio import BaseGpio

class DummyGpio(BaseGpio):

    def __init__(self, pConfig=None):
        super(DummyGpio, self).__init__(pConfig)
        self.__channel = {}

    def write(self, pchannel, pvalue):
        self.__channel[pchannel] = pvalue
        self._log.debug(f"WRITE {pvalue} on channel {pchannel}")

    def read(self, pchannel):
        try:
            return self.__channel[pchannel]
        except KeyError:
            self._log.error(f"Channel {pchannel} not found")