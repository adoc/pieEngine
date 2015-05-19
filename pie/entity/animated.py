"""
"""

from pie.asset import get_largest_frame
from pie.entity.base import *
from pie.animation import AnimationLoop


# TODO: Good start but doesn't handle some irregular but useful arg combos.
# Where does this go????
class SequenceAnimation:
    def __init__(self, **kwa):
        """Mixin for animated Entity classes. The ``frame_index``
        property can be used

        :param int count:
        :param float interval:
        :param int start:
        :param int end:
        :param bool autostart:
        :param func animation_factory:
        :return:
        """

        self.__start = self.__index = kwa.pop('start', 0)
        self.__interval = kwa.pop('interval', 1.0)
        self.__count = count = kwa.pop('count', 0)
        end = kwa.pop('end', 0)
        self.__end = end > 0 and end or (count - 1)
        self.__animation_obj = kwa.pop('animation_factory',
                                       lambda: AnimationLoop())()

        if kwa.pop('autostart', True):
            self.__animation_obj.start()

    #Value props
    @property
    def start(self):
        return self.__start

    @property
    def end(self):
        return self.__end

    @property
    def count(self):
        return self.__count

    @property
    def playing_count(self):
        return abs((self.end - self.start + 1) / self.interval)

    @property
    def interval(self):
        return self.__interval

    @property
    def index(self):
        return self.__index

    #Transport props
    @property
    def at_start(self):
        return self.index <= self.start

    @property
    def at_end(self):
        return self.index >= self.end

    @property
    def is_reversed(self):
        return self.interval < 0

    @property
    def is_forward(self):
        return self.interval > 0

    # Transport methods
    def advance(self):
        self.__index += self.interval
        self.__index %= self.count

    def flip_interval(self):
        self.__interval = -self.interval

    def reverse(self):
        self.__interval = -abs(self.interval)

    def forward(self):
        self.__interval = abs(self.interval)

    def rewind(self):
        self.__index = self.__start

    def fast_forward(self):
        self.__index = self.__end

    # Loop Method
    def update(self):
        self.__animation_obj.update(self)


class SurfaceSequence(SpriteRect):
    def __init__(self, frames, autostart=True, **kwa):
        SpriteRect.__init__(self, get_largest_frame(frames), **kwa)

        self.__seq = SequenceAnimation(count=len(frames), autostart=autostart)
        self.__frames = tuple(frames) # Not mutable for now.

    @property
    def image(self):
        return self.__frames[int(self.__seq.index)]

    def update(self):
        self.__seq.update()


class SurfaceSelection(SpriteRect):
    def __init__(self, frames, autostart=True, **kwa):
        SpriteRect.__init__(self, get_largest_frame(frames), **kwa)

        self.__frames = tuple(frames) # Not mutable for now.
        self.__count = len(self.__frames)
        self.__index = 0

    @property
    def image(self):
        try:
            return self.__frames[self.__index]
        except IndexError:
            print("Missing frame: %s" % self.__index )

    def set_frame(self, index):
        index = int(index)
        index %= self.__count
        self.__index = index