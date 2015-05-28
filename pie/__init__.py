"""pieEngine - Pygame Prototyping Engine


* You'll find that much of the code is done in ways that might not be
considered pythonic; e.g. the usage of private instance variables and
flat getters/settings. The goal for the author is to hopefully allow
these pieces to be more easily ported to strict, verbose and faster
languages like Java/libGDX or C#/Unity.
"""
import uuid

__author__ = 'Nick Long (https://nicklong.io/craft)'
__url__ = "https://github.com/adoc/pieEngine"

import logging
log = logging.getLogger(__name__)


try:
    import pygame
except ImportError:
    log.error("Pygame could not load, it is a hard dependency of pieEngine.")
    raise


try:
    import numpy
except ImportError:
    log.warning("Numpy could not load, some functionality in pieEngine will be "
                "disabled.")
else:
    pygame.surfarray.use_arraytype('numpy')


__all__ = ('MIdentity', 'MRunnable')


__identity_ord = 0


def _reset_entity_ord(confirm=False):
    """Testing purposes only.

    :param bool confirm: Confirm that we know what we're doing.
    """
    global __identity_ord
    if confirm:
        __identity_ord = 0


def _next_entity_ord():
    """Increment the singleton entity ordinal and return it.
    *Note: This is not multi-process safe but should be thread safe.*
    :rtype:int
    :return: Next entity ordinal.
    """
    global __identity_ord
    __identity_ord += 1
    return __identity_ord


class MIdentity:
    """Base parent class for all Entities. Provides an ordinal
    :data:`ord` and unique identifier :attr:`id`. Default uses
    runtime module-level counter for the ordinal and UUID4 for the
    id.
    """

    def __init__(self, ord_factory=None, id_factory=None):
        """Either default can be overridden by passing an
        `ord_factory` and/or `id_factory` keyword argument.

        :param function ord_factory: Ordinal factory Defaults to
            :func:`next_entity_ord`.
        :param function id_factory: ID factory Defaults to
            :func:`uuid.uuid4`.
        """

        self.__ord = ord_factory and ord_factory() or _next_entity_ord()
        self.__id = id_factory and id_factory() or uuid.uuid4()

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


class MRunnable:
    """Provides a "runnable" mixin to subclasses.

    :param bool auto_start: True to automatically set the state to running.
    """

    def __init__(self, auto_start=False):
        #: Initialize an MRunnable object.
        self.__running = auto_start

    def start(self):
        """Set the running state to true (running).
        """
        self.__running = True

    def stop(self):
        """Set the running state to false (stopped).
        """
        self.__running = False

    @property
    def running(self):
        """Running state.

        :rtype bool:
        :return: Running state is True.
        """
        return self.__running

    @property
    def stopped(self):
        """Stopped (or not running) state.

        :rtype bool:
        :return: Stopped state is True.
        """
        return not self.__running