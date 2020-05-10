# -*- coding: UTF-8 -*-


from scheduler import Scheduler
from state import StateMachine
import datetime
import logging
import timer
import asyncio


class Engine:
    """Core of the application"""

    def __init__(self, channels):
        """
        :param channels: a list of Channel object
        """

        self._channels = channels
        self._statemachine = {}
        self.__savestartdate = {}
        self.__saveenddate = {}
        self._currentstate = {}
        self._timer = {}
        for ch in self._channels:
            self._statemachine[ch.nb] = StateMachine()
            self._statemachine[ch.nb].register("NotRunning", self._not_running, [ch])
            self._statemachine[ch.nb].register("Running", self._running, [ch])
            self._statemachine[ch.nb].register("ManualOn", self._manual_on, [ch])
            self._statemachine[ch.nb].register("ManualOff", self._manual_off, [ch])
            self._statemachine[ch.nb].setState("NotRunning")
            self._currentstate[ch.nb] = {'nb': ch.nb, 'state': "NotRunning"}
            self._timer[ch.nb] = timer.Timer()

        self._oldstate = self._currentstate.copy()
        self._sched = Scheduler(self.run)
        self._logger = logging.getLogger('sprinkler')
        self._event_new_state = asyncio.Event()

    def get_event_new_state(self):
        return self._event_new_state

    def get_datetime_now(self):
        return datetime.datetime.now()

    def run(self):
        self._logger.debug("Running engine...")
        for ch in self._channels:
            self._statemachine[ch.nb].run()

    def _manual_on(self, channel):
        """ Force running """
        channel.running = True
        if channel.manual == "OFF":
            self._logger.info(f"Channel {channel.name} ({channel.nb}) forced OFF")
            self._statemachine[channel.nb].setState("ManualOff")
            self._save_channel_state(channel.nb, "ManualOff")
            self._statemachine[channel.nb].run()
        elif channel.manual == "AUTO":
            self._logger.info(f"Channel {channel.name} ({channel.nb}) set in program mode")
            self._statemachine[channel.nb].setState("NotRunning")
            self._save_channel_state(channel.nb, "NotRunning")
            self._statemachine[channel.nb].run()

    def _manual_off(self, channel):
        """ Force stop """
        channel.running = False
        if channel.manual == "ON":
            self._logger.info(f"Channel '{channel.name}' ({channel.nb}) forced ON")
            self._statemachine[channel.nb].setState("ManualOn")
            self._statemachine[channel.nb].run()
        elif channel.manual == "AUTO":
            self._logger.info(f"Channel '{channel.name}' ({channel.nb}) set in program mode")
            self._statemachine[channel.nb].setState("NotRunning")
            self._save_channel_state(channel.nb, "NotRunning")
            self._statemachine[channel.nb].run()

    def _running(self, channel):
        """ When channel is running """
        if channel.manual == "OFF":
            self._logger.info(f"Channel '{channel.name}' ({channel.nb}) forced OFF")
            self._statemachine[channel.nb].setState("ManualOff")
            self._save_channel_state(channel.nb, "ManualOff")
            self._statemachine[channel.nb].run()
        elif channel.manual == "ON":
            self._logger.info(f"Channel '{channel.name}' ({channel.nb}) forced ON")
            self._statemachine[channel.nb].setState("ManualOn")
            self._statemachine[channel.nb].run()
        else:
            channel_status = []
            if channel.isenable:
                for prog in channel.progs:
                    if prog.isactive:
                        day = self.get_datetime_now().weekday()
                        if prog.get_one_day(day):
                            # Programme is active for today
                            now = self.get_datetime_now()

                            self._logger.debug(f"{channel.name}: Start date: {self.__savestartdate[channel.nb].isoformat()}")
                            self._logger.debug(f"{channel.name} End date: {self.__saveenddate[channel.nb].isoformat()}")
                            self._logger.debug(f"Now: {now.isoformat()}")

                            channel_status.append(self.__savestartdate[channel.nb] <= now and self.__saveenddate[channel.nb] > now)

            if True in channel_status:
                channel.running = True
                self._save_channel_state(channel.nb, "Running")
            else:
                self._logger.info(f"Channel '{channel.name}' ({channel.nb}) is now OFF")
                self._statemachine[channel.nb].setState("NotRunning")
                self._save_channel_state(channel.nb, "NotRunning")
                self._statemachine[channel.nb].run()
                channel.running = False

    def _not_running(self, channel):
        """ When channel is not running """
        if channel.manual == "OFF":
            self._logger.info(f"Channel {channel.name} ({channel.nb}) forced OFF")
            self._statemachine[channel.nb].setState("ManualOff")
            self._save_channel_state(channel.nb, "ManualOff")
            self._statemachine[channel.nb].run()
        elif channel.manual == "ON":
            self._logger.info(f"Channel {channel.name} ({channel.nb}) forced ON")
            self._statemachine[channel.nb].setState("ManualOn")
            self._statemachine[channel.nb].run()
        else:
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

                            self._logger.debug(f"{channel.name} Start date: {start.isoformat()}")
                            self._logger.debug(f"{channel.name} End date: {end.isoformat()}")
                            self._logger.debug(f"Now: {now.isoformat()}")

                            channel_status.append(start <= now and end > now)

            if True in channel_status:
                self._logger.info(f"Channel '{channel.name}' ({channel.nb}) is now ON ")
                self._statemachine[channel.nb].setState("Running")
                self._save_channel_state(channel.nb, "Running")
                # save start and end date to prevent false detection around
                # midnight
                self.__savestartdate[channel.nb] = start
                self.__saveenddate[channel.nb] = end
                channel.running = True
                self._statemachine[channel.nb].run()
            else:
                channel.running = False
                self._save_channel_state(channel.nb, "NotRunning")

    def _save_channel_state(self, channel_nb, state, duration=0):
        # replace current value
        if state == "ManualOn":
            self._currentstate[channel_nb] = {'nb': channel_nb, 'state': state, 'duration': duration}
        else:
            self._currentstate[channel_nb] = {'nb': channel_nb, 'state': state}
        # Notify if there is some change
        if self._currentstate[channel_nb] != self._oldstate[channel_nb]:
            self._event_new_state.set()
            self._oldstate[channel_nb] = self._currentstate[channel_nb]

    def channel_forced(self, nb, action, duration=0):
        """ Set channel action
        :param nb: channel number
        :param action: channel action. "ON", "OFF", "AUTO"
        :param duration: when action is ON, the duration in minutes of the sprinkler"""
        for ch in self._channels:
            if nb == ch.nb:
                if action in ("OFF", "AUTO"):
                    self._logger.info(f"Channel {ch.name} ({ch.nb}) forced to {action}")
                    if action == "OFF":
                        self._save_channel_state(nb, "ManualOff")
                    else:
                        self._save_channel_state(nb, "NotRunning")
                    self._timer[ch.nb].cancel()
                    ch.manual = action
                elif action == "ON" and duration != 0:
                    self._logger.info(f"Channel {ch.name} ({ch.nb}) forced to ON for {duration} minutes")
                    self._save_channel_state(nb, "ManualOn", duration)
                    # Remove all already forced sprinkler
                    self._timer[ch.nb].cancel()
                    self._timer[ch.nb] = timer.Timer(duration*60, self._stop_ch_after_delay, args=(ch.nb,))
                    ch.manual = "ON"
                self.run()

    async def _stop_ch_after_delay(self, nb):
        """ Callback called to switch channel ch to AUTO after a delay """
        self._logger.info(f"Channel n°{nb}: end of forced ON")
        for ch in self._channels:
            if nb == ch.nb:
                ch.manual = "AUTO"
                self.run()

    def get_channel_state(self):
        return [x for x in self._currentstate.values()]

    def stop(self):
        for nb in self._timer:
            self._timer[nb].cancel()
        self._sched.cancel()

