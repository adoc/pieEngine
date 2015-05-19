"""
"""

import pygame

from pie.entity.base import *

__all__ = ('Point', 'Fill', 'Image')


class Point(SpriteRect):
    def __init__(self, pos, radius=0, **kwa):
        if radius > 5 and not 'collide_func' in kwa:
            kwa['collide_func'] = pygame.sprite.collide_circle
        SpriteRect.__init__(self, pos, (0, 0), *kwa)
        self.__radius = radius

    @property
    def radius(self):
        return self.__radius


class Fill(SpriteSurface):
    """A static solid color surface.
    """
    def __init__(self, *surface_args, fill_color=pygame.Color(0, 0, 0), **kwa):
        """

        :param surface_args:
        :param fill_color:
        :param kwa:
        :return:
        """
        SpriteSurface.__init__(self, *surface_args, **kwa)

        self.__fill_color = fill_color
        self.fill()

    def fill(self, fill_color=None):
        """

        :param fill_color:
        :return:
        """
        self.__fill_color = fill_color or self.__fill_color
        self.surface.fill(self.__fill_color)


Image = SpriteSurface