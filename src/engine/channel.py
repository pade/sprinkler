from hw.gpio import BaseGpio

class Channel:
    def __init__(self, number: int, name: str, hwInterface: BaseGpio) -> None:
        """Constructor

        Args:
            number (int): Channel number
            name (str): Channel friendly name
            hwInterface (_type_): Corresponding HW interface
        """
        self._nb = number
        self._name = name
        self._hw = hwInterface
        
    @property
    def name(self) -> str:
        """ Get channel name """
        return self._name
    
    @name.setter
    def name(self, value: str):
        """ Set channel name """
        self._name = value

    def setOn(self) -> None:
        self._hw.write(self._nb, True)
        
    def setOff(self) -> None:
        self._hw.write(self._nb, False)
        
    def getState(self) -> bool:
        return self._hw.read(self._nb)
        
