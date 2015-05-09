import pygame
import pygame.math

from pie.entity import MIdentity, MRect, MAnimated
from pie.math import vect_diff


# TODO: Write a version of this with interpolation. (Probably class based)
def radial_distribution(group, radius, interval=0):
    deg = 360 / len(group)

    rotation_vect = pygame.math.Vector2(radius, radius)
    center_vect = pygame.math.Vector2(group.rect.center)

    for n, sprite in enumerate(group):
        sprite.rect.center = vect_diff(center_vect,
                                       rotation_vect.rotate(deg * n + interval))


# class RadialDistribution:
#     def __init__(self, radius):
#         self.__radius = radius
#
#     def distribute(self):
#         pass


class MRelativeGroup:
    def __init__(self):
        self.__old_rect = None

    def update(self):
        """Move all sprites in self, relative to the containing rect.
        (Including rect transforms since the center-point is calculate.)
        """
        # TODO: Decent solution with __old_rect, but this still feels hackish.
        sprites = self.sprites()

        if self.__old_rect and self.__old_rect != self.rect:
            move_vect = vect_diff(self.rect.center, self.__old_rect.center)
            for sprite in sprites:
                sprite.move_ip(*move_vect)

        self.__old_rect = self.rect.copy()


class DistributedOnce(pygame.sprite.OrderedUpdates, MIdentity, MRect,
                      MRelativeGroup, MAnimated):
    def __init__(self, *entities,
                 distribute_factory=lambda g, i: radial_distribution(g, 100, interval=i),
                 collide_func=pygame.sprite.collide_rect):
        self.__rect_init = False
        self.__distribute_factory = distribute_factory
        self.__old_rect = None
        self.collide_func = collide_func
        pygame.sprite.OrderedUpdates.__init__(self, *entities)
        MIdentity.__init__(self)
        # TODO: We should find a way to init MRect here. That would remove some of the hackishness.
        MRelativeGroup.__init__(self)
        MAnimated.__init__(self, 360, interval=5)

    def __update_bounding_rect(self):
        # TODO: Should this happen before and after the distribution??
        sprites = self.sprites()
        MRect.__init__(self, sprites[0].rect.unionall(sprites))

    def distribute(self):
        self.__update_bounding_rect()
        self.__distribute_factory(self, 0)
        self.__update_bounding_rect()

    def add(self, *sprites):
        pygame.sprite.OrderedUpdates.add(self, *sprites)
        self.distribute()

    def remove(self, *sprites):
        pygame.sprite.OrderedUpdates.remove(self, *sprites)
        self.distribute()

    def update(self):
        pygame.sprite.OrderedUpdates.update(self)
        MRelativeGroup.update(self)
        self.__distribute_factory(self, self.index)
        MAnimated.update(self)

