from collections import OrderedDict


class OrderedDefaultDict(OrderedDict):
    """Simplest OrderedDict and ``defaultdict``-like functionality.
    """
    def __init__(self, factory, *args, **kwa):
        OrderedDict.__init__(self, *args, **kwa)
        self.__factory = callable(factory) and factory or (lambda: factory)

    def __missing__(self, key):
        self[key] = self.__factory()
        return self[key]