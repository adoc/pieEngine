"""
Game Engine.
"""

import pygame.sprite
from pygame.locals import *

from ameiosis.engine.asset import AssetsMixin
from ameiosis.engine.event import EventsMixin, DragHandler
from ameiosis.engine.sprite import ClickPointSprite
from ameiosis.engine.animation import AnimationLoop


class Background(pygame.Surface):
    def __init__(self, screen, flags=0, fill_color=pygame.Color(0, 0, 0)):
        pygame.Surface.__init__(self, screen.get_size(), flags, screen)
        self.__fill_color = fill_color
        self.fill(fill_color)


# TODO: Abstract out debug.
class Engine(EventsMixin, AssetsMixin):
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
        EventsMixin.__init__(self)

        if not background:
            background = Background(surface)
        self.__background = background.convert(surface)

        self._drag_handler = DragHandler()
        self._surface = surface
        self._clock = clock
        self.__done = False
        self.__target_fps = target_fps

        self.__mouse_left_down = False

        # self.__background = pygame.Surface(self._surface.get_size())
        # self.__background = self.__background.convert()
        # self.__background.fill(background_color)

        self._debug_font = pygame.font.Font(None, 18)
        self._debug_pos = (8, 8)
        self._debug_lines = []

    # TODO: Refactor into a mixin.
    def ev_mouse_down(self, ev):
        if ev.button == 1:
            self.__mouse_left_down = True
            self._drag_handler.check(*ev.pos)

    def ev_mouse_up(self, ev):
        if ev.button == 1:
            self.__mouse_left_down = False
            self._drag_handler.un_drag()

    def ev_mouse_motion(self, ev):
        if self.__mouse_left_down:
            self._drag_handler.move(*ev.pos)

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

    def update(self):
        pass

    def quit(self):
        self.__done = True

    @property
    def done(self):
        return self.__done

    def buffer(self):
        self._clock.tick(self.__target_fps)
        pygame.display.flip()

    def draw(self):
        # TODO: Might implement a list stack blit here to allow for
        # reordering of blits rather than being based on inheritance.
        # This might not be neccessary.
        self._surface.blit(self.__background, (0, 0))