"""
"""

import pygame

import pie._pygame.sprite

__all__ = ('OrderedEntities',)


class OrderedEntities(pie._pygame.sprite.RenderUpdatesMixin,
                      pygame.sprite.OrderedUpdates):
    """Provides :class:`pygame.sprite.OrderedUpdates` with an altered
    :meth:`draw` method.

    """
    entities = pygame.sprite.OrderedUpdates.sprites