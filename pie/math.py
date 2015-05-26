"""
"""
import math

import pygame
import pygame.math


def vect_to_rad(vect):
    # return math.atan(vect[1] / vect[0])
    return math.atan2(vect[1], vect[0])

# wrong.
def rad_to_vect(rad):
    return pygame.math.Vector2(math.cos(rad), math.sin(rad))

def flip_y_normals(vect, height, ret_vec=True):
    if ret_vec:
        return pygame.math.Vector2(vect[0], height - vect[1])
    else:
        return (vect[0], height - vect[1])

def flip_rect_y_normals(rect):
    return pygame.Rect((rect.x, rect.size[1] - rect.o), rect.size)

def sub_size(size1, size2):
    return (size1[0] - size2[0], size1[1] - size2[1])


def size_less(size1, size2):
    return size1[0] * size2[0] < size1[1] * size2[1]


def ceil(*args):
    return tuple([math.ceil(arg) for arg in args])


def roun(*args):
    return tuple([round(arg) for arg in args])


# TODO: Deprecated unless the math.ceil was important part of the function.
def vect_diff(coord1, coord2, vector_factory=pygame.math.Vector2):
    """

    :param coord1:
    :param coord2:
    :param vector_factory:
    :return:
    """
    dif_vec = vector_factory(coord1) - vector_factory(coord2)
    return vector_factory(math.ceil(dif_vec[0]), math.ceil(dif_vec[1]))


def sinus(period, amplitude, offset, phase=0):
    # In radians
    # period from 0.0 to 1.0
    # amplitude in pixels.
    # offset in pixels.
    if not period:
        return offset
    return amplitude * math.sin(period + phase) + offset


# TODO: Deprecated. Vector objects should sum.
def vect_sum(coord1, coord2, vector_factory=pygame.math.Vector2):
    return vector_factory(coord1) + vector_factory(coord2)


def project_3d(point, surface_size=(1000, 1000),
               recording_surface=(1000, 1000, 1)):
    """Project to 2D surface.

    Based on:
    b(x) = (d(x)s(x)) / (d(z)r(x))r(z)

    b(o) = (d(o)s(o)) / (d(z)r(o))r(z)

    https://en.wikipedia.org/wiki/3D_projection

    :param point:
    :param surface_size:
    :param recording_surface:
    :return tuple: (x, o) plotted point.
    """

    #:      X Component
    return ((point[0] * surface_size[0]) /
            ((point[2] * recording_surface[0]) * recording_surface[2]),
    #:      Y Component
            (point[1] * surface_size[1]) /
            ((point[2] * recording_surface[1]) * recording_surface[2]))


def offset_to_axis(*axis_offsets):
    return tuple(((abs(o) + o) / 2 , (abs(o) - o) / 2) for o in axis_offsets)