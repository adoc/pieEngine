"""
"""
import math

from pygame.math import Vector2


__all__ = ("sub_size",)


def sub_size(size1, size2):
    return (size1[0] - size2[0], size1[1] - size2[1])


def size_less(size1, size2):
    return size1[0] * size2[0] < size1[1] * size2[1]


def ceil(*args):
    return tuple([math.ceil(arg) for arg in args])

def roun(*args):
    return tuple([round(arg) for arg in args])


def vect_diff(coord1, coord2):
    # dif_vec = Vector2(ceil(*coord1)) - Vector2(ceil(*coord2))
    # dif_vec = Vector2(roun(*coord1)) - Vector2(roun(*coord2))
    dif_vec = Vector2(coord1) - Vector2(coord2)
    #return Vector2(math.ceil(dif_vec.x), math.ceil(dif_vec.y))
    return dif_vec



def vect_sum(coord1, coord2):
    return Vector2(coord1) + Vector2(coord2)