# -*- coding: UTF-8 -*-


from channel import Channel
from scheduler import Scheduler
import datetime
import logging


class Engine(object):
    """Core of the application"""

    def __init__(self, channels):
        '''
        @param ch: a list of Channel object
        '''
        super(Engine, self).__init__()
        self._channels = channels
        self._sched = Scheduler(self.run)
        self._logger = logging.getLogger()

    def get_datetime_now(self):
        return datetime.datetime.now()
        pass

    def run(self):
        for ch in self._channels:
            self._run_channel(ch)

    def _run_channel(self, channel):
        if channel.isenable:
            channel_status = []
            for prog in channel.progs:
                if prog.isactive:
                    day = self.get_datetime_now().weekday()
                    if prog.get_one_day(day):
                        # Programme is active for today
                        now = self.get_datetime_now()
                        start = prog.stime.startDate(now)
                        end = prog.stime.endDate(now)

                        self._logger.debug("Start date: {}"
                                           .format(start.isoformat()))
                        self._logger.debug("End date: {}"
                                           .format(end.isoformat()))
                        self._logger.debug("Now: {}"
                                           .format(now.isoformat()))

                        channel_status.append(start <= now and end > now)

            if True in channel_status:
                channel.running = True
            else:
                channel.running = False
