"""
Game Engine.
"""

import pygame.sprite

from pie.base import MRunnable
from pie.entity import BaseEntity
from pie.asset import AssetHandler
from pie.event import DragHandler, EventHandler, MouseState
from pie.entity import FillSurfaceEntity
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


class Renderer:
    """
    """
    def __init__(self, screen, background, group, non_static_background=False):
        self.__screen = screen
        self.__background = background
        self.__group = group

        if non_static_background:
            self.render = self.__render_non_static

    def __render_static(self):
        # Clear the dirty rects using Entity callback.
        self.__group.clear(self.__screen, self.__background.group_clear)
        pygame.display.update(
                self.__group.draw(
                    self.__screen))

    def __render_non_static(self):
        self.__screen.blit(self.__background.image, self.__background.rect)
        self.__group.draw(self.__screen)
        pygame.display.flip()

    def init(self):
        self.__screen.blit(self.__background.image, self.__background.rect)
        pygame.display.flip()

    def render(self):
        return self.__render_static()



        # self._debug_font = pygame.font.Font(None, 18)
        # self._debug_pos = (8, 8)
        # self._debug_lines = []


    # # TODO: Refactor in to debug mixin.
    # def draw_debug(self, tick_time=0):
    #     self.__debug_surface.image.fill((0,0,0))
    #     for n, line in enumerate(reversed(self._debug_lines)):
    #         pos = list(self._debug_pos)
    #         pos[1] = n * self._debug_font.get_linesize() + self._debug_pos[1]
    #         self.__debug_surface.image.blit(
    #             self._debug_font.render(*line),
    #             pos)
    #     if tick_time:
    #         pos[1] += self._debug_font.get_linesize() + self._debug_pos[1]
    #         self.__debug_surface.image.blit(
    #             self._debug_font.render("Tick: %.4f" % tick_time, 1, (240, 240, 240)),
    #             pos
    #         )
    #     self._debug_lines = []

        # self._debug_lines.append(("FPS: %s" % (self.__clock.get_fps()), 1, (240, 240, 240)))





# TODO: Abstract out debug.
class Engine(BaseEntity, MRunnable):
    """Game enging base class. Any game implementations will subclass
    from this.
    """

    def __init__(self, screen_factory=None, clock_factory=None,
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
        BaseEntity.__init__(self)
        MRunnable.__init__(self, auto_start=auto_start)

        self.__debug = debug
        self.__target_fps = target_fps

        self.__screen = fallback_factory(screen_factory,
                                         self.__default_screen_factory)

        self.__clock = fallback_factory(clock_factory,
                                        lambda: FpsClock(target_fps,
                                                    accurate=clock_accurate))

        self.__background = fallback_factory(background_factory,
                                        self.__default_bg_surface_factory)

        self.__render_group = fallback_factory(render_group_factory,
                                               pygame.sprite.RenderUpdates)

        self.__renderer = Renderer(self.__screen, self.__background,
                                   self.__render_group,
                                   non_static_background=non_static_background)

        # Set up subsystems.
        self.__assets = AssetHandler(self.__screen)
        self.__events = EventHandler() # Allow us to bind to events.
        self.__mouse = MouseState(self.events) # Tracks mouse state using
                                            # the events handler.
        self.__drag_handler = DragHandler(self.events, self.mouse)

        # Bind events.
        self.__events.bind(pygame.QUIT, lambda ev: self.stop())
        self.__events.bind(pygame.VIDEORESIZE, self.__ev_resize)

        self.__end_state = True

    @staticmethod
    def __default_screen_factory():
        info = pygame.display.Info()
        return pygame.display.set_mode((info.current_w // 2,
                                        info.current_h // 2))

    def __default_bg_surface_factory(self):
        return FillSurfaceEntity(screen_factory=self.__screen.copy)

    def __ev_resize(self, event):
        # TODO: Broken with image backgrounds.
        """Resize events callback.

        :param event:
        :param _:
        :return:
        """
        new_size = event.dict['size']
        surface_size = self.__screen.get_size()
        if new_size != surface_size:
            self.__screen = pygame.display.set_mode(event.dict['size'],
                                                    self.__screen.get_flags(),
                                                    self.__screen.get_bitsize())
            self.__background.reset(surface_factory=self.__screen.copy)
            self.init()
            # self.__debug_surface.reset(surface_factory=self.__screen.copy)
        self.__screen_width, self.__screen_height = self.__screen.get_size()

    @property
    def render_group(self):
        return self.__render_group

    @property
    def assets(self):
        return self.__assets

    @property
    def events(self):
        return self.__events

    @property
    def mouse(self):
        return self.__mouse

    @property
    def drag_handler(self):
        return self.__drag_handler

    @property
    def screen_width(self):
        return self.__screen_width

    @property
    def screen_height(self):
        return self.__screen_height

    def init(self):
        """
        """
        self.__renderer.init()

    def update(self):
        """
        """
        self.events.update()
        self.drag_handler.update()

    def throttle(self):
        """
        """
        return self.__clock.tick()

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
            self.throttle()
            self.render()

        return self.__end_state