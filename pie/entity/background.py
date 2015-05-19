"""Background Entities.
"""

import functools

import pygame

import pie._pygame.sprite

from pie.entity import MViewport
from pie.entity.primitive import Fill, Image
from pie.math import project_3d


class BackgroundFill(Fill):
    pass


class BackgroundImage(Image):
    pass


class ParallaxBackground(pie._pygame.sprite.OrderedUpdates, MViewport):
    """
    """
    def __init__(self, *entities, viewport=None):
        """

        :param entities:
        :param viewport:
        """
        MViewport.__init__(self, viewport or
                           pygame.display.get_surface().get_rect())
        pie._pygame.sprite.OrderedUpdates.__init__(self, *entities)

    def update(self, *args):
        """
        """

        if self.viewport_changed:
            viewport_size = self.viewport.size
            project = functools.partial(project_3d,
                                        surface_size=viewport_size,
                                        recording_surface=viewport_size + (1,))
            for entity in self.sprites():
                entity.viewport.topleft = project(self.viewport.topleft +
                                                  (entity.parallax_distance,))
                entity.update(self, *args)
            MViewport.update(self, *args)
        else:
            pie._pygame.sprite.OrderedUpdates.update(self, *args)