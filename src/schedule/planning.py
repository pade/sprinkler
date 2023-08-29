from typing import Tuple, List
from .stime import STime
from uuid import uuid4, UUID

class Days:
    """ Active days """

    def __init__(self) -> None:
        self.monday: bool = False
        self.tuesday: bool = False
        self.wednesday: bool = False
        self.thursday: bool = False
        self.friday: bool = False
        self.saturday: bool = False
        self.sunday: bool = False

    @staticmethod
    def fromValues(
        monday=False,
        tuesday=False,
        wednesday=False,
        thursday=False,
        friday=False,
        saturday=False,
        sunday=False
    ):
        days = Days()
        days.monday = monday
        days.tuesday = tuesday
        days.wednesday = wednesday
        days.thursday = thursday
        days.friday = friday
        days.saturday = saturday
        days.sunday = sunday
        return days
    
    @staticmethod
    def fromList(value: Tuple[bool, bool, bool, bool, bool, bool, bool]):
        days = Days()
        days.monday = value[0]
        days.tuesday = value[1]
        days.wednesday = value[2]
        days.thursday = value[3]
        days.friday = value[4]
        days.saturday = value[5]
        days.sunday = value[6]
        return days
    
    def __repr__(self) -> str:
        return f'M: {self.monday}, T: {self.tuesday}, W: {self.wednesday}, T: {self.thursday}, F: {self.friday}, S: {self.saturday}, S: {self.sunday}'
    

class SEvent:
    """ Event definition """
    def __init__(self, enable: bool, days: Days, channel: int, time: STime, name: str) -> None:
        self.name = name
        self.enable = enable
        self.days = days
        self.channel = channel
        self.time = time
        self.id = uuid4()

class Planning:
    """ Manage plannings """

    def __init__(self) -> None:
        """ Constructor """
        self._data: List[SEvent] = []
        self._index: int = 0

    def addEvent(self, event: SEvent) -> None:
        self._data.append(event)

    def removeEvent(self, id: UUID) -> None:
        event = self.findById(id)
        if event:
            self._data.remove(event)

    def findById(self, id: UUID) -> SEvent | None:
        for event in self._data:
            if id == event.id:
                return event
        return None
    
    def __iter__(self):
        self._index = 0
        return self
    
    def __next__(self):
      if self._index < len(self._data):
          item = self._data[self._index]
          self._index += 1
          return item
      else:
          raise StopIteration
        