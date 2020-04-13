import sched
import time
import threading


class Timer(threading.Thread):
       
    def __init__(self):
        self._sched= sched.scheduler(time.time, time.sleep)
        self._stoptimer = False
        super().__init__()

    def program(self, minutes, action, argument=(), kwargs={}):
        self._sched.enter(minutes*60, 1, action, argument, kwargs)

    def run(self):
        while(not self._stoptimer):
            self._sched.run(blocking=False)
            time.sleep(5)

    def clear(self):
        # remove all pending timer
        for event in self._sched.queue:
            self._sched.cancel(event)

    def stop(self):
        for event in self._sched.queue:
            self._sched.cancel(event)
        self._stoptimer = True

    

    