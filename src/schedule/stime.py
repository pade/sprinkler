from datetime import datetime
from datetime import timedelta


class STime(object):
    '''
    Spinkler time
    :param hours: Starting hour from 0 to 23. Outside this range, set to range limit
    :param minutes: Starting minute from 0 to 59. Outside this range,
        set to range limit
    :param duration: duration of sprinkler, in minutes
    '''

    def __init__(self, hours: int, minutes: int, duration: int) -> None:
        '''
        Constructor
        '''
        self.duration = duration
        self.hours = hours
        self.minutes = minutes

    @property
    def hours(self) -> int:
        return self._hours
    
    @hours.setter
    def hours(self, hours: int) -> None:
        if hours < 0:
            self._hours = 0
        elif hours > 23:
            self._hours = 23
        else:
            self._hours = hours

    @property
    def minutes(self) -> int:
        return self._minutes
    
    @minutes.setter
    def minutes(self, minutes: int) -> None:
        if minutes < 0:
            self._minutes = 0
        elif minutes > 59:
            self._minutes = 59
        else:
            self._minutes = minutes

    @property
    def duration(self) -> int:
        return self._duration
    
    @duration.setter
    def duration(self, duration: int) -> None:
        if duration < 0:
            self._duration = 0
        else:
            self._duration = duration

    def __str__(self):
        return "%02d:%02d [%d]" % (self.hours, self.minutes, self.duration)

    # def intoMinutes(self):
    #     '''
    #     Return the time into minutes
    #     '''
    #     return self.hours * 60 + self.minute

    # def __add__(self, pNbMinutes):
    #     '''
    #     Add STime object with a duration in minutes
    #     @param pNbMinutes: duration in minutes
    #     @return: a STimet instance class
    #     '''

    #     (nbhour, minute) = ((self.minute + pNbMinutes) // 60,
    #                         (self.minute + pNbMinutes) % 60)
    #     hour = (self.hours + nbhour) % 24
    #     return STime(hour=hour, minute=minute)

    # def setTime(self, hours, minutes):
    #     '''
    #     Set STime object with the string in argument
    #     @param hour: hour to set
    #     @param minute: minute to set
    #     Nota: duration is unchanged
    #     '''

    #     self.hours, self.minute = hours, minutes

    # def startDate(self, pDateTime):
    #     '''
    #     Convert STime to datetime object
    #     with day, month and year of pDateTime object
    #     @param pDateTime: Original datetime object to take into account
    #     '''
    #     return datetime(pDateTime.year, pDateTime.month, pDateTime.day,
    #                     self.hours, self.minute)

    # def endDate(self, pDateTime):
    #     '''
    #     Convert STime to datetime object adding with duration
    #     with day, month and year of pDateTime object
    #     @param pDateTime: Original datetime object to take into account
    #     '''
    #     return self.startDate(pDateTime) + timedelta(minutes=self.duration)

    # def setDuration(self, duration):
    #     '''
    #     Set duration (in minutes)
    #     '''
    #     self.duration = duration

    # @classmethod
    # def now(cls):
    #     '''
    #     @return return a STime object with current time
    #     '''
    #     t = datetime.now()
    #     return cls(hour=t.hour, minute=t.minute)
