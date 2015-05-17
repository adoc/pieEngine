"""Entities base classes.
"""
# Might be a bit of overkill but heart is in the right place and
# implementations have seemed clean.
#
# Maybe a little better now!

import uuid

import pygame
import pygame.math

# TODO: Check this usage and see if we can remove it from pie.math.
from pie.math import vect_diff


__all__ = ('next_entity_ord',
           'MIdentity',
           'MRect',
           'MSurface',
           'MSurfaceRect',
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
    """Base parent class for all Entities. Provides an ordinal
    :data:`ord` and unique identifier :attr:`id`. Default uses
    runtime module-level counter for the ordinal and UUID4 for the
    id.
    """

    def __init__(self, **kwa):
        """Either default can be overridden by passing an
        `ord_factory` and/or `id_factory` keyword argument.

        :param function ord_factory: Ordinal factory Defaults to
            :func:`next_entity_ord`.
        :param function id_factory: ID factory Defaults to
            :func:`uuid.uuid4`.
        """

        self.__ord = kwa.pop('ord_factory', next_entity_ord)
        self.__id = kwa.pop('id_factory', uuid.uuid4)

    @property
    def ord(self):
        """Return the ordinal of this :mod:`entity`. By default this
        is an integer.

        :rtype: int
        :return: Runtime or global (if user handled) Ordinal of this
            entity.
        """
        return self.__ord

    @property
    def id(self):
        """Return the unique identifier of this :mod:`entity`. By
        default is a :class:`uuid.UUID`.

        :rtype: object
        :return: By default a UUID object unique ident.
        """
        return self.__id


class MRect:
    """Entity mixin for a `pygame.Rect`_ object.

    Provides a :data:`rect` property. Also provides in place rect
    transforms.
    """

    def __init__(self, *rect_args, **kwa):
        """Reset the ``Rect`` object for this Entity.

        :param *rect_args: passed directly to a `pygame.Rect`_
            constructor.
        :param bool normalize: Normalize the :data:`rect` on
            instantiation.
        :param float parallax_distance: The relative Z coordinate
            distance for use in parallax calculations.
        """
        self.__rect = pygame.Rect(*rect_args)

        if kwa.pop('normalize', False):
            self.__rect.normalize()

        self.__parallax_distance = kwa.pop('parallax_distance', 1.0)

    @property
    def rect(self):
        """This entity's rectangle.

        :rtype: :class:`pygame.Rect`
        """
        return self.__rect

    @property
    def parallax_distance(self):
        """This entity's parallax_distance.

        :rtype: float
        """
        return self.__parallax_distance

    def move_ip(self, x, y):
        """Moves this entity's :data:`rect`

        :param int x: Horizontal offset to move the :data:`rect`.
        :param int y: Vertical offset to move the :data:`rect`.
        """
        self.__rect = self.__rect.move(x, y)

    def inflate_ip(self, x, y):
        """Inflate or shrink this entity's :data:`rect`. The :data:`rect`
        remains centered.

        :param int x: Horizontal offset to size the :data:`rect`.
        :param int y: Vertical offset to size the :data:`rect`.
        """
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
    """Entity mixin for a `pygame.Surface`_ object. Provides a
    :data:`surface` property and a :data:`viewport` property that
    represents an area of the surface that is rendered.

    Also provides in place surface transforms.
    """

    def __init__(self, *surface_args, **kwa):
        """If only one argument is passed and it is a
        `pygame.Surface`_ then we set this :data:`surface` to that
        object.

        :param pygame.Surface surface_args[0]: Reference to
            a `pygame.Surface`_ that will be used for this entity.
        :param *surface_args: If no surface is passed, these args
            are passed to `pygame.Surface`_ to create the surface
            for this entity.
        :param pygame.Rect viewport=None: Reference to
            a `pygame.Rect`_ object representing the current
            :data:`viewport` and area of the :data:`surface` to be
            rendered.
        :param bool alpha=False: The :data:`surface` has an alpha
            color channel. (This does nothing unless ``convert=True``
        :param bool convert=False: Convert the :data:`surface` to
            optimized for rendering. (Uses `pygame.Surface.convert`_
            or `pygame.Surface.convert_alpha`_ based on *alpha*
            keyword argument.)
        :param int blit_flags=0: The flags to be used when rendering
            this :data:`surface`. (e.g. :class:`pygame.BLEND_RGBA_ADD`)
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
        """This entity's `pygame.Surface`_ object.

        :rtype: `pygame.Surface`_
        """

        return self.__surface

    @property
    def image(self):
        """Synonym of this :data:`surface` to enable mixing with
        deeper `pygame.sprite`_ APIs.

        :rtype: `pygame.Surface`_
        """
        return self.surface # Using non-private is intentional here.

    @property
    def viewport(self):
        """This entity's *viewport* `pygame.Rect`_.

        :rtype: `pygame.Rect`_
        """

        return self.__viewport

    @property
    def viewport_changed(self):
        """True if the :data:`viewport` has changed since the last
        :meth:`update`.

        :rtype: bool
        """
        return self.__old_viewport != self.__viewport

    @property
    def blit_flags(self):
        """The flags used when rendering this entity.

        :rtype: int
        """

        return self.__blit_flags

    # TODO: Deprecated but good reference.
    def blit_view(self, dest_surface, dest):
        dest_surface.blit(self.image, dest, self.viewport,
                          special_flags=self.blit_flags)

    def convert_ip(self, *convert_args, **convert_kwa):
        """Convert this surface using `pygame.Surface.convert`_ API.

        :param *convert_args: Arguments to be passed to the
            :data:`surface` convert.
        :param **convert_kwa: Keyword arguments passed to the
            :data:`surface` convert.
        """

        self.__surface = self.surface.convert(*convert_args, **convert_kwa)

    def convert_alpha_ip(self, *convert_args, **convert_kwa):
        """Convert this surface using `pygame.Surface.convert_alpha`_
        API.

        :param *convert_args: Arguments to be passed to the
            :data:`surface` convert.
        :param **convert_kwa: Keyword arguments passed to the
            :data:`surface` convert.
        """

        self.__surface = self.surface.convert_alpha(*convert_args,
                                                    **convert_kwa)

    def transform_ip(self, xform_func, *xform_args, **xform_kwa):
        """Use the *xform_func* API on this :data:`surface`.

        :param `pygame.transform`_ xform_func: Transform function.
        :param *xform_args: Arguments passed to transform function.
        :param **xform_kwa: Keyword arguments passed to transform
            function.
        """
        self.__surface = xform_func(self.surface, *xform_args, **xform_kwa)

    def update(self):
        """
        """

        self.__old_viewport = self.__viewport.copy()


class MSurfaceRect(MSurface, MRect):
    def __init__(self, *surface_args, rect_kwa={}, **kwa):
        MSurface.__init__(self, *surface_args, **kwa)
        MRect.__init__(self, self.surface.get_rect(**rect_kwa), **kwa)

    @property
    def flip_rect(self):
        """Flipped rectangle coordinates for use in pymunk.

        :return:
        """
        nr = self.rect.copy()
        nr.top = self.surface.get_height() - nr.top
        return nr


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