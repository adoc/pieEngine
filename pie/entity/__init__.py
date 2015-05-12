# Might be a bit of overkill but heart is in the right place and
# implementations have seemed clean.
#
# Maybe a little better now!

import uuid

import pygame
import pygame.math

from pie.math import vect_diff


__all__ = ('MIdentity',
           'MRect',
           'MSurface',
           'MSprite')


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

    def __init__(self, **kwa):
        """Base parent class for all Entities. Provides an ordinal
        ``ord`` and unique identifier ``id``. Default uses module-level
        counter for the ordinal and UUID4 for the id. Either can be
        overridden by passing an ``ord_factory`` and/or ``id_factory``
        keyword argument.

        :param ord_factory:
        :param id_factory:

        :return:


        """
        self.__ord = kwa.pop('ord_factory', next_entity_ord)
        self.__id = kwa.pop('id_factory', uuid.uuid4)

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


class MRect:
    """Entity mixin for a ``pygame.Rect`` object.

    Provides a ``rect`` property. Also provides in place rect transforms.
    """

    def __init__(self, *args, **kwa):
        """Reset the ``Rect`` object for this Entity.

        :param *rect_args: passed directly to a ``pygame.Rect``
            constructor
        :param rect_factory: Rect factory function. This takes
            precedence over ``*rect_args``
        """
        self.__rect = pygame.Rect(*args)

        if kwa.pop('normalize', False):
            self.__rect.normalize()

        self.parallax_offset = 1.0

    @property
    def rect(self):
        """Property returning this Entity's rect.
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


# TODO: Look for relations and differences between .viewport and .rect as implementations are fleshed out.
class MSurface:
    """
    """

    def __init__(self, *surface_args, **kwa):

        """Entity mixin for a ``pygame.Surface`` object.

        Provides a ``surface`` property. Most importantly, provides a
        ``viewport`` property that represents an area of the surface that is
        blitted.

        Also provides in place surface transforms.

        If only one argument is passed and it is a ``pygame.Surface`` then we set this surface to that object. Otherwise, we check for a ``surface_factory`` and finally attempt to create a ``pygame.Surface`` using the ``*surface_args``.

        :param surface_args[0]:
        :param surface_args[]:
        :param viewport=None:
        :param convert=True:
        :param blit_flags=0:
        :param surface_factory=None:
        """

        viewport = kwa.pop('viewport', None)
        convert = kwa.pop('convert', False)
        alpha = kwa.pop('alpha', False)
        blit_flags = kwa.pop('blit_flags', 0)
        if surface_args and isinstance(surface_args[0], pygame.Surface):
            self.__surface = surface_args[0]
        else:
            self.__surface = pygame.Surface(*surface_args)

        self.__viewport = viewport or self.__surface.get_rect()
        self.__old_viewport = self.__viewport.copy()
        self.__blit_flags = blit_flags

        if convert:
            if alpha:
                self.convert_alpha_ip()
            else:
                self.convert_ip()

    @property
    def surface(self):
        """Property returning this surface.
        """

        return self.__surface

    @property
    def image(self):
        """Property synonym of this surface to enable mixing with
        deeper ``pygame.sprite`` APIs.
        """

        return self.surface # Using non-private is intentional here.

    @property
    def viewport(self):
        return self.__viewport

    @property
    def viewport_changed(self):
        return self.__old_viewport != self.__viewport

    @property
    def blit_flags(self):
        return self.__blit_flags

    def blit_view(self, dest_surface, dest):
        dest_surface.blit(self.image, dest, self.viewport,
                          special_flags=self.blit_flags)

    def convert_ip(self, *convert_args, **convert_kwa):
        """Convert this surface using ``pygame.Surface.convert`` API.
        http://www.pygame.org/docs/ref/surface.html#pygame.Surface.convert

        :param convert_args:
        :param convert_kwa:
        :return:
        """

        self.__surface = self.surface.convert(*convert_args, **convert_kwa)

    def convert_alpha_ip(self, *convert_args, **convert_kwa):
        """Convert this surface using ``pygame.Surface.convert_alpha``
        API.
        http://www.pygame.org/docs/ref/surface.html#pygame.Surface.convert_alpha

        :param convert_args:
        :param convert_kwa:
        :return:
        """

        self.__surface = self.surface.convert_alpha(*convert_args,
                                                    **convert_kwa)

    def transform_ip(self, xform_func, *xform_args, **xform_kwa):
        """Use the ``pygame.transform`` API on this surface.
        http://www.pygame.org/docs/ref/transform.html

        :param xform_func:
        :param xform_args:
        :param xform_kwa:
        :return:
        """
        old_view_center = self.__viewport.center
        self.__surface = xform_func(self.surface, *xform_args, **xform_kwa)
        self.__viewport = self.surface.get_rect(center=old_view_center)

    def update(self):
        self.__old_viewport = self.__viewport.copy()


class MSurfaceRect(MSurface, MRect):
    def __init__(self, *surface_args, rect_kwa={}, **kwa):
        MSurface.__init__(self, *surface_args, **kwa)
        MRect.__init__(self, self.surface.get_rect(**rect_kwa), **kwa)


class MSprite(pygame.sprite.Sprite):
    """MSprite mixin class provides abstract ``collide_func`` prop and
    ``group_clear`` method.
    """

    def __init__(self, **kwa):
        """Initialize MSprite.

        :param collide_func: The collision determination function.
        :return:
        """
        pygame.sprite.Sprite.__init__(self, *kwa.pop('sprite_groups', ()))
        self.__collide_func = kwa.pop('collide_func',
                                      pygame.sprite.collide_rect)

    @property
    def collide_func(self):
        """Returns the collide function.

        :return: The function to determine collisions with this Sprite.
        """

        return self.__collide_func

    def group_clear(self, surface, rect):
        """Used ass callback for ``pygame.sprite.Group().clear`` in the
        Engine Renderer.

        :param surface: The surface to be partially cleared.
        :param rect: The rect area to be cleared.
        """

        # TODO: Keep an eye on this function. may not work in all cases...
        # TODO: Check if in any way related to viewport or if viewport can be used.
        surface.blit(self.image, rect, area=rect.move(
            *vect_diff(surface.get_rect().topleft, self.rect.topleft)))