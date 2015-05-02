"""
"""

import io
import zipfile

from collections import defaultdict

import pygame


class AssetsMixin:
    def __init__(self):
        self.__animations = defaultdict(list)
        self.__debug = True

    def __iter_animation(self, zipfilepath, size=None):
        zf = zipfile.ZipFile(zipfilepath, 'r')

        for name in sorted(zf.namelist()):
            bytes_io = io.BytesIO(zf.read(name))
            image = pygame.image.load(bytes_io)
            image.convert_alpha(self._surface)
            if size:
                image = pygame.transform.scale(image, size)
            yield image

    def init_animation(self, name, zipfilepath, size=None):
        if self.__debug:
            self._surface.blit(
                    self._debug_font.render("Loading and Processing images...",
                                            1, (240, 240, 240)), (8, 8))
            self.buffer()
        self.__animations[name].extend(self.__iter_animation(zipfilepath,
                                                           size=size))

    def get_largest_frame(self, animation_name):
        frame_size = (0, 0)

        animation = self.__animations[animation_name]
        largest_frame = animation[0]

        for image in animation:
            img_size = image.get_size()
            if img_size[0] > frame_size[0] or img_size[1] > frame_size[1]:
                largest_frame = image
                frame_size = (img_size[0], img_size[1])

        return largest_frame

    @property
    def animations(self):
        return self.__animations