"""Background Entities.
"""

import copy
import functools

import pygame

from pie.entity import MViewport
from pie.entity.base import SpriteRect
from pie.entity.group import OrderedEntities
from pie.entity.primitive import Fill, Image, ImageSurfarray
from pie.math import project_3d


class BackgroundFill(Fill):
    """Alias to :class:`pie.entity.primitive.Fill`
    """
    pass


class BackgroundImage(Image):
    """Alias to :class:`pie.entity.primitive.Image`
    """
    pass


# TODO: Uses surfarray but some math not figured out. .roll is slowwwww!!!
class RepeatingImage(ImageSurfarray):
    def __init__(self, entity, *args, **kwa):
        self.__entity = entity
        ImageSurfarray.__init__(self, entity.surface, *args, **kwa)

    def update(self, *args):
        if self.viewport_changed:
            self.offset(self.viewport.topleft)
            MViewport.update(self)

# TODO: Uses surfarray but some math not figured out. .roll is slowwwww!!!
class RepeatingProjectedImage(RepeatingImage):
    def __init__(self, entity, *args, **kwa):
        self.__entity = entity
        RepeatingImage.__init__(entity.surface, *args, **kwa)
        self.__size = self.viewport.size
        self.__project = functools.partial(project_3d,
                                    surface_size=self.__size,
                                    recording_surface=self.__size + (1,))

    def update(self, *args):
        if self.viewport_changed:
            x, y = self.viewport.topleft
            self.offset(self.__project(x, y, self.parallax_distance))
            MViewport.update(self)


class RepeatingEntity(MViewport, OrderedEntities):
    def __init__(self, entity_factory):
        #  SpriteRect.__init__(self, entity.rect.copy())
        self.__quads = [entity_factory() for _ in range(4)]
        MViewport.__init__(self, self.__quads[0].rect.copy())
        OrderedEntities.__init__(self, *self.__quads)
        self.__size = self.viewport.size
        self.__project = functools.partial(project_3d,
                                    surface_size=self.__size,
                                    recording_surface=self.__size + (1,))
        self._adjust_viewport()

    def _adjust_viewport(self, offset=(0, 0)):
        screen_rect = pygame.display.get_surface().get_rect()
        entities = self.__quads

        size_x, size_y = self.__size
        off_x, off_y = (offset[0],
                        offset[1])

        # Quad 1
        entity = entities[0]
        lsize_x, lsize_y = (size_x * entity.parallax_distance,
                            size_y * entity.parallax_distance)
        loff_x, loff_y = (off_x % lsize_x,
                        off_y % lsize_y)

        entity.viewport.topleft = self.__project((-loff_x, -loff_y + lsize_y,
                                            entity.parallax_distance))


        # Quad 2
        entity = entities[1]
        lsize_x, lsize_y = (size_x * entity.parallax_distance,
                            size_y * entity.parallax_distance)
        loff_x, loff_y = (off_x % lsize_x,
                        off_y % lsize_y)
        entity.viewport.topleft = self.__project((-loff_x + lsize_x, -loff_y + lsize_y,
                                            entity.parallax_distance))

        # # # Quad 3
        entity = entities[2]
        lsize_x, lsize_y = (size_x * entity.parallax_distance,
                            size_y * entity.parallax_distance)
        loff_x, loff_y = (off_x % lsize_x,
                        off_y % lsize_y)
        entity.viewport.topleft = self.__project((-loff_x + lsize_x, -loff_y,
                                            entity.parallax_distance))

        # # #Quad 4
        entity = entities[3]
        lsize_x, lsize_y = (size_x * entity.parallax_distance,
                            size_y * entity.parallax_distance)
        loff_x, loff_y = (off_x % lsize_x,
                        off_y % lsize_y)
        entity.viewport.topleft = self.__project((-loff_x, -loff_y,
                                            entity.parallax_distance))


    def update(self):
        if self.viewport_changed:
            self._adjust_viewport(self.viewport.topleft)
        MViewport.update(self)


class MParallax(MViewport):
    def __init__(self, viewport):
        MViewport.__init__(self, viewport or
                           pygame.display.get_surface().get_rect())
        #self.__layers = entities
        #self.add(*entities)

    def update(self, *args):
        """Update the viewport position of each contained entity if
        this viewport has changed. Uses the standard 3D projection
        function :func:`pie.math.project_3d`

        :param args: Pass-through args.
        """
        # print("Parallax: ", self.viewport_changed)
        if self.viewport_changed:
            size_x, size_y = viewport_size = self.viewport.size
            project = functools.partial(project_3d,
                                        surface_size=viewport_size,
                                        recording_surface=viewport_size + (1,))
            for entity in self.entities():
                entity.viewport.topleft = project(self.viewport.topleft +
                                                  (entity.parallax_distance,))
                entity.update(self, *args)
            MViewport.update(self, *args)


class ParallaxBackground(MParallax, OrderedEntities):
    """Provides a parallax background. Pass any number of `entities`
    that are center aligned. Change the `viewport`
    """

    def __init__(self, *entities, viewport=None):
        """

        :param entities:
        :param viewport:
        """

        MParallax.__init__(self, viewport)
        OrderedEntities.__init__(self, *entities)

    def update(self, *args):
        MParallax.update(self, *args)
        OrderedEntities.update(self)


class ScrollingParallaxBackground(MViewport, OrderedEntities):
    def __init__(self, *entity_factories, viewport=None):
        MViewport.__init__(self, pygame.display.get_surface().get_rect())
        self.__scrollers = [RepeatingEntity(entity_factory)
                                for entity_factory in entity_factories]

        OrderedEntities.__init__(self, *self.__scrollers)

    def update(self, *args):
        #MParallax.update(self, *args)
        OrderedEntities.update(self, *args)
        if self.viewport_changed:
            for entity in self.__scrollers:
                entity.viewport.topleft = self.viewport.topleft
                entity.update()


        # else:
        #     for entity in self.__scrollers:
        #         entity.update()