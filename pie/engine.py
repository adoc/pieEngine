"""
Game Engine.
"""

import pygame.sprite
from pygame.locals import *

from pie.base import MRunnable
from pie.asset import AssetHandler
from pie.event import DragHandler, EventHandler, MouseState
from pie.entity import FillSurfaceEntity, DrawSurfaceEntity

__all__ = ("Engine",)


# TODO: Abstract out debug.
class Engine(MRunnable):
    """Game enging base class. Any game implementations will subclass
    from this.
    """
    def __init__(self, screen, clock, target_fps=60, debug=False, auto_start=True):
        """

        :param pygame.Surface: Pygame screen this ``Engine`` is rendering to.
        :param pygame.time.Clock clock: Pygame ``Clock`` instance to throttle the engine.
        :param int target_fps:
        :param BackGround background: ``Background`` instance
        :return:
        """
        MRunnable.__init__(self, auto_start=auto_start)
        self.__clear_surface = FillSurfaceEntity(surface_factory=screen.copy)
        self.__draw_surface = DrawSurfaceEntity(surface_factory=screen.copy)
        self.__debug_surface = DrawSurfaceEntity(surface_factory=screen.copy)

        self.__screen = screen
        self.__clock = clock
        self.__target_fps = target_fps
        self.__debug = debug

        self.__blit_queue = []

        # Set up subsystems.
        self.assets = AssetHandler(screen)
        self.events = EventHandler() # Allow us to bind to events.
        self.mouse = MouseState(self.events) # Tracks mouse state using
                                            # the events handler.
        self.__drag_handler = DragHandler(self.events, self.mouse)

        # Bind events.
        self.events.bind(QUIT, lambda ev: self.stop())
        self.events.bind(VIDEORESIZE, self.__ev_resize)

        self._debug_font = pygame.font.Font(None, 18)
        self._debug_pos = (8, 8)
        self._debug_lines = []

    def __ev_resize(self, event):
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
            self.__clear_surface.reset(surface_factory=self.__screen.copy)
            self.__debug_surface.reset(surface_factory=self.__screen.copy)
        self.__screen_width, self.__screen_height = self.__screen.get_size()

    @property
    def screen_width(self):
        return self.__screen_width

    @property
    def screen_height(self):
        return self.__screen_height

    @property
    def drag_handler(self):
        return self.__drag_handler

    @property
    def draw_surface(self):
        return self.__draw_surface

    # TODO: Refactor in to debug mixin.
    def draw_debug(self, tick_time=0):
        for n, line in enumerate(reversed(self._debug_lines)):
            pos = list(self._debug_pos)
            pos[1] = n * self._debug_font.get_linesize() + self._debug_pos[1]
            self.__screen.blit(
                self._debug_font.render(*line),
                pos)
        if tick_time:
            pos[1] += self._debug_font.get_linesize() + self._debug_pos[1]
            self.__screen.blit(
                self._debug_font.render("Tick: %.4f" % tick_time, 1, (240, 240, 240)),
                pos
            )
        self._debug_lines = []

    def append_blit(self, draw):
        self.__blit_queue.append(draw)

    def update(self):
        self.events.handle()
        self.drag_handler.update()
        self._debug_lines.append(("FPS: %s" % (self.__clock.get_fps()), 1, (240, 240, 240)))

    def buffer(self):
        """Delays the game if rendering over target FPS then flips the
        display buffer.
        """
        self.__clock.tick_busy_loop(self.__target_fps)
        pygame.display.flip()

    # TODO: Rename.
    def draw(self):
        self.append_blit(self.__clear_surface.present)
        self.append_blit(self.__draw_surface.present)
        if self.__debug:
            self.append_blit(self.__debug_surface.present)

    def render(self):
        for presentation in self.__blit_queue:
            self.__screen.blit(*presentation())
        del self.__blit_queue[:]