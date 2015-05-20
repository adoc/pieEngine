"""Background Entities.
"""

import functools

import pygame

from pie.entity import MViewport
from pie.entity.group import OrderedEntities
from pie.entity.primitive import Fill, Image
from pie.math import project_3d


class BackgroundFill(Fill):
    """Alias to :class:`pie.entity.primitive.Fill`
    """
    pass


class BackgroundImage(Image):
    """Alias to :class:`pie.entity.primitive.Image`
    """
    pass


class ParallaxBackground(OrderedEntities, MViewport):
    """Provides a parallax background. Pass any number of `entities`
    that are center aligned. Change the `viewport`
    """

    def __init__(self, *entities, viewport=None):
        """

        :param entities:
        :param viewport:
        """
        MViewport.__init__(self, viewport or
                           pygame.display.get_surface().get_rect())
        OrderedEntities.__init__(self, *entities)

    def update(self, *args):
        """Update the viewport position of each contained entity if
        this viewport has changed. Uses the standard 3D projection
        function :func:`pie.math.project_3d`

        :param args: Pass-through args.
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
            OrderedEntities.update(self, *args)