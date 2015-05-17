"""Utility classes and functions.
"""

from collections import OrderedDict

__all__ = ('fallback_factory', 'OrderedDefaultDict')


def fallback_factory(*factories):
    """Return the first of *factories* that is valid callable
    function.

    :param *factories: Argument list of potential factory functions.
    :return function: Factory function.
    """
    for factory in factories:
        if factory and callable(factory):
            return factory


class OrderedDefaultDict(OrderedDict):
    """Simple class that provides an OrderedDict and
    ``defaultdict``-like functionality.
    """
    def __init__(self, factory, *args, **kwa):
        OrderedDict.__init__(self, *args, **kwa)
        self.__factory = callable(factory) and factory or (lambda: factory)

    def __missing__(self, key):
        self[key] = self.__factory()
        return self[key]