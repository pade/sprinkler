# -*- coding: UTF-8 -*-


#from channel import Channel
from scheduler import Scheduler
from state import StateMachine
import datetime
import logging


class Engine(object):
    """Core of the application"""

    def __init__(self, channels):
        '''
        @param channels: a list of Channel object
        '''
        super(Engine, self).__init__()
        self._channels = channels
        self._statemachine = {}
        self.__savestartdate = {}
        self.__saveenddate = {}
        for ch in self._channels:
            self._statemachine[ch.nb] = StateMachine()
            self._statemachine[ch.nb].register(
                "NotRunning", self._not_running, [ch])
            self._statemachine[ch.nb].register(
                "Running", self._running, [ch])
            self._statemachine[ch.nb].setState("NotRunning")

        self._sched = Scheduler(self.run)
        self._logger = logging.getLogger()

    def get_datetime_now(self):
        return datetime.datetime.now()

    def run(self):
        for ch in self._channels:
            self._statemachine[ch.nb].run()

    def _running(self, channel):
        """ Whenn channel is running """
        channel_status = []
        if channel.isenable:
            for prog in channel.progs:
                if prog.isactive:
                    day = self.get_datetime_now().weekday()
                    if prog.get_one_day(day):
                        # Programme is active for today
                        now = self.get_datetime_now()

                        self._logger.debug("{}: Start date: {}"
                                           .format(channel.name,
                                                   self.__savestartdate[
                                                       channel.nb].isoformat()
                                                   )
                                           )
                        self._logger.debug("{} End date: {}"
                                           .format(channel.name,
                                                   self.__saveenddate[
                                                       channel.nb].isoformat()
                                                   )
                                           )
                        self._logger.debug("Now: {}"
                                           .format(now.isoformat()))

                        channel_status.append(
                            self.__savestartdate[channel.nb] <= now and
                            self.__saveenddate[channel.nb] > now)

        if True in channel_status:
            channel.running = True
        else:
            self._statemachine[channel.nb].setState("NotRunning")
            channel.running = False

    def _not_running(self, channel):
        """ When channel is not running """
        channel_status = []
        if channel.isenable:
            for prog in channel.progs:
                if prog.isactive:
                    day = self.get_datetime_now().weekday()
                    if prog.get_one_day(day):
                        # Programme is active for today
                        now = self.get_datetime_now()
                        start = prog.stime.startDate(now)
                        end = prog.stime.endDate(now)

                        self._logger.debug("{} Start date: {}"
                                           .format(
                                               channel.name,
                                               start.isoformat()))
                        self._logger.debug("{} End date: {}"
                                           .format(
                                               channel.name,
                                               end.isoformat()))
                        self._logger.debug("Now: {}"
                                           .format(now.isoformat()))

                        channel_status.append(start <= now and end > now)

        if True in channel_status:
            self._statemachine[channel.nb].setState("Running")
            # save start and end date to prevent false detection around
            # midnight
            self.__savestartdate[channel.nb] = start
            self.__saveenddate[channel.nb] = end
            channel.running = True
        else:
            channel.running = False

    def stop(self):
        """ Stop running engine
        """
        self._sched.stop()
        while self._sched.is_alive():
            pass
