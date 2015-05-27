"""Entity Base user classes.
"""

#TODO: Review for 0.1.2

import numpy
import pygame

from pie.entity import *
from pie.math import offset_to_axis

__all__ = ('Rect',
           'Surface',
           'SpriteRect',
           'SpriteSurface',
           'SpriteSurfarray')


class Rect(MIdentity, MRect):
    def __init__(self, *rect_args, normalize=False, ord_factory=None,
                 id_factory=None):
        MRect.__init__(self, *rect_args, normalize=normalize)
        MIdentity.__init__(self, ord_factory=ord_factory, id_factory=id_factory)


# TODO: Will this even be used??
class Surface(MIdentity, MSurfaceRect):
    def __init__(self, *surface_args, viewport=None, convert=False,
                 alpha=False, blit_flags=0, normalize=False,
                 parallax_distance=0.0, ord_factory=None, id_factory=None,
                 **rect_pos):
        MSurfaceRect.__init__(self, *surface_args, viewport=viewport,
                              convert=convert, alpha=alpha,
                              blit_flags=blit_flags, normalize=normalize,
                              parallax_distance=parallax_distance, **rect_pos)
        MIdentity.__init__(self, ord_factory=ord_factory, id_factory=id_factory)


class SpriteRect(MIdentity, MSprite, MRect):
    def __init__(self, *rect_args, normalize=False, sprite_groups=(),
                 collide_func=None, ord_factory=None, id_factory=None):
        MRect.__init__(self, *rect_args, normalize=normalize)
        MSprite.__init__(self, sprite_groups=sprite_groups,
                         collide_func=collide_func)
        MIdentity.__init__(self, ord_factory=ord_factory, id_factory=id_factory)


class SpriteSurface(MIdentity, MSprite, MViewport, MSurfaceRect):
    def __init__(self, *surface_args, viewport=None, convert=False,
                 alpha=False, blit_flags=0, normalize=False,
                 parallax_distance=0.0, sprite_groups=(), collide_func=None,
                 ord_factory=None, id_factory=None, **rect_pos):
        MSurfaceRect.__init__(self, *surface_args,
                              convert=convert, alpha=alpha,
                              blit_flags=blit_flags, normalize=normalize,
                              **rect_pos)
        MViewport.__init__(self, viewport or self.surface.get_rect(),
                           parallax_distance=parallax_distance)
        MSprite.__init__(self, sprite_groups=sprite_groups,
                         collide_func=collide_func)
        MIdentity.__init__(self, ord_factory=ord_factory, id_factory=id_factory)


class SpriteSurfarray(MIdentity, MSprite, MViewport, MSurfarrayRect):
    def __init__(self, surface, normalize=False, viewport=None,
                parallax_distance=0.0, sprite_groups=(), ord_factory=None,
                id_factory=None, **rect_pos):
        MSurfarrayRect.__init__(self, surface, normalize=normalize, **rect_pos)
        MViewport.__init__(self, viewport or self.rect,
                           parallax_distance=parallax_distance)
        MSprite.__init__(self, sprite_groups=sprite_groups)
        MIdentity.__init__(self, ord_factory=ord_factory, id_factory=id_factory)

    # def blit_to(self, surface):
    #     # TODO: Watch this. no clue how fast/slow it is. No clue
    #
    #     # Handle viewport first.
    #     vp_pos_x, vp_pos_y = self.viewport.topleft
    #     vp_size_x, vp_size_y = self.viewport.size
    #     vp_surfarray = numpy.pad(self.surfarray, offset_to_axis(-vp_pos_x, -vp_pos_y),
    #                 'constant', constant_values=0)[vp_pos_x:vp_size_x + vp_pos_x, vp_pos_y:vp_size_y + vp_pos_y]
    #
    #     # Handle the rect now.
    #     r_pos_x, r_pos_y = self.rect.topleft
    #     r_size_x, r_size_y = self.rect.size
    #
    #     surfarray = numpy.pad(vp_surfarray, offset_to_axis(r_pos_x, r_pos_y),
    #                 'constant', constant_values=0)[r_pos_x:r_size_x + r_pos_x, r_pos_y:r_size_y + r_pos_y]
    #
    #     print(surfarray.shape)
    #
    #     max_size_x, max_size_y = surface.get_rect().size
    #     return pygame.surfarray.blit_array(surface,
    #                                        surfarray[:max_size_x,
    #                                                         :max_size_y])


class TextSurface(MIdentity, MSprite, MViewport, MSurfaceRect):
    def __init__(self, *surface_args, viewport=None, convert=False,
                 alpha=False, blit_flags=0, normalize=False,
                 parallax_distance=0.0, sprite_groups=(), collide_func=None,
                 ord_factory=None, id_factory=None, **rect_pos):
        MSurfaceRect.__init__(self, *surface_args,
                              convert=convert, alpha=alpha,
                              blit_flags=blit_flags, normalize=normalize,
                              **rect_pos)
        MViewport.__init__(self, viewport or self.surface.get_rect(),
                           parallax_distance=parallax_distance)
        MSprite.__init__(self, sprite_groups=sprite_groups,
                         collide_func=collide_func)
        MIdentity.__init__(self, ord_factory=ord_factory, id_factory=id_factory)