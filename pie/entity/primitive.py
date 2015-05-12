import pygame

from pie.entity import MIdentity, MRect, MSurface, MSurfaceRect, MSprite


class Point(MIdentity, MRect, MSprite):
    def __init__(self, pos, radius=0, **kwa):
        MIdentity.__init__(self)
        MRect.__init__(self, pos, (0, 0))
        if radius > 5 and not 'collide_func' in kwa:
            kwa['collide_func'] = pygame.sprite.collide_circle
        MSprite.__init__(self, **kwa)
        self.__radius = radius

    @property
    def radius(self):
        return self.__radius


class Fill(MIdentity, MSurfaceRect, MSprite):
    """A static solid color surface.
    """
    def __init__(self, *surface_args, surface_factory=None,
                 fill_color=pygame.Color(0, 0, 0), sprite_groups=[], **rect_kwa):
        MIdentity.__init__(self)
        MSurfaceRect.__init__(self, *surface_args, surface_factory=surface_factory)
        MSprite.__init__(self, sprite_groups=sprite_groups)

        self.__fill_color = fill_color
        self.fill()

    def resize(self, screen):
        pass

    def fill(self, fill_color=None):
        self.__fill_color = fill_color or self.__fill_color
        self.surface.fill(self.__fill_color)