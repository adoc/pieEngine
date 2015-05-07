"""
"""

import io
import zipfile

from collections import defaultdict

import pygame

__all__ = ("Animations",
           "get_largest_frame",
           "AssetHandler")


class Animations(defaultdict):
    def __init__(self, screen):
        defaultdict.__init__(self, list)
        self.__screen = screen

    def __iter_from_zip(self, zip_filepath, size=None):
        zf = zipfile.ZipFile(zip_filepath, 'r')
        for name in sorted(zf.namelist()):
            bytes_io = io.BytesIO(zf.read(name))
            image = pygame.image.load(bytes_io).convert_alpha(self.__screen)
            bytes_io.close()
            if size:
                image = pygame.transform.scale(image, size)
            yield image
        zf.close()

    def add_from_zip(self, name, zip_filepath, size=None):
        self[name].extend(self.__iter_from_zip(zip_filepath, size=size))


def get_largest_frame(frame_list):
    frame_size = (0, 0)
    largest_frame = frame_list[0]

    for image in frame_list:
        img_size = image.get_size()
        if img_size[0] > frame_size[0] or img_size[1] > frame_size[1]:
            largest_frame = image
            frame_size = (img_size[0], img_size[1])

    return largest_frame


class AssetHandler:
    def __init__(self, screen):
        self.__screen = screen
        self.animations = Animations(screen)

    def get_image(self, filepath):
        return pygame.image.load(filepath).convert_alpha(self.__screen)