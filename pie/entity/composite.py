import entity.group
import math

import pygame
import pygame.math

import pie._pygame.sprite
from pie.entity import MIdentity, MSurfaceRect
from pie.entity.base import *
from pie.entity.animated import SequenceAnimation
from pie.math import vect_diff, sinus


# TODO: Write a version of this with interpolation. (Probably class based)
def radial_distribution(group, radius, interval=0):
    deg = 360 / len(group)

    rotation_vect = pygame.math.Vector2(radius, radius)
    center_vect = pygame.math.Vector2(group.rect.center)

    for n, sprite in enumerate(group):
        sprite.rect.center = vect_diff(center_vect,
                                       rotation_vect.rotate(deg * n + interval))


def radial_sinusoidal(group, min_radius, max_radius, interval=0):
    group_len = len(group)
    deg = 360 / group_len

    rotation_vect = pygame.math.Vector2(max_radius, max_radius)
    center_vect = pygame.math.Vector2(group.rect.center)

    amp = max_radius - min_radius
    off = (max_radius + min_radius)/2

    for n, sprite in enumerate(group):
        farthest_vector = vect_diff(center_vect,
                                       rotation_vect.rotate(deg * n + interval))
        print(sinus(n / group_len * math.pi, 1, 0))
        sprite.rect.center = center_vect.lerp(farthest_vector,
                                                sinus(n / group_len * math.pi, 1, 0))


def weird_snakey(group, min_radius, max_radius, interval=0):
    group_len = len(group)
    deg = 360 / group_len

    center_vect = pygame.math.Vector2(group.rect.center)

    amp = max_radius - min_radius
    off = (max_radius + min_radius)/2

    for n, sprite in enumerate(group):
        radius = sinus(((n / group_len)+1) * math.pi, amp, off, phase=interval/100)
        rotation_vect = pygame.math.Vector2(radius, radius)
        sprite.rect.center = vect_diff(center_vect,
                                       rotation_vect.rotate(deg * n + interval))



def werid_snake2(group, min_radius, max_radius, interval=0):
    group_len = len(group)
    deg = 360 / group_len

    center_vect = pygame.math.Vector2(group.rect.center)

    amp = max_radius - min_radius
    off = (max_radius + min_radius)/2

    print(amp,  off)

    for n, sprite in enumerate(group):
        radius = sinus(((n / group_len)+1), amp, off, phase=interval/100)
        #rotation_vect = pygame.math.Vector2(radius, radius)
        print(radius)
        sprite.rect.center = vect_diff(center_vect,
                                       rotation_vect.rotate(deg * n + interval))


# def radial_sinusoidal(group, min_radius, max_radius, interval=0):
#     group_len = len(group)
#     deg = 360 / group_len
#
#     rotation_vect = pygame.math.Vector2(max_radius, max_radius)
#     center_vect = pygame.math.Vector2(group.rect.center)
#
#     amp = max_radius - min_radius
#     off = max_radius
#
#     for n, sprite in enumerate(group):
#         radius = sinus(((n / group_len)+1) + 2 * math.pi, amp, off, phase=interval/180)
#         print(radius)
#         rotation_vect = pygame.math.Vector2(radius, radius)
#         sprite.rect.center = vect_diff(center_vect,
#                                        rotation_vect.rotate(deg * n + interval))

def fucking_cool(group, min_radius, max_radius, interval=0):
    group_len = len(group)
    deg = 360 / group_len

    rotation_vect = pygame.math.Vector2(max_radius, max_radius)
    center_vect = pygame.math.Vector2(group.rect.center)

    for n, sprite in enumerate(group):
        farthest_vector = vect_diff(center_vect,
                                       rotation_vect.rotate(deg * n + interval))
        new_rotation_vector = center_vect.lerp(farthest_vector,
                                               abs(sinus((n*interval/deg)*math.pi/180, .1, .9)))
        sprite.rect.center = new_rotation_vector


def radial_sinusoidal(group, min_radius, max_radius, interval=0):
    group_len = len(group)
    deg = 360 / group_len

    rotation_vect = pygame.math.Vector2(max_radius, max_radius)
    center_vect = pygame.math.Vector2(group.rect.center)

    for n, sprite in enumerate(group):
        farthest_vector = vect_diff(center_vect,
                                       rotation_vect.rotate((deg * n + interval) % 360))
        new_rotation_vector = center_vect.lerp(farthest_vector,
                                               abs(sinus((deg+interval*n)*math.pi/180, .1, .9)))
        sprite.rect.center = new_rotation_vector

# class RadialDistribution:
#     def __init__(self, radius):
#         self.__radius = radius
#
#     def distribute(self):
#         pass


# TODO: Might have been replaced with Viewport
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


class DistributedOnce(entity.group.OrderedEntities, Rect,
                      MRelativeGroup):
    def __init__(self, *entities,
                 distribute_factory=lambda g, i: radial_sinusoidal(g, 70, 100, interval=i),
                 collide_func=pygame.sprite.collide_rect):
        self.__rect_init = False
        self.__distribute_factory = distribute_factory
        self.__old_rect = None
        self.collide_func = collide_func
        pygame.sprite.OrderedUpdates.__init__(self, *entities)
        MIdentity.__init__(self)
        # TODO: We should find a way to init MRect here. That would remove some of the hackishness.
        MRelativeGroup.__init__(self)

    def __update_bounding_rect(self):
        # TODO: Should this happen before and after the distribution??
        sprites = self.sprites()
        Rect.__init__(self, sprites[0].rect.unionall(sprites[1:]))

    def distribute(self, idx=0):
        self.__distribute_factory(self, idx)
        # self.__update_bounding_rect()

    def add(self, *sprites):
        pygame.sprite.OrderedUpdates.add(self, *sprites)
        self.__update_bounding_rect()
        self.distribute()

    def remove(self, *sprites):
        pygame.sprite.OrderedUpdates.remove(self, *sprites)
        self.__update_bounding_rect()
        self.distribute()

    def update(self):
        pygame.sprite.OrderedUpdates.update(self)
        MRelativeGroup.update(self)


class DistributedAnimated(DistributedOnce):
    def __init__(self, *entities,
                 distribute_factory=lambda g, i: radial_sinusoidal(g, 30, 50, interval=i),
                 collide_func=pygame.sprite.collide_rect):
        DistributedOnce.__init__(self, *entities,
                 distribute_factory=distribute_factory,
                 collide_func=collide_func)

        self.__seq = SequenceAnimation(count=360, interval=2)

    def update(self):
        DistributedOnce.update(self)
        self.__seq.update()
        self.distribute(idx=self.__seq.index)
