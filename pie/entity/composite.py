import pygame
import pygame.math

from pie.entity import MIdentity, MRect
from pie.math import vect_diff

i = 0

def radial_distribution(group, radius):
    global i
    i += 1
    interval = 360 / len(group)
    print(interval)

    rotation_vect = pygame.math.Vector2(0, radius)
    center_vect = pygame.math.Vector2(group.rect.center)

    for n, sprite in enumerate(group):
        a =  vect_diff(center_vect, rotation_vect.rotate(interval * n + i))
        sprite.rect.center = a


class Distributed(pygame.sprite.OrderedUpdates, MIdentity, MRect):
    def __init__(self, *entities,
                 distribute_factory=lambda g: radial_distribution(g, 100)):
        self.__distribute_factory = distribute_factory
        pygame.sprite.OrderedUpdates.__init__(self, *entities)
        MIdentity.__init__(self)
        self.collide_func = pygame.sprite.collide_rect

    def __update_entities(self):
        sprites = self.sprites()
        if sprites:
            MRect.__init__(self, sprites[0].rect.unionall(sprites))
        else:
            MRect.__init__(self, -1, -1, 0, 0)

        self.__distribute_factory(self)

    def add(self, *sprites):
        pygame.sprite.OrderedUpdates.add(self, *sprites)
        self.__update_entities()

    def remove(self, *sprites):
        pygame.sprite.OrderedUpdates.remove(self, *sprites)
        self.__update_entities()

    def update(self):
        print("hi")
        self.__distribute_factory(self)
        #pygame.sprite.OrderedUpdates.update(self)