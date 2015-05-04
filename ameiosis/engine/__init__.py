"""
Game Engine.
"""

import pygame.sprite
from pygame.locals import *

from ameiosis.engine.asset import AssetsMixin
from ameiosis.engine.event import DragHandler
from ameiosis.engine.sprite import ClickPointSprite
from ameiosis.engine.animation import AnimationLoop


class Background:
    def __init__(self, screen, flags=0, fill_color=pygame.Color(0, 0, 0)):
        self.__surface = None
        self.__screen = screen
        self.__screen_flags = flags
        self.__fill_color = fill_color
        self.__gen_surface()

    def __gen_surface(self):
        self.__surface = pygame.Surface(self.__screen.get_size(),
                                        self.__screen_flags, self.__screen)
        self.__surface = self.__surface.convert()
        self.__surface.fill(self.__fill_color)

    def render(self):
        return (self.__surface, (0, 0))

    def reset(self, *args, **kwa):
        if 2 > len(args) > 0:
            self.__surface = args[0]
        self.__screen_flags = kwa.get('flags') or self.__screen_flags
        self.__fill_color = kwa.get('fill_color') or self.__fill_color
        self.__gen_surface()


# TODO: Abstract out debug.
class Engine(AssetsMixin):
    """Game enging base class. Any game implementations will subclass
    from this.
    """
    def __init__(self, surface, clock, target_fps=60,
                 background=None):
        """

        :param pygame.Surface: Pygame surface this ``Engine`` is rendering to.
        :param pygame.time.Clock clock: Pygame ``Clock`` instance to throttle the engine.
        :param int target_fps:
        :param BackGround background: ``Background`` instance
        :return:
        """
        AssetsMixin.__init__(self)

        self.__target_fps = target_fps

        if not background:
            self.__background = Background(surface)
        else:
            self.__background = background

        self.__draw_surface = pygame.Surface(surface.get_size(), SRCALPHA)
        self.__draw_surface = self.__draw_surface.convert_alpha()

        self._surface = surface
        self._clock = clock
        self.__stopped = False

        self.__drag_handler = DragHandler()

        self.__draw_queue = []

        # Bind events.
        self.bind(QUIT, self.stop)
        self.bind(VIDEORESIZE, self.__ev_resize)
        self.bind(MOUSEBUTTONDOWN, self.__drag_handler.ev_mouse_down)
        self.bind(MOUSEBUTTONUP, self.__drag_handler.ev_mouse_up)
        self.bind(MOUSEMOTION, self.__drag_handler.ev_mouse_motion)

        self._debug_font = pygame.font.Font(None, 18)
        self._debug_pos = (8, 8)
        self._debug_lines = []

    @property
    def drag_handler(self):
        return self.__drag_handler

    @property
    def draw_surface(self):
        return self.__draw_surface

    def __ev_resize(self, event, **_):
        new_size = event.dict['size']
        surface_size = self._surface.get_size()
        if new_size != surface_size:
            self._surface = pygame.display.set_mode(event.dict['size'],
                                                    self._surface.get_flags(),
                                                    self._surface.get_bitsize())
            self.__background.reset(self._surface)

    # TODO: Refactor in to debug mixin.
    def draw_debug(self, tick_time=0):
        for n, line in enumerate(reversed(self._debug_lines)):
            pos = list(self._debug_pos)
            pos[1] = n * self._debug_font.get_linesize() + self._debug_pos[1]
            self._surface.blit(
                self._debug_font.render(*line),
                pos)
        if tick_time:
            pos[1] += self._debug_font.get_linesize() + self._debug_pos[1]
            self._surface.blit(
                self._debug_font.render("Tick: %.4f" % tick_time, 1, (240, 240, 240)),
                pos
            )
        self._debug_lines = []

    def add_draw(self, draw):
        self.__draw_queue.append(draw)

    def update(self):
        pass

    def stop(self, *args, **kwa):
        """Flag the engine to stop the ``Engine`` at the next
        opportunity.
        """
        self.__stopped = True

    @property
    def stopped(self):
        """Engine is done.
        :return: bool True when engine should be stopped as soon as possible
        """
        return self.__stopped

    def buffer(self):
        """Delays the game if rendering over target FPS. Also flips the
        display buffer.
        """
        self._clock.tick(self.__target_fps)
        pygame.display.flip()

    def draw(self):
        self.add_draw(self.__background.render)
        self.add_draw(lambda: (self.__draw_surface, (0,0)))

    def render(self):
        for draw in self.__draw_queue:
            self._surface.blit(*draw())
        del self.__draw_queue[:]