from collections import OrderedDict


__all__ = ('fallback_factories', 'OrderedDefaultDict')


def fallback_factory(*factories, factory_args=(), factory_kwa={}):
    for factory in factories:
        if factory:
            return factory(*factory_args, **factory_kwa)


class OrderedDefaultDict(OrderedDict):
    """Simplest OrderedDict and ``defaultdict``-like functionality.
    """
    def __init__(self, factory, *args, **kwa):
        OrderedDict.__init__(self, *args, **kwa)
        self.__factory = callable(factory) and factory or (lambda: factory)

    def __missing__(self, key):
        self[key] = self.__factory()
        return self[key]