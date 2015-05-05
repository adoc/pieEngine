"""
"""

import io
import zipfile

from collections import defaultdict

import pygame


class Animations(defaultdict):
    def __init__(self, screen, debug=True):
        defaultdict.__init__(self, list)
        self.__screen = screen
        self.__debug = debug

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
        # TODO: Figure out a way to show this debug information.
        # if self.__debug:
        #     self.add_draw(lambda: (self._debug_font.render("Loading and Processing images...",
        #                                     1, (240, 240, 240)), (8, 8)))
        #     self.render()
        #     self.buffer()
        self[name].extend(self.__iter_from_zip(zip_filepath, size=size))

    def get_largest_frame(self, name):
        frame_size = (0, 0)

        animation = self[name]
        largest_frame = animation[0]

        for image in animation:
            img_size = image.get_size()
            if img_size[0] > frame_size[0] or img_size[1] > frame_size[1]:
                largest_frame = image
                frame_size = (img_size[0], img_size[1])

        return largest_frame


class AssetHandler:
    def __init__(self, screen, debug=True):
        self.animations = Animations(screen, debug=debug)