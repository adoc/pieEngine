"""
"""

from pie.entity import MIdentity, MSurfaceRect, MSprite


class Image(MIdentity, MSurfaceRect, MSprite):
    def __init__(self, *surface_args, **kwa):
        MIdentity.__init__(self, **kwa)
        MSurfaceRect.__init__(self, *surface_args, **kwa)
        MSprite.__init__(self, **kwa)


Surface = Image