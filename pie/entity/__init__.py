# TODO: Module needs to refactor away from "reset" methods. .reset may not be needed.
# Bit of overkill but heart is in the right place!

import uuid

import pygame

from pie.math import vect_diff
from pie.animation import AnimationLoop, Animation


# __all__ = ('Point',
#            'Fill',
#            'BackgroundFill',
#            'Image',
#            'BackgroundImage',
#            'Animated')


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


class MIdentity:
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


class MRect:
    """Container Entity for a ``pygame.Rect`` object. Provides
    ``rect`` property to get the ``Rect`` object. Also provides a
    ``reset`` method to replace the current ``Rect``.
    """

    def __init__(self, *rect_args, rect_factory=None):
        """Reset the ``Rect`` object.

        :param *rect_args: passed directly to a ``pygame.Rect``
            constructor
        :param rect_factory: Rect factory function. This takes
            precedence over ``*rect_args``
        """

        self.__rect = (callable(rect_factory) and rect_factory() or
                       pygame.Rect(*rect_args))
        self.__rect.normalize()

    @property
    def rect(self):
        """Returns the ``Rect`` object.
        """
        return self.__rect

    def move_ip(self, x, y):
        self.__rect = self.__rect.move(x, y)

    def inflate_ip(self, x, y):
        self.__rect = self.__rect.inflate(x, y)

    def clamp_ip(self, rect):
        self.__rect = self.__rect.clamp(rect)

    def clip_ip(self, rect):
        self.__rect = self.__rect.clip(rect)

    def union_ip(self, rect):
        self.__rect = self.__rect.union(rect)

    def unionall_ip(self, rect_sequence):
        self.__rect = self.__rect.unionall(rect_sequence)

    def fit_ip(self, rect):
        self.__rect = self.__rect.fit(rect)


class MSurface:
    """
    """

    def __init__(self, *surface_args, surface_factory=None):
        """

        :param surface_factory:
        :return:
        """
        self.__surface = (callable(surface_factory) and surface_factory() or
                          pygame.Surface(*surface_args))

    @property
    def surface(self):
        return self.__surface

    @property
    def image(self):
        """Synonym to enable mixing with ``pygame.sprite.Sprite``
        """
        return self.surface

    def convert_ip(self, *conver_args, **conver_kwa):
        self.__surface = self.__surface.convert(*conver_args, **conver_kwa)

    def convert_alpha_ip(self, *convert_args, **convert_kwa):
        self.__surface = self.__surface.convert_alpha(*convert_args,
                                                      **convert_kwa)

    def transform_ip(self, xform_func, *xform_args, **xform_kwa):
        self.__surface = xform_func(self.__surface, *xform_args, **xform_kwa)


class MSurfaceRect(MSurface, MRect):
    def __init__(self, *surface_args, surface_factory=None, **rect_kwa):
        MSurface.__init__(self, *surface_args,
                               surface_factory=surface_factory)
        self.rect_set_surface(**rect_kwa)

    def rect_set_surface(self, **rect_kwa):
        MRect.__init__(self, self.surface.get_rect(**rect_kwa))

    def transform_ip(self, xform_func, *xform_args, **xform_kwa):
        old_rect = self.surface.get_rect().center
        MSurface.transform_ip(self, xform_func, *xform_args, **xform_kwa)
        self.rect_set_surface(center=old_rect.center)


class ESprite(pygame.sprite.Sprite, MIdentity, MSurfaceRect):
    def __init__(self, *surface_args, surface_factory=None,
                 sprite_groups=(), collide_func=pygame.sprite.collide_rect,
                 **surface_rect_kwa):
        pygame.sprite.Sprite.__init__(self, *sprite_groups)
        MIdentity.__init__(self)
        MSurfaceRect.__init__(self, *surface_args,
                                  surface_factory=surface_factory,
                                  **surface_rect_kwa)
        self.__collide_func = collide_func

    @property
    def collide_func(self):
        return self.__collide_func

    def group_clear(self, surface, rect):
        # TODO: Keep an eye on this function. may not work in all cases...
        surface.blit(self.image, rect, area=rect.move(
            *vect_diff(surface.get_rect().topleft, self.rect.topleft)))


class EDirtySprite(pygame.sprite.DirtySprite, MIdentity, MSurfaceRect):
    def __init__(self, *surface_args, surface_factory=None,
                 sprite_groups=(), **surface_rect_kwa):
        pygame.sprite.DirtySprite.__init__(self, *sprite_groups)
        MIdentity.__init__(self)
        MSurfaceRect.__init__(self, *surface_args,
                                  surface_factory=surface_factory,
                                  **surface_rect_kwa)


# TODO: Good start but doesn't handle some irregular but useful arg combos.
class MAnimated:
    def __init__(self, count=0, interval=1.0, start=0,
                 end=0, autostart=True,
                 animation_factory=lambda: AnimationLoop()):
        """Mixin for animated Entity classes. The ``frame_index``
        property can be used

        :param int count:
        :param float interval:
        :param int start:
        :param int end:
        :param bool autostart:
        :param func animation_factory:
        :return:
        """

        self.__start = self.__index = start
        self.__interval = interval
        self.__count = count
        self.__end = end > 0 and end or (count - 1)
        self.__animation_obj = animation_factory()

        if autostart:
            self.__animation_obj.start()

    #Value props
    @property
    def start(self):
        return self.__start

    @property
    def end(self):
        return self.__end

    @property
    def count(self):
        return self.__count

    @property
    def playing_count(self):
        return abs(
                (self.end - self.start + 1) / self.interval)

    @property
    def interval(self):
        return self.__interval

    @property
    def index(self):
        return self.__index

    #Transport props
    @property
    def at_start(self):
        return self.index <= self.start

    @property
    def at_end(self):
        return self.index >= self.end

    @property
    def is_reversed(self):
        return self.interval < 0

    @property
    def is_forward(self):
        return self.interval > 0

    # Transport methods
    def advance(self):
        self.__index += self.interval
        self.__index %= self.count

    def flip(self):
        self.__interval = -self.interval

    def reverse(self):
        self.__interval = -abs(self.interval)

    def forward(self):
        self.__interval = abs(self.interval)

    def rewind(self):
        self.__index = self.__start

    def fast_forward(self):
        self.__index = self.__end

    # Loop Method
    def update(self):
        self.__animation_obj.update(self)