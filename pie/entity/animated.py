import pygame

from pie.animation import AnimationLoop
from pie.asset import get_largest_frame
from pie.entity import MIdentity, MRect


__author__ = 'coda'


class Animated(pygame.sprite.Sprite, MIdentity, MRect):
    def __init__(self, frames, sprite_groups=[], autostart=True,
                 animation_cls=AnimationLoop, **surface_rect_kwa):
        pygame.sprite.Sprite.__init__(self, *sprite_groups)
        MIdentity.__init__(self)
        # TODO: get_largest_frame may not be needed if we enforce animations to have a constant frame size.
        MRect.reset(self,
                         get_largest_frame(frames).get_rect(**surface_rect_kwa))

        self.__frames = tuple(frames) # Not mutable for now.
        self.__frame_index = 0
        self.__frame_interval = 1
        self.__frame_count = len(frames)
        self.__animation_obj = animation_cls(self)

        self.autostart = autostart

        if autostart:
            self.__animation_obj.start()

    #Transport props
    @property
    def at_start(self):
        return self.__frame_index == 0

    @property
    def at_end(self):
        return self.__frame_index == self.__frame_count - 1

    @property
    def is_reversed(self):
        return self.__frame_interval < 0

    @property
    def surface(self):
        return self.__frames[self.__frame_index]

    # Transport methods
    def advance(self):
        self.__frame_index += self.__frame_interval
        self.__frame_index %= self.__frame_count

    def negate_interval(self):
        self.__frame_interval = -self.__frame_interval

    def rewind(self):
        self.__frame_index = 0

    # Loop Method
    def update(self):
        self.__animation_obj.update()

    def present(self):
        return (self.surface, self.rect)



