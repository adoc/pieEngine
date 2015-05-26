"""
"""
import time

import numpy
import pygame

from pie.entity import MViewport
from pie.entity.base import *

__all__ = ('Point', 'Fill', 'Image')


class Point(SpriteRect):
    """
    """

    def __init__(self, pos, radius=0, collide_func=None,
                 **kwa):
        """

        :param pos:
        :param radius:
        :param kwa:
        :return:
        """

        if not collide_func and radius > 0:
            kwa['collide_func'] = pygame.sprite.collide_circle

        SpriteRect.__init__(self, pos, (1, 1), **kwa)
        self.__radius = radius

    @property
    def radius(self):
        """
        :return: Point radius.
        """
        return self.__radius


class Fill(SpriteSurface):
    """A static solid color surface.
    """
    def __init__(self, *surface_args, fill_color=pygame.Color(0, 0, 0), **kwa):
        """

        :param surface_args:
        :param fill_color:
        :param kwa:
        :return:
        """
        SpriteSurface.__init__(self, *surface_args, **kwa)

        self.__fill_color = fill_color
        self.fill()

    def fill(self, fill_color=None):
        """

        :param fill_color:
        :return:
        """
        self.__fill_color = fill_color or self.__fill_color
        self.surface.fill(self.__fill_color)


Image = Surface = SpriteSurface


ImageSurfarray = SpriteSurfarray

def iter_bake_fade(surface, spread=5, alpha_threshold=0):
    for i in range(spread):
        surf = surface.copy()

        alpha = pygame.surfarray.pixels_alpha(surf)
        alpha[alpha>alpha_threshold] *= (i + 1) / spread

        #max = numpy.amax(alpha)
        #alpha[alpha>0] -= numpy.amax(alpha) / spread * (i+1)

        #surf.set_alpha(255-(max_alpha/spread * i), pygame.RLEACCEL)
        #surf.set_alpha(128)
        #surf_r = pygame.surfarray.pixels3d(surf)
        #print(numpy.take(surf_r, (), 2).shape)
        #print(surf_r.shape)

        yield surf

class BlurredImage(SpriteSurface):
    def __init__(self, *args, max_spread=8, secondary_blur_surface=None, **kwa):
        Image.__init__(self, *args, **kwa)
        self.__max_spread = max_spread
        self.__secondary_blur_surface = secondary_blur_surface

        fade_alpha = 255
        self.__blit_args = []
        if self.__secondary_blur_surface:
            self.__blits = tuple(iter_bake_fade(self.__secondary_blur_surface, spread=max_spread))
        else:
            self.__blits = tuple(iter_bake_fade(self.image, spread=max_spread))

    def blit_to(self, surface):
        #surf = self.__surfaces.pop()
        for surf, args in zip(self.__blits, self.__blit_args):
            surface.blit(surf, *args) #, special_flags=pygame.BLEND_RGBA_ADD)

        surface.blit(self.image, self.rect.copy(), self.viewport.copy())

    def update(self, *args):
        if self.viewport_changed:
            self.__blit_args.append((self.rect.copy(), self.viewport.copy()))
            self.__blit_args = self.__blit_args[-self.__max_spread:]
        else:
            self.__blit_args = []
            # if self.__blit_args:
            #     self.__blit_args.pop()

        MViewport.update(self)


class BlurredImage_old(Image):
    def __init__(self, *args, max_spread=10, **kwa):
        Image.__init__(self, *args, **kwa)

        self.__dummy_surf = pygame.Surface(self.viewport.size)

        self.__max_spread = max_spread
        self.__surfarrays = []
        for _ in range(max_spread):
            self.__surfarrays.append(numpy.zeros(self.viewport.size))

        self.__accumulator = pygame.surfarray.array2d(self.__dummy_surf)

        self.__idx = 0

    def blit_to(self, surface):
        size_x, size_y = surface.get_rect().size
        rect = Image.blit_to(self, self.__dummy_surf)

        s = self.__surfarrays[self.__idx] = pygame.surfarray.array2d(self.__dummy_surf)
        self.__accumulator = numpy.add(self.__accumulator, s)

        pygame.surfarray.blit_array(surface, self.__accumulator[:size_x,:size_y])

        try:
            return rect
        finally:
            self.__accumulator = numpy.subtract(self.__accumulator,
                                                self.__surfarrays[self.__idx])
            self.__idx += 1
            self.__idx %= self.__max_spread
            self.__dummy_surf.fill((0,0,0))
