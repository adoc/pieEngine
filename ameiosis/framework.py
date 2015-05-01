"""
Game Framework.
"""

import pygame.sprite
from pygame.locals import *


USER_EVENT_1 = USEREVENT + 1
USER_EVENT_2 = USEREVENT + 2
USER_EVENT_3 = USEREVENT + 3
USER_EVENT_4 = USEREVENT + 4
USER_EVENT_5 = USEREVENT + 5
USER_EVENT_6 = USEREVENT + 6
USER_EVENT_7 = USEREVENT + 7
USER_EVENT_8 = USEREVENT + 8
USER_EVENT_9 = USEREVENT + 9
USER_EVENT_10 = USEREVENT + 10


class ClickPointSprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.rect = pygame.Rect((x, y), (1,1))
        self.radius = 1


class EventsMixin:
    def ev_mouse_down(self, ev):
        pass

    def ev_mouse_up(self, ev):
        pass

    def ev_mouse_motion(self, ev):
        pass

    def ev_key_down(self, ev):
        pass

    def ev_key_up(self, ev):
        pass

    def ev_user_event_1(self, ev):
        pass

    def ev_user_event_2(self, ev):
        pass

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit()
            elif event.type == KEYDOWN:
                self.ev_key_down(event)
            elif event.type == KEYUP:
                self.ev_key_up(event)
            elif event.type == MOUSEBUTTONDOWN:
                self.ev_mouse_down(event)
            elif event.type == MOUSEBUTTONUP:
                self.ev_mouse_up(event)
            elif event.type == MOUSEMOTION:
                self.ev_mouse_motion(event)
            elif event.type == USER_EVENT_1:
                self.ev_user_event_1(event)
            elif event.type == USER_EVENT_2:
                self.ev_user_event_2(event)


class DragHandler(set):
    def __init__(self, *draggable):
        set.__init__(self, *draggable)

    @property
    def dragging(self):
        for sprite in self:
            if sprite.dragging:
                yield sprite

    def check(self, x, y):
        self.__click_sprite = ClickPointSprite(x, y)
        for sprite in self:
            if pygame.sprite.collide_circle(self.__click_sprite, sprite):
                sprite.drag(self.__click_sprite)

    def move(self, x, y):
        self.__click_sprite.rect.center = (x, y)

    def un_drag(self):
        for sprite in self.dragging:
            sprite.un_drag()


class Game(EventsMixin):
    def __init__(self, surface, clock, target_fps=60,
                 background_color=(20, 20, 20)):
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
        self._clock.tick(60)
        pygame.display.flip()

    def draw(self):
        self._surface.blit(self.__background, (0, 0))