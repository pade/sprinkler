# -*- coding: UTF-8 -*-

from stime import STime
import logging


class Progdays():
    """docstring for Progdays"""

    def __init__(self):
        self._isactive = False
        self.stime = STime()
        # table of days: first is monday, last is sunday
        self._days = [False, False, False, False, False, False, False]
        self._logger = logging.getLogger('sprinkler')

    def _set_isactive(self, activate):
        self._isactive = activate

    def _get_isactivate(self):
        return self._isactive

    def set_one_day(self, day, isactive):
        '''
        Activate only one day
        @param day: day number to activate (0: monday)
        @param isactive: boolean
        '''
        if day < 0 or day > 6:
            self._logger.debug("Invalid 'day' parameter (day: {})".format(day))
        else:
            self._days[day] = isactive

    def get_one_day(self, day):
        '''
        Return if a day is active
        @param day: day number (0: monday)
        '''
        return self._days[day]

    def set_days(self, days):
        '''
        Set all activity for all days, from monday to sunday
        @param days: a table of 7 booleans (0 is for monday)
        '''
        self._days = days

    def get_days(self):
        return self._days

    def get_stime(self):
        return self.stime

    isactive = property(_get_isactivate, _set_isactive, None, None)
