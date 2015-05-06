"""Base classes in use by the modules. Rarely, if ever will the user
developer need to interact with these classes.
"""

__all__ = ("MRunnable",)


class MRunnable:
    """Provides a runnable mixin to subclasses.
    """

    def __init__(self, auto_start=False):
        """Initialize an MRunnable object.

        :param auto_start: True to automatically set the state to running.
        """
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

        :return bool: Running state is True.
        """
        return self.__running

    @property
    def stopped(self):
        """Stopped (or not running) state.

        :return bool: Stopped state is True.
        """
        return not self.__running