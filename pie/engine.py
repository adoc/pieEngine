"""
Game Engine.
"""

import pygame.sprite

import pie._pygame.sprite
from pie.base import MRunnable
from pie.entity import MIdentity
from pie.entity.background import BackgroundFill
from pie.asset import AssetHandler
from pie.event import DragHandler, EventHandler
from pie.math import vect_diff
from pie.util import fallback_factory


__all__ = ("FpsClock", "Renderer", "Engine")


class FpsClock:
    def __init__(self, target_fps, accurate=True):
        self.__clock = pygame.time.Clock()
        self.__target_fps = target_fps
        if accurate:
            self.tick = self.__tick_busy_loop

    def tick(self):
        return self.__tick()

    def __tick(self):
        return self.__clock.tick(self.__target_fps)

    def __tick_busy_loop(self):
        return self.__clock.tick_busy_loop(self.__target_fps)

    def get_time(self):
        return self.__clock.get_time()

    def get_rawtime(self):
        return self.__clock.get_rawtime()

    def get_fps(self):
        return self.__clock.get_fps()


# TODO: Refactoring [#3]
class Renderer:
    """
    """
    def __init__(self, screen, background, group,
                 non_static_background=False):
        self.__screen = screen

        self.__background = background # How do we handle backgrounds?? [#3]
        self.__group = group # Does this stay a group of sprites only? [#3]
        # Do we add the "list of groups" abstract here? [#3]

        if non_static_background:
            self.render = self.__render_non_static
            self.clear = self.__clear_non_static
        else:
            self.render = self.__render_static
            self.clear = self.__clear_static

    def __clear_static(self):
        self.__group.clear(self.__screen, self.__background.group_clear)

    def __clear_non_static(self):
        self.__screen.blit(self.__background.image, self.__background.rect)

    def __render_static(self):
        pygame.display.update(self.__group.draw(self.__screen))

    def __render_non_static(self):
        self.__group.draw(self.__screen)
        pygame.display.flip()

    def init(self, offset=None):
        if offset:
            self.__background.move_ip(*offset)
            for sprite in self.__group:
                sprite.move_ip(*offset)

        self.__clear_non_static()
        self.__render_non_static()
        pygame.display.flip()


class Engine(MRunnable, MIdentity):
    """Game enging base class. Any game implementations will subclass
    from this.
    """

    def __init__(self, screen, clock_factory=None,
                 clock_accurate=False, target_fps=60,
                 debug=False, background_factory=None,
                 render_group_factory=None,
                 non_static_background=False, auto_start=True):
        """

        :param pygame.Surface: Pygame screen this ``Engine`` is rendering to.
        :param pygame.time.Clock clock: Pygame ``Clock`` instance to throttle the engine.
        :param int target_fps:
        :param BackGround background: ``Background`` instance
        :return:
        """
        MRunnable.__init__(self, auto_start=auto_start)
        MIdentity.__init__(self)

        self.__debug = debug
        self.__target_fps = target_fps

        self.__screen = (isinstance(screen, pygame.Surface) and screen or
                                    fallback_factory(screen,
                                         self.__default_screen_factory))

        self.__clock = fallback_factory(clock_factory,
                                        lambda: FpsClock(target_fps,
                                                    accurate=clock_accurate))

        self.__background = fallback_factory(background_factory,
                                        self.__default_bg_surface_factory)

        self.__render_group = fallback_factory(render_group_factory,
                                               pie._pygame.sprite.OrderedUpdates)
        self.__update_group = []

        self.__renderer = Renderer(self.__screen, self.__background,
                                   self.__render_group,
                                   non_static_background=non_static_background)

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

    def init(self, offset=None):
        """
        """
        self.__renderer.init(offset=offset)

    def add_render_plain(self, *entities):
        # This by way of pygame will break out the contained sprites.
        self.__render_group.add(*entities)
        for entity in entities:
            self.__update_group.append(entity) # This is to track the actual groups being added.

    def update(self):
        """
        """
        self.events.update()
        self.drag_handler.update()

        for entity in self.__update_group:
            entity.update()

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