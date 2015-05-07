# TODO: Module needs to refactor away from "reset" methods. .reset may not be needed.

import uuid

import pygame

from pie.animation import AnimationLoop
from pie.asset import get_largest_frame


__all__ = ('next_entity_ord',
           'BaseEntity',
           'RectEntity',
           'SurfaceEntity',
           'SurfaceRectEntity',
           'PointEntity',
           'SpriteEntity',
           'DirtySpriteEntity',
           'DrawSurfaceEntity',
           'FillSurfaceEntity',
           'FillSpriteEntity',
           'AnimatedEntity')


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
        """Base parent class for all Entities. Provides an ordinal
        ``ord`` and unique identifier ``id``. Default uses module-level
        counter for the ordinal and UUID4 for the id. Either can be
        overridden by passing an ``ord_factory`` and/or ``id_factory``
        keyword argument.

        :param ord_factory:
        :param id_factory:

        :return:


        """
        self.__ord = ord_factory()
        self.__id = id_factory()

    @property
    def ord(self):
        """Return the ordinal of this entity.
        """
        return self.__ord

    @property
    def id(self):
        """Return the unique identifier of this entity. (By default is
        a UUID object.
        """
        return self.__id

    def update(self):
        raise NotImplementedError("Entity ``update`` method is not "
                                  "implemented.")

    def present(self):
        raise NotImplementedError("Entity ``present`` method is not "
                                  "implemented.")


class RectEntity(BaseEntity):
    """Container Entity for a ``pygame.Rect`` object. Provides
    ``rect`` property to get the ``Rect`` object. Also provides a
    ``reset`` method to replace the current ``Rect``.
    """

    def __init__(self, *rect_args, rect_factory=None):
        super(RectEntity, self).__init__()
        self.reset(*rect_args, rect_factory=rect_factory)

    @property
    def rect(self):
        """Returns the ``Rect`` object.
        """
        return self.__rect

    def reset(self, *rect_args, rect_factory=None):
        """Reset the ``Rect`` object.

        :param *rect_args: passed directly to a ``pygame.Rect``
            constructor
        :param rect_factory: Rect factory function. This takes
            precedence over ``*rect_args``
        """
        self.__rect = (callable(rect_factory) and rect_factory() or
                       pygame.Rect(*rect_args))
        self.__rect.normalize()

    def rect_move(self, x, y):
        self.__rect = self.__rect.move(x, y)

    def rect_inflate(self, x, y):
        self.__rect = self.__rect.inflate(x, y)

    def rect_clamp(self, rect):
        self.__rect = self.__rect.clamp(rect)

    def rect_clip(self, rect):
        self.__rect = self.__rect.clip(rect)

    def rect_union(self, rect):
        self.__rect = self.__rect.union(rect)

    def rect_unionall(self, rect_sequence):
        self.__rect = self.__rect.unionall(rect_sequence)

    def rect_fit(self, rect):
        self.__rect = self.__rect.fit(rect)


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
        return self.surface

    def reset(self, *surface_args, surface_factory=None):
        self.__surface = (callable(surface_factory) and surface_factory() or
                          pygame.Surface(*surface_args))

    def surface_convert(self, *args, **kwa):
        self.__surface = self.__surface.convert(*args, **kwa)

    def surface_convert_alpha(self, *args, **kwa):
        self.__surface = self.__surface.convert_alpha(*args, **kwa)

    def surface_transform(self, xform_func, *xform_args, **xform_kwa):
        self.reset(surface_factory=lambda: xform_func(self.__surface,
                                                      *xform_args, **xform_kwa))


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

    # Override rect methods that will transform the final surface.
    # TODO: Update with transforms!
    def rect_inflate(self, x, y):
        self.__rect = self.__rect.inflate(x, y)

    def rect_clamp(self, rect):
        self.__rect = self.__rect.clamp(rect)

    def rect_clip(self, rect):
        self.__rect = self.__rect.clip(rect)

    def rect_union(self, rect):
        self.__rect = self.__rect.union(rect)

    def rect_unionall(self, rect_sequence):
        self.__rect = self.__rect.unionall(rect_sequence)

    def rect_fit(self, rect):
        self.__rect = self.__rect.fit(rect)


# User Implementable Classes
class PointEntity(pygame.sprite.Sprite, RectEntity):
    def __init__(self, pos, radius=0):
        RectEntity.__init__(self, pos, (0, 0))
        self.radius = radius


class SpriteEntity(pygame.sprite.Sprite, SurfaceRectEntity):
    def __init__(self, *surface_args, surface_factory=None,
                 sprite_groups=[], **surface_rect_kwa):
        BaseEntity.__init__(self)
        SurfaceRectEntity.reset(*surface_args,
                                        surface_factory=surface_factory,
                                        **surface_rect_kwa)
        pygame.sprite.Sprite.__init__(*sprite_groups)


class DirtySpriteEntity(pygame.sprite.DirtySprite, SurfaceRectEntity):
    def __init__(self, *surface_args, surface_factory=None,
                 sprite_groups=[], **surface_rect_kwa):
        BaseEntity.__init__(self)
        SurfaceRectEntity.reset(self, *surface_args,
                                        surface_factory=surface_factory,
                                        **surface_rect_kwa)
        pygame.sprite.DirtySprite.__init__(self, *sprite_groups)


class DrawSurfaceEntity(pygame.sprite.Sprite, SurfaceRectEntity):
    """A surface used generally for ``pygame.draw`` operations.
    """
    def __init__(self, *surface_args, surface_factory=None,
                 sprite_groups=[], **surface_rect_kwa):
        BaseEntity.__init__(self)
        SurfaceRectEntity.reset(self, *surface_args,
                                        surface_factory=surface_factory,
                                        **surface_rect_kwa)
        pygame.sprite.Sprite.__init__(self, *sprite_groups)



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


class FillSpriteEntity(SpriteEntity):
    def __init__(self, *surface_args, surface_factory=None,
                 fill_color=pygame.Color(0, 0, 0), sprite_groups=[],
                 **rect_kwa):
        BaseEntity.__init__(self)
        self.reset(*surface_args, surface_factory=surface_factory,
              fill_color=fill_color, **rect_kwa)
        pygame.sprite.Sprite.__init__(self, *sprite_groups)

    def reset(self, *surface_args, surface_factory=None,
                 fill_color=pygame.Color(0, 0, 0), sprite_groups=[],
                 **rect_kwa):
        SpriteEntity.reset(self, *surface_args,
                           **rect_kwa)
        self.__fill_color = fill_color
        self.surface.fill(self.__fill_color)


class ImageSpriteEntity(SpriteEntity):
    def __init__(self, *surface, sprite_groups=[], surface_factory=None, **rect_args):
        BaseEntity.__init__(self)
        self.reset(surface_factory=lambda: surface and surface[0] or
                                           surface_factory, **rect_args)

    def group_clear(self, surface, rect):
        surface.blit(self.image, rect, area=rect)


class AnimatedEntity(pygame.sprite.Sprite, RectEntity):
    def __init__(self, frames, sprite_groups=[], autostart=True,
                 animation_cls=AnimationLoop, **surface_rect_kwa):
        BaseEntity.__init__(self)
        # TODO: get_largest_frame may not be needed if we enforce animations to have a constant frame size. (which we should)
        RectEntity.reset(self,
                         get_largest_frame(frames).get_rect(**surface_rect_kwa))
        pygame.sprite.Sprite.__init__(self, *sprite_groups)

        self.__frames = tuple(frames) # Not mutable for now.
        self.__frame_index = 0
        self.__frame_interval = 1
        self.__frame_count = len(frames)
        self.__animation_obj = animation_cls(self)

        self.autostart = autostart

        if autostart:
            self.__animation_obj.start()

    #Transport props
    @property
    def at_start(self):
        return self.__frame_index == 0

    @property
    def at_end(self):
        return self.__frame_index == self.__frame_count - 1

    @property
    def is_reversed(self):
        return self.__frame_interval < 0

    @property
    def surface(self):
        return self.__frames[self.__frame_index]

    # Transport methods
    def advance(self):
        self.__frame_index += self.__frame_interval
        self.__frame_index %= self.__frame_count

    def negate_interval(self):
        self.__frame_interval = -self.__frame_interval

    def rewind(self):
        self.__frame_index = 0

    # Loop Method
    def update(self):
        self.__animation_obj.update()

    def present(self):
        return (self.surface, self.rect)


class CompositeEntity(BaseEntity):
    def __init__(self):
        pass

    # rect??
    # dirty rect?


    def present_comp(self):
        pass




# TODO: Not finished. Flesh this out and possibly make it an entity.
class AnimatedSpriteCluster:
    def __init__(self, animated_sprites, pos, size, distribution_function=None, animation_function=None):
        self.__animated_sprites = animated_sprites
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])

        self.__distribution_function = distribution_function
        self.__animation_function = animation_function

    def update(self):
        map(lambda s: s.update(), self.__animated_sprites)

    def draw(self, surface):
        map(lambda s: s.draw(surface), self.__animated_sprites)