"""Debug Entities.
"""

from pie.entity.base import SpriteSurface

class DebugText(SpriteSurface):
    def __init__(self, pos=(0,0), max_size=(200,-1)):

        # Can't init sprite surface until we know what we're dealing with!
        SpriteSurface.__init__(self, )