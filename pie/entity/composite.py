import pygame
import pygame.math

from pie.entity import MIdentity, MRect, ESprite
from pie.math import vect_diff


# TODO: Write a version of this with interpolation. (Probably class based)
def radial_distribution(group, radius, interval=0):
    deg = 360 / len(group)

    rotation_vect = pygame.math.Vector2(radius, radius)
    center_vect = pygame.math.Vector2(group.rect.center)

    for n, sprite in enumerate(group):
        sprite.rect.center = vect_diff(center_vect,
                                       rotation_vect.rotate(deg * n + interval))


class RadialDistribution:
    pass


class Distributed(pygame.sprite.OrderedUpdates, MIdentity, MRect):
    def __init__(self, *entities,
                 distribute_factory=lambda g: radial_distribution(g, 50),
                 collide_func=pygame.sprite.collide_rect):
        self.__rect_init = False
        self.__distribute_factory = distribute_factory
        self.__old_rect = None
        self.collide_func = collide_func
        pygame.sprite.OrderedUpdates.__init__(self, *entities)
        MIdentity.__init__(self)

    def __update_bounding_rect(self):
        # TODO: Decent solution with __old_rect, but this still feels hackish.
        sprites = self.sprites()

        if self.__old_rect and self.__old_rect != self.rect:
            move_vect = vect_diff(self.rect.topleft, self.__old_rect.topleft)
            for sprite in sprites:
                sprite.move_ip(*move_vect)

        MRect.__init__(self, sprites[0].rect.unionall(sprites))
        self.__old_rect = self.rect.copy()

    def distribute(self):
        self.__update_bounding_rect()
        self.__distribute_factory(self)

    def add(self, *sprites):
        pygame.sprite.OrderedUpdates.add(self, *sprites)
        self.distribute()

    def remove(self, *sprites):
        pygame.sprite.OrderedUpdates.remove(self, *sprites)
        self.distribute()

    def update(self):
        pygame.sprite.OrderedUpdates.update(self)
        self.__update_bounding_rect()