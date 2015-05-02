"""
Game Engine.
"""

import pygame.sprite

from ameiosis.engine.assets import AssetsMixin
from ameiosis.engine.events import ClickPointSprite, EventsMixin, DragHandler
from ameiosis.engine.animations import AnimationLoop


class Engine(EventsMixin, AssetsMixin):
    def __init__(self, surface, clock, target_fps=60,
                 background_color=(20, 20, 20)):
        AssetsMixin.__init__(self)
        EventsMixin.__init__(self)
        self._drag_handler = DragHandler()
        self._surface = surface
        self._clock = clock
        self.__done = False
        self.__target_fps = target_fps

        self.__mouse_left_down = False

        self.__background = pygame.Surface(self._surface.get_size())
        self.__background = self.__background.convert()
        self.__background.fill(background_color)

        self._debug_font = pygame.font.Font(None, 18)
        self._debug_pos = (8, 8)
        self._debug_lines = []

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
        self._surface.blit(self.__background, (0, 0))