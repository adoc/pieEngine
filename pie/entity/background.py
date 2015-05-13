"""
"""
import functools

import pie._pygame.sprite

from pie.entity.primitive import Fill
from pie.entity.image import Image
from pie.math import project_3d


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
            viewport_size = self.viewport.size
            project = functools.partial(project_3d,
                                           surface_size=viewport_size,
                                          recording_surface=viewport_size +
                                                             (1,))
            for entity in self.sprites():
                entity.viewport.topleft = project(self.viewport.topleft +
                                                  (entity.parallax_distance,))

            self.__old_viewport = self.__viewport.copy()

    @property
    def viewport(self):
        return self.__viewport

    @property
    def viewport_changed(self):
        return self.__old_viewport != self.__viewport

