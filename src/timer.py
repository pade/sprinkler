import sched
import time
import threading


class Timer(threading.Thread):
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        """ To create a singleton class """
        if Timer._instance is None:
            with Timer._lock:
                if Timer._instance is None:
                    Timer._instance = super(Timer, cls).__new__(cls)
        return Timer._instance
        
    def __init__(self):
        self._sched= sched.scheduler(time.time, time.sleep)
        self._stoptimer = False
        super().__init__()

    def program(self, minutes, action, argument=(), kwargs={}):
        self._sched.enter(minutes*60, 1, action, argument, kwargs)

    def run(self):
        while(not self._stoptimer):
            self._sched.run()

    def clear(self):
        # remove all pending timer
        for event in self._sched.queue:
            self._sched.cancel(event)

    def stop(self):
        self._stoptimer = True
        for event in self._sched.queue:
            self._sched.cancel(event)

    

    