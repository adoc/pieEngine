"""
"""

import pygame.math

import pie._pygame.sprite

from pie.entity import MRect
from pie.entity.primitive import Fill
from pie.entity.image import Image


class BackgroundFill(Fill):
    pass


class BackgroundImage(Image):
    pass


class ParallaxBackground(pie._pygame.sprite.OrderedUpdates):
    def __init__(self, *entities, viewport=None):
        pie._pygame.sprite.OrderedUpdates.__init__(self, *entities)
        self.__viewport = viewport
        self.__old_viewport = None

    def update(self):
        if self.viewport_changed:
            for entity in self.sprites():
                entity.viewport.topleft = (
                    pygame.math.Vector2(self.viewport.topleft) *
                    entity.parallax_offset)
            self.__old_viewport = self.__viewport.copy()

    @property
    def viewport(self):
        return self.__viewport

    @property
    def viewport_changed(self):
        return self.__old_viewport != self.__viewport

