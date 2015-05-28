"""Entity Abstract classes. Generally not implemented by the user.
"""

#TODO: Review for 0.1.2

import numpy
import pygame
import pygame.math

from pie.math import vect_diff

__all__ = ('MRect',
           'MViewport',
           'MSurface',
           'MSurfarray',
           'MSurfaceRect',
           'MSurfarrayRect',
           'MSprite')


class MRect:
    """Entity mixin for a :class:`pygame.Rect` object.

    Provides a :data:`rect` property. Also provides in place rect
    transforms.
    """

    # TODO: Move parallax_distance to MViewport??
    def __init__(self, *rect_args, normalize=False):
        """Reset the ``Rect`` object for this Entity.

        :param *rect_args: passed directly to a `pygame.Rect`_
            constructor.
        :param bool normalize: Normalize the :data:`rect` on
            instantiation.
        :param float parallax_distance: The relative Z coordinate
            distance for use in parallax calculations.
        """
        self.__rect = (rect_args and pygame.Rect(*rect_args) or
                       pygame.Rect((0, 0), (0, 0)))

        if normalize:
            self.__rect.normalize()

    @property
    def rect(self):
        """This entity's rectangle.

        :rtype: `pygame.Rect`_
        """
        #self.__rect = self.__rect.clip(pygame.display.get_surface().get_rect())
        return self.__rect


class MViewport:
    """
    """

    def __init__(self, *rect_args, parallax_distance=0.0):
        self.__viewport = (rect_args and pygame.Rect(*rect_args) or
                           pygame.Rect((0, 0), (0, 0)))
        self.__old_viewport = self.__viewport.copy()
        self.__parallax_distance = parallax_distance

    @property
    def viewport(self):
        """This entity's *viewport* `pygame.Rect`_.

        :rtype: `pygame.Rect`_
        """
        #self.__viewport = self.__viewport.clip(pygame.display.get_surface().get_rect())
        return self.__viewport

    @property
    def parallax_distance(self):
        """This entity's parallax_distance.

        :rtype: float
        """
        return self.__parallax_distance

    @property
    def viewport_changed(self):
        """True if the :data:`viewport` has changed since the last
        :meth:`update`.

        :rtype: bool
        """
        return self.__old_viewport != self.__viewport

    def update(self, *args):
        """Snapshot the current :data:`viewport`. This is used to
        update the :data:`viewport_changed` property.
        """

        self.__old_viewport = self.__viewport.copy()


class MSurface:
    """Entity mixin for a `pygame.Surface`_ object. Provides a
    :data:`surface` property.

    Also provides in-place surface transforms.
    """

    def __init__(self, *surface_args, convert=False, alpha=False,
                 blit_flags=0):
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

        if surface_args and isinstance(surface_args[0], pygame.Surface):
            self.__surface = surface_args[0]
        elif surface_args:
            self.__surface = pygame.Surface(*surface_args)
        else:
            self.__surface = pygame.display.get_surface().copy()

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
    def blit_flags(self):
        """The flags used when rendering this entity.

        :rtype: int
        """

        return self.__blit_flags

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

    # TODO: Move to MSurfaceRect
    def blit_to(self, surface):
        return surface.blit(self.image, self.rect, self.viewport,
                            special_flags=self.blit_flags)


class MSurfarray:
    def __init__(self, surface, blit_flags=0):
        self.__surfarray = pygame.surfarray.array2d(surface)
        self.__orig_surfarray = numpy.copy(self.__surfarray)
        self.__blit_flags = blit_flags

    @property
    def surfarray(self):
        return self.__surfarray

    @property
    def shape(self):
        return self.__surfarray.shape

    # numpy.roll is slow, at least when used twice...
    def offset(self, offset):
        # Roll original array along the x
        size_y, size_x = self.shape
        arr = numpy.roll(self.__orig_surfarray, offset[1] % size_x, 1)
        arr = numpy.roll(arr, offset[0] % size_y, 0)
        self.__surfarray = arr

    def blit_to(self, surface):
        max_size_x, max_size_y = surface.get_rect().size
        return pygame.surfarray.blit_array(surface,
                                           self.__surfarray[:max_size_x,
                                                            :max_size_y])


class MSurfaceRect(MRect, MSurface):
    """Entity mixin combining :class:`MRect` and :class:`MSurface`.
    """

    def __init__(self, *surface_args, convert=False,
                 alpha=False, blit_flags=0, normalize=False, **rect_pos):
        """The :data:`rect` property will be set to the :data:`surface`
        rect and passed any *rect_pos* keyword args to adjust the rect.
        """
        MSurface.__init__(self, *surface_args,
                          convert=convert, alpha=alpha, blit_flags=blit_flags)
        MRect.__init__(self, self.surface.get_rect(**rect_pos),
                       normalize=normalize)


class MSurfarrayRect(MRect, MSurfarray):
    """Entity mixin combining :class:`MRect` and :class:`MSurfarray`.
    """

    def __init__(self, surface, normalize=False, **rect_pos):
        """The :data:`rect` property will be set to the :data:`surface`
        rect and passed any *rect_pos* keyword args to adjust the rect.
        """
        MSurfarray.__init__(self, surface)
        MRect.__init__(self, (0, 0), self.shape[:2],
                       normalize=normalize)
        for k, v in rect_pos.items():
            setattr(self.rect, k, v)


class MSprite(pygame.sprite.Sprite):
    """Entity mixin for `pygame.Sprite`_ that provides
    :data:`collide_func` property and meth:`group_clear` methods.
    """

    def __init__(self, sprite_groups=(),
                 collide_func=None):
        """Initialize MSprite.

        :param tuple sprite_groups=():
        :param function collide_func: The collision determination
            function. Defaults to pygame.sprite.collide_rect
        """
        pygame.sprite.Sprite.__init__(self, *sprite_groups)
        self.__collide_func = collide_func or pygame.sprite.collide_rect
        self.visible = True

    @property
    def collide_func(self):
        """Returns the collide function.

        :return: The function to determine collisions with this Sprite.
        """

        return self.__collide_func

    # TODO: Move to SpriteSurface??
    def group_clear(self, surface, rect):
        """Used as callback for ``pygame.sprite.Group().clear`` in the
        Engine Renderer.

        :param `pygame.Surface`_ surface: The surface to be partially cleared.
        :param `pygame.Rect`_ rect: The rect area to be cleared.
        """

        # Keep an eye on this function. may not work in all cases...
        # TODO: Check if in any way related to viewport or if viewport can be used.
        surface.blit(self.image, rect, area=rect.move(
            *vect_diff(surface.get_rect().topleft, self.rect.topleft)))


class MText:
    def __init__(self, family="helvetica"):
        pass