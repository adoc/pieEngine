"""Base user classes for Entities.
"""

#TODO: Review for 0.1.2

from pie.entity import *

__all__ = ('Rect', 'Surface', 'SpriteRect', 'SpriteSurface')


class Rect(MIdentity, MRect):
    def __init__(self, *rect_args, normalize=False, parallax_distance=0.0,
                 ord_factory=None, id_factory=None):
        MRect.__init__(self, *rect_args, normalize=normalize,
                       parallax_distance=parallax_distance)
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
    def __init__(self, *rect_args, normalize=False, parallax_distance=0.0,
                 sprite_groups=(), collide_func=None, ord_factory=None, id_factory=None):
        MRect.__init__(self, *rect_args, normalize=normalize,
                       parallax_distance=parallax_distance)
        MSprite.__init__(self, sprite_groups=sprite_groups,
                         collide_func=collide_func)
        MIdentity.__init__(self, ord_factory=ord_factory, id_factory=id_factory)


class SpriteSurface(MIdentity, MSprite, MViewport, MSurfaceRect):
    def __init__(self, *surface_args, viewport=None, convert=False,
                 alpha=False, blit_flags=0, normalize=False,
                 parallax_distance=0.0, sprite_groups=(), collide_func=None,
                 ord_factory=None, id_factory=None, **rect_pos):
        MSurfaceRect.__init__(self, *surface_args, viewport=viewport,
                              convert=convert, alpha=alpha,
                              blit_flags=blit_flags, normalize=normalize,
                              parallax_distance=parallax_distance, **rect_pos)
        MViewport.__init__(self, viewport or self.surface.get_rect())
        MSprite.__init__(self, sprite_groups=sprite_groups,
                         collide_func=collide_func)
        MIdentity.__init__(self, ord_factory=ord_factory, id_factory=id_factory)