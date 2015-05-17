"""Classes for timing an Engine.
"""

import pygame

__all__ = ('Clock', 'RateClock')


class Clock:
    """:class:`Clock` used to time :class:`pie.engine.Engine` instances.
    """

    def __init__(self, accurate=False):
        """
        :param bool accurate: Use `pygame.time.Clock <http://www.pygame.org/docs/ref/time.html#pygame.time.Clock>`_
            slower but more "accurate" CPU based delay vs. SDL Delay.
        """
        self.__clock = pygame.time.Clock()
        if accurate:
            self.tick = self.__tick_busy_loop

    def __tick(self, framerate):
        #:
        return self.__clock.tick(framerate)

    def __tick_busy_loop(self, framerate):
        #:
        return self.__clock.tick_busy_loop(framerate)

    def tick(self, framerate):
        """Delay the engine in order to maintain a target *framerate*.

        :param int framerate: Frame rate to target with this tick.
        :rtype: float
        :return: Milliseconds since last :func:`tick` call.
        """
        return self.__tick(framerate)

    @property
    def time(self):
        """Returns the time between the previous :func:`tick` calls.

        :rtype: float
        :return: Milliseconds
        """
        return self.__clock.get_time()

    @property
    def rawtime(self):
        """Return the time between the previous :func:`tick` calls, not
        including any added delay to maintain *framerate*.

        :rtype: float
        :return: Milliseconds
        """
        return self.__clock.get_rawtime()

    @property
    def framerate(self):
        """Calculate the actual *framerate*. Based on the average of
        the last ten calls to :func:`tick`

        :rtype: float
        :return: Milliseconds
        """
        return self.__clock.get_fps()


class RateClock(Clock):
    """:class:`Clock` object that will target a given *framerate* on
    instantiation.

    :param int framerate: Target frame rate (FPS)
    :param bool accurate: Use CPU-based "accurate" clock.
    """

    def __init__(self, framerate, accurate=False):
        Clock.__init__(self, accurate)
        self.__framerate = framerate

    def tick(self):
        """Delay the :class:`pie.engine.Engine` instance in order to
        maintain a target *framerate*.

        :rtype: float
        :return: Milliseconds since last :func:`tick`.
        """
        return Clock.tick(self, self.__framerate)


