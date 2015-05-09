import pygame


from pie.asset import get_largest_frame
from pie.entity import MIdentity, MRect, MAnimated


class Animated(pygame.sprite.Sprite, MIdentity, MRect, MAnimated):
    def __init__(self, frames, sprite_groups=[], autostart=True, **surface_rect_kwa):
        pygame.sprite.Sprite.__init__(self, *sprite_groups)
        MIdentity.__init__(self)
        # TODO: get_largest_frame may not be needed if we enforce animations to have a constant frame size.
        MRect.__init__(self,
                         get_largest_frame(frames).get_rect(**surface_rect_kwa))

        MAnimated.__init__(self, count=len(frames), autostart=autostart)

        self.__frames = tuple(frames) # Not mutable for now.

    @property
    def surface(self):
        return self.__frames[self.index]