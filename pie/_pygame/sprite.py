"""
"""


class RenderUpdatesMixin:
    """Method :meth:`pygame.sprite.RenderUpdates.draw` copied directly
    from source and modified to include a `viewport` area for the blit
    and passing `special_flags` directly from the entitiy/sprite
    object.
    """

    def draw(self, surface):
        spritedict = self.spritedict
        surface_blit = surface.blit
        dirty = self.lostsprites
        self.lostsprites = []
        dirty_append = dirty.append
        for s in self.sprites():
            if s.visible:
                r = spritedict[s]
                # This is the line updated in order to pass flags.
                # newrect = surface_blit(s.image, s.rect, s.viewport,
                #                        special_flags=s.blit_flags)
                newrect = s.blit_to(surface)
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