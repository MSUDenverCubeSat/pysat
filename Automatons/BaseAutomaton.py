from threading import Timer
from abc import ABC, abstractmethod


class BaseAutomaton (ABC):
    interval_sec = 10
    __active__ = False

    def start(self):
        self.__active__ = True
        self._resetTimer()

    def stop(self):
        self.__active__ = False
        try:
            self.__timer__.cancel()
        except Exception as e:
            a = ""

    def _timerUp(self):
        try:
            self.execute()
        except Exception as e:
            print("Error: ", e)
        finally:
            self._resetTimer()

    def _resetTimer(self):
        if self.__active__:
            self.__timer__ = Timer(self.interval_sec, self._timerUp, ())
            self.__timer__.start()

    @abstractmethod
    def execute(self):
        pass
