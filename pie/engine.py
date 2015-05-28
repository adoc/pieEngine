"""
Game Engine.
"""

import pygame

from pie import MRunnable, MIdentity

from pie.clock import RateClock

from pie.entity.group import OrderedEntities
from pie.entity.background import BackgroundFill
from pie.asset import AssetHandler
from pie.event import DragHandler, EventHandler
from pie.math import vect_diff
from pie.util import fallback_factory
from pie.render import Renderer

__all__ = ("Engine",)


class Engine(MIdentity, MRunnable):
    """Game enging base class. Any game implementations will subclass
    from this.
    """

    def __init__(self, screen=None, init_pygame=True, clock_factory=None,
                 debug=False, background_factory=None,
                 render_group_factory=None,
                 static_background=True, auto_start=False):
        """

        :param pygame.Surface: Pygame screen this ``Engine`` is rendering to.
        :param pygame.time.Clock clock: Pygame ``Clock`` instance to throttle the engine.
        :param int target_fps:
        :param BackGround background: ``Background`` instance
        :return:
        """
        MRunnable.__init__(self, auto_start=auto_start)
        MIdentity.__init__(self)

        if init_pygame:
            pygame.init()

        self.__debug = debug

        self.__screen = (isinstance(screen, pygame.Surface) and screen or
                                    fallback_factory(screen,
                                         self.__default_screen_factory)())

        self.__clock = (fallback_factory(clock_factory,
                                         lambda: RateClock(2000,
                                                    accurate=False))())

        self.__background = (fallback_factory(background_factory,
                                        self.__default_bg_surface_factory)())

        # Reference to the iterator of sprites to be blitted.
        self.__render_group = fallback_factory(render_group_factory,
                                               OrderedEntities)()
        self.__update_group = []

        self.__renderer = Renderer(self.__screen, self.__background,
                                   self.__render_group,
                                   static_background=static_background)

        # Set up subsystems.
        self.__assets = AssetHandler(self.__screen)
        self.__events = EventHandler()
        self.__drag_handler = DragHandler(self.events)

        # Bind events.
        self.__events.bind(pygame.QUIT, self.__ev_quit)
        self.__events.bind(pygame.VIDEORESIZE, self.__ev_resize)

        self.__end_state = True

    def __ev_quit(self, _):
        self.__end_state = False
        self.stop()

    @staticmethod
    def __default_screen_factory():
        info = pygame.display.Info()
        return pygame.display.set_mode((info.current_w // 2,
                                        info.current_h // 2))

    def __default_bg_surface_factory(self):
        return BackgroundFill(self.__screen.copy())

    def __ev_resize(self, event):
        """Resize the display screen and...

        :param event:
        :param _:
        :return:
        """

        new_size = event.dict['size']
        surface_size = self.__screen.get_size()
        old_center = self.__screen.get_rect().center
        if new_size != surface_size:
            self.__screen = pygame.display.set_mode(new_size,
                                                    self.__screen.get_flags(),
                                                    self.__screen.get_bitsize())
            self.init(offset=vect_diff(self.__screen.get_rect().center,
                                       old_center))
        self.__screen_width, self.__screen_height = self.__screen.get_size()

    @property
    def assets(self):
        return self.__assets

    @property
    def events(self):
        return self.__events

    @property
    def drag_handler(self):
        return self.__drag_handler

    @property
    def screen_width(self):
        return self.__screen_width

    @property
    def screen_height(self):
        return self.__screen_height

    @property
    def fps(self):
        return self.__clock.framerate

    def init(self, offset=None):
        """
        """
        self.__renderer.init(offset=offset)

    def add_render_plain(self, *entities):
        # The entities, by way of :mod:`pygame`, will break out the contained
        # sprites.
        self.__render_group.add(*entities)
        for entity in entities:
            self.__update_group.append(entity) # This is to track the
                                               # actual groups being
                                               # added.

    def update(self, *args):
        """
        """
        # print(len(self.__render_group))
        self.events.update()
        self.drag_handler.update()

        for entity in self.__update_group:
            entity.update(*args)

    def throttle(self):
        """
        """
        return self.__clock.tick()

    def clear(self):
        """
        """
        self.__renderer.clear()

    def render(self):
        """
        """
        self.__renderer.render()

    def start(self):
        """
        """
        MRunnable.start(self)

        self.init()

        while not self.stopped:
            self.update()
            self.clear()
            self.throttle()
            self.render()

        return self.__end_state