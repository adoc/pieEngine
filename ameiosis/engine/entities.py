import uuid

import pygame


__all__ = ('next_entity_ord', 'EntityBase', 'RectEntity', 'SurfaceEntity')


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


class RectEntity(BaseEntity):
    """
    """

    def __init__(self, *rect_args, rect_factory=None):
        super(RectEntity, self).__init__()
        self.rect_reset(*rect_args, rect_factory=rect_factory)

    @property
    def rect(self):
        return self.__rect

    def rect_reset(self, *rect_args, rect_factory=None):
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
        self.surface_reset(*surface_args, surface_factory=surface_factory)

    @property
    def surface(self):
        return self.__surface

    @property
    def image(self):
        """Synonym to enable mixing with ``pygame.sprite.Sprite``
        """
        # TODO: This assumes subclassing Sprite. Determine if we subclass or compose it.
        return self.__surface

    def surface_reset(self, *surface_args, surface_factory=None):
        self.__surface = (callable(surface_factory) and surface_factory() or
                          pygame.Surface(*surface_args))

    def surface_convert(self, *args, **kwa):
        self.__surface = self.__surface.convert(*args, **kwa)

    def surface_convert_alpha(self, *args, **kwa):
        self.__surface = self.__surface.convert_alpha(*args, **kwa)


class SurfaceRectEntity(RectEntity, SurfaceEntity):
    def __init__(self, *surface_args, surface_factory=None, **rect_kwa):
        BaseEntity.__init__(self)
        self.surface_reset(*surface_args,
                               surface_factory=surface_factory, **rect_kwa)

    def surface_reset(self, *surface_args, surface_factory=None, **rect_kwa):
        SurfaceEntity.surface_reset(self, *surface_args,
                                    surface_factory=surface_factory)
        self.rect_reset(self.surface.get_rect(**rect_kwa))

    def present(self):
        return (self.surface, self.rect)


# Composition. Fail??
class SurfaceRectSpriteEntity(SurfaceRectEntity):
    def __init__(self, *surface_args, surface_factory=None,
                 sprite_factory=None, **surface_rect_kwa):
        BaseEntity.__init__(self)
        self.sprite_reset(*surface_args, surface_factory=surface_factory,
                 sprite_factory=sprite_factory, **surface_rect_kwa)

    def sprite_reset(self, *surface_args, surface_factory=None,
             sprite_factory=None, sprite_rect_factory=None, **surface_rect_kwa):
        SurfaceRectEntity.surface_reset(*surface_args,
                                        surface_factory=surface_factory,
                                        **surface_rect_kwa)
        self.__sprite = sprite_factory()
        self.__sprite.rect = (callable(sprite_rect_factory) and
                              sprite_rect_factory() or self.rect)
        self.__sprite.image = self.surface

    @property
    def sprite(self):
        return self.__sprite

    def present(self):
        return (self.surface, self.rect, self.sprite)


# Inheritance. ??
def make_sprite_entity_cls(cls=pygame.sprite.Sprite):
    """
    This allows for use of of pygame.sprite.DirtySprite as well.
    """

    class SpriteEntity(cls, SurfaceRectEntity):
        def __init__(self, *groups, **surface_rect_kwa):
            cls.__init__(self, *groups)
            SurfaceRectEntity.__init__(**surface_rect_kwa)

    return SpriteEntity


class FillEntity(SurfaceRectEntity):
    """
    """
    def __init__(self, *surface_args, surface_factory=None,
                 fill_color=pygame.Color(0, 0, 0), **rect_kwa):
        SurfaceRectEntity.__init__(self, *surface_args,
                                   surface_factory=surface_factory, **rect_kwa)
        self.__fill_color = fill_color

    def update(self):
        self.surface.fill(self.__fill_color)