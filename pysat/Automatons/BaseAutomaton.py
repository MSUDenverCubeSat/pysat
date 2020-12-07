from threading import Timer
from abc import ABC, abstractmethod


class BaseAutomaton (ABC):
    """Classes inheriting from this should do a task repeatedly every so often"""
    _interval_sec = 10
    __active__ = False

    def start(self):
        self.__active__ = True
        self._reset_timer()

    def stop(self):
        self.__active__ = False
        try:
            self.__timer__.cancel()
        except Exception:
            pass

    def _timer_up(self):
        try:
            self.execute()
        except Exception as e:
            print("Error: ", e)
        finally:
            self._reset_timer()

    def _reset_timer(self):
        if self.__active__:
            self.__timer__ = Timer(self._interval_sec, self._timer_up)
            self.__timer__.start()

    @abstractmethod
    def execute(self):
        pass
