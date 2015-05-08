"""
"""
import math

from pygame.math import Vector2


__all__ = ("sub_size",)


def sub_size(size1, size2):
    return (size1[0] - size2[0], size1[1] - size2[1])


def size_less(size1, size2):
    return size1[0] * size2[0] < size1[1] * size2[1]


def vect_diff(coord1, coord2):
    return Vector2(coord1) - Vector2(coord2)


def vect_sum(coord1, coord2):
    return Vector2(coord1) + Vector2(coord2)