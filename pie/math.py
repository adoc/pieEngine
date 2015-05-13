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
    return Vector2(math.ceil(dif_vec.x), math.ceil(dif_vec.y))
    #return dif_vec


def sinus(period, amplitude, offset, phase=0):
    # In radians
    # period from 0.0 to 1.0
    # amplitude in pixels.
    # offset in pixels.
    if not period:
        return offset
    return amplitude * math.sin(period + phase) + offset


def vect_sum(coord1, coord2):
    return Vector2(coord1) + Vector2(coord2)


def project_3d(point, surface_size=(1000, 1000),
               recording_surface=(1000, 1000, 1)):
    """Project to 2D surface.

    Based on:
    b(x) = (d(x)s(x)) / (d(z)r(x))r(z)

    b(y) = (d(y)s(y)) / (d(z)r(y))r(z)

    https://en.wikipedia.org/wiki/3D_projection

    :param point:
    :param surface_size:
    :param recording_surface:
    :return tuple: (x, y) plotted point.
    """

    #       X Component
    return ((point[0] * surface_size[0]) /
            ((point[2] * recording_surface[0]) * recording_surface[2]),
    #       Y Component
            (point[1] * surface_size[1]) /
            ((point[2] * recording_surface[1]) * recording_surface[2]))