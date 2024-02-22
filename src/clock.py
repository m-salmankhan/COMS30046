# SINGLETON CLOCK
from time import sleep


class Clock:
    __clock = None

    def __new__(cls, *args, **kwargs):
        if cls.__clock is None:
            cls.__clock = super(Clock, cls).__new__(cls)

        return cls.__clock

    def __init__(self, speed: int = 0):
        if not hasattr(self, "_initialised"):
            self.__time = 0
            self._initialised = True
            self.__speed = speed

    def tick(self):
        sleep(self.__speed/4)
        self.__time += 1

    def get_time(self):
        return self.__time
