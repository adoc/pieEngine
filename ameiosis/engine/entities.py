import uuid

import pygame


# TODO: Needs to be updated, otherwise we need to allow ALL.
#__all__ = ('next_entity_ord', 'EntityBase', 'RectEntity', 'SurfaceEntity')


__entity_ord = 0
def next_entity_ord():
    """Increment the singleton entity ordinal and return it.
    Note: This is not multi-process safe but should be thread safe.
    :return int: next entity ordinal.
    """
    global __entity_ord
    __entity_ord += 1
    return __entity_ord


def _reset_entity_ord(confirm=False):
    """Testing purposes only.

    :param confirm:
    :return:
    """
    global __entity_ord
    if confirm:
        __entity_ord = 0


class BaseEntity:
    """
    """

    def __init__(self, ord_factory=next_entity_ord, id_factory=uuid.uuid4):
        """

        :param ord_factory:
        :param id_factory:

        :return:


        """
        self.__ord = ord_factory()
        self.__uuid = id_factory()

    @property
    def ord(self):
        return self.__ord

    @property
    def uuid(self):
        return self.__uuid

    @property
    def id(self):
        return self.__uuid.int

    def update(self):
        raise NotImplementedError("Entity ``update`` method is not implemented.")


class RectEntity(BaseEntity):
    """
    """

    def __init__(self, *rect_args, rect_factory=None):
        super(RectEntity, self).__init__()
        self.reset(*rect_args, rect_factory=rect_factory)

    @property
    def rect(self):
        return self.__rect

    def reset(self, *rect_args, rect_factory=None):
        self.__rect = (callable(rect_factory) and rect_factory() or
                       pygame.Rect(*rect_args))


class SurfaceEntity(BaseEntity):
    """
    """

    def __init__(self, *surface_args, surface_factory=None):
        """

        :param surface_factory:
        :return:
        """
        BaseEntity.__init__(self)
        self.reset(*surface_args, surface_factory=surface_factory)

    @property
    def surface(self):
        return self.__surface

    @property
    def image(self):
        """Synonym to enable mixing with ``pygame.sprite.Sprite``
        """
        # TODO: This assumes subclassing Sprite. Determine if we subclass or compose it.
        return self.__surface

    def reset(self, *surface_args, surface_factory=None):
        self.__surface = (callable(surface_factory) and surface_factory() or
                          pygame.Surface(*surface_args))

    def surface_convert(self, *args, **kwa):
        self.__surface = self.__surface.convert(*args, **kwa)

    def surface_convert_alpha(self, *args, **kwa):
        self.__surface = self.__surface.convert_alpha(*args, **kwa)


class SurfaceRectEntity(RectEntity, SurfaceEntity):
    def __init__(self, *surface_args, surface_factory=None, **rect_kwa):
        BaseEntity.__init__(self)
        self.reset(*surface_args,
                               surface_factory=surface_factory, **rect_kwa)

    def reset(self, *surface_args, surface_factory=None, **rect_kwa):
        SurfaceEntity.reset(self, *surface_args,
                                    surface_factory=surface_factory)
        RectEntity.reset(self, self.surface.get_rect(**rect_kwa))

    def present(self):
        return (self.surface, self.rect)


class SpriteEntity(pygame.sprite.Sprite, SurfaceRectEntity):
    def __init__(self, *surface_args, surface_factory=None,
                 sprite_groups=[], **surface_rect_kwa):
        BaseEntity.__init__(self)
        pygame.sprite.Sprite.__init__(*sprite_groups)
        SurfaceRectEntity.reset(*surface_args,
                                        surface_factory=surface_factory,
                                        **surface_rect_kwa)


class DirtySpriteEntity(pygame.sprite.DirtySprite, SurfaceRectEntity):
    def __init__(self, *surface_args, surface_factory=None,
                 sprite_groups=[], **surface_rect_kwa):
        BaseEntity.__init__(self)
        pygame.sprite.DirtySprite.__init__(*sprite_groups)
        SurfaceRectEntity.reset(*surface_args,
                                        surface_factory=surface_factory,
                                        **surface_rect_kwa)


class FillSurfaceEntity(SurfaceRectEntity):
    """A static solid color surface.
    """
    def __init__(self, *surface_args, surface_factory=None,
                 fill_color=pygame.Color(0, 0, 0), **rect_kwa):
        self.reset(*surface_args, surface_factory=surface_factory,
                   fill_color=fill_color, **rect_kwa)

    def reset(self, *surface_args, surface_factory=None,
              fill_color=pygame.Color(0, 0, 0), **rect_kwa):
        SurfaceRectEntity.reset(self, *surface_args,
                                surface_factory=surface_factory, **rect_kwa)
        self.__fill_color = fill_color
        self.surface.fill(self.__fill_color)


class DrawSurfaceEntity(SurfaceRectEntity):
    """A surface used generally for drawing.
    """
    pass