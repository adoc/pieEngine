import pygame

from pie.entity import ESprite, MIdentity, MRect


class Point(ESprite):
    def __init__(self, pos, radius=0):
        MIdentity.__init__(self)
        MRect.__init__(self, pos, (0, 0))
        self.__radius = 0

    @property
    def radius(self):
        return self.__radius


class Fill(ESprite):
    """A static solid color surface.
    """
    def __init__(self, *surface_args, surface_factory=None,
                 fill_color=pygame.Color(0, 0, 0), sprite_groups=[], **rect_kwa):
        ESprite.__init__(self, *surface_args,
                                     surface_factory=surface_factory,
                                     sprite_groups=sprite_groups, **rect_kwa)
        self.__fill_color = fill_color
        self.fill()

    def resize(self, screen):
        pass

    def fill(self, fill_color=None):
        self.__fill_color = fill_color or self.__fill_color
        self.surface.fill(self.__fill_color)