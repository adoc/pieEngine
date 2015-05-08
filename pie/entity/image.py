from pie.entity import ESprite

__author__ = 'coda'


class Image(ESprite):
    def __init__(self, *surface, sprite_groups=[], surface_factory=None,
                 **rect_kwa):
        ESprite.__init__(self,
                         surface_factory=surface and (
                         lambda: surface[0]) or surface_factory,
                         sprite_groups=sprite_groups, **rect_kwa)


