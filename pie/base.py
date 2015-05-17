"""Base classes in use by the modules.

Rarely, if ever will the user need to interact with these classes.
"""

__all__ = ("MRunnable",)


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