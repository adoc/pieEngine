import pygame
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

    def ev_user_event_3(self, ev):
        pass

    def ev_user_event_4(self, ev):
        pass

    def ev_user_event_5(self, ev):
        pass

    def ev_user_event_6(self, ev):
        pass

    def ev_user_event_7(self, ev):
        pass

    def ev_user_event_8(self, ev):
        pass

    def ev_user_event_9(self, ev):
        pass

    def ev_user_event_10(self, ev):
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
            elif event.type == USER_EVENT_3:
                self.ev_user_event_3(event)
            elif event.type == USER_EVENT_4:
                self.ev_user_event_4(event)
            elif event.type == USER_EVENT_5:
                self.ev_user_event_5(event)
            elif event.type == USER_EVENT_6:
                self.ev_user_event_6(event)
            elif event.type == USER_EVENT_7:
                self.ev_user_event_7(event)
            elif event.type == USER_EVENT_8:
                self.ev_user_event_8(event)
            elif event.type == USER_EVENT_9:
                self.ev_user_event_9(event)
            elif event.type == USER_EVENT_10:
                self.ev_user_event_10(event)


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