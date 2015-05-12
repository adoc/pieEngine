"""
"""

import pygame


class _RenderUpdatesMixin:
    """Method ``draw`` copied directly from
    ``pygame.sprite.RenderUpdates``
    """
    def draw(self, surface):
        spritedict = self.spritedict
        surface_blit = surface.blit
        dirty = self.lostsprites
        self.lostsprites = []
        dirty_append = dirty.append
        for s in self.sprites():
            r = spritedict[s]
            # This is the line updated in order to pass flags.
            newrect = surface_blit(s.image, s.rect, s.viewport, special_flags=s.blit_flags)
            if r:
                if newrect.colliderect(r):
                    dirty_append(newrect.union(r))
                else:
                    dirty_append(newrect)
                    dirty_append(r)
            else:
                dirty_append(newrect)
            spritedict[s] = newrect
        return dirty


class OrderedUpdates(_RenderUpdatesMixin, pygame.sprite.OrderedUpdates):
    pass