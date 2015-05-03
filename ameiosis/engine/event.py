import sys
import traceback
from collections import defaultdict

import pygame
from pygame.locals import *

from ameiosis.engine.sprite import ClickPointSprite


class EventsMixin:
    """Engine mixin class providing Event functionality.
    """
    def __init__(self):
        """Initializes the EventsMixin and sets up some default
        bindings.
        """
        self.__mouse_button_state = [None] * 8
        self.__mouse_pos_state = (None,) * 2

        self.__event_binds = defaultdict(list)
        self.__event_user_binds = defaultdict(lambda: 0)
        self.__user_bind_index = 0

        # Set up default event bindings.
        self.bind(MOUSEBUTTONDOWN, self.ev_mouse_down)
        self.bind(MOUSEBUTTONUP, self.ev_mouse_up)
        self.bind(MOUSEMOTION, self.ev_mouse_motion)

    @property
    def mouse_button_state(self):
        """Returns a list of mouse buttons that are down. True when
        down, False when up, and None when there's been no state
        update.

        :return: List of truthy mouse button down states.
        """
        return self.__mouse_button_state

    @property
    def mouse_pos_state(self):
        return self.__mouse_pos_state

    def ev_mouse_down(self, ev, **kwa):
        self.__mouse_button_state[ev.button-1] = True

    def ev_mouse_up(self, ev, **kwa):
        self.__mouse_button_state[ev.button-1] = False

    def ev_mouse_motion(self, ev, **kwa):
        self.__mouse_pos_state = ev.pos

    def bind(self, event_const, func):
        """Bind a function a an event. (FIFO stack)
        :param pygame.*EVENT event_const: Event to bind the function to
        :param func: Function to be bound to the event.
        """
        self.__event_binds[event_const].append(func)

    def set_next_user_event(self, name):
        self.__user_bind_index += 1
        user_event = USEREVENT + self.__user_bind_index
        self.__event_user_binds[name] = user_event
        return user_event

    def bind_named(self, name, func):
        """

        :param name:
        :param func:
        :return:
        """
        user_event = self.__event_user_binds.get(name)
        if user_event:
            self.bind(user_event, func)
        else:
            self.bind(self.set_next_user_event(name), func)

        return user_event

    def unbind(self, event_const, func):
        """
        * This is a slow operation and should be used sparingly
        :param pygame.*EVENT event_const: Event to unbind the function
            from.
        :param func: Function to be unbound from the event.
        """
        self.__event_binds[event_const].remove(func)

    def unbind_named(self, name, func):
        """

        :param name:
        :param funct:
        :return:
        """

        self.unbind(self.__event_user_binds[name], func)

    def handle_events(self):
        """Check for events that have been bound and execute their
        callbacks with params (event, engine=<Engine object>). Clears
        the event queue after callback execution.
        """
        # TODO: We might need to use an ordered dict for __event_binds
        for event in pygame.event.get(list(self.__event_binds.keys())):
                for callback in self.__event_binds[event.type]:
                    callback(event, engine=self)
        pygame.event.clear()


class DragHandler(set):
    def __init__(self, *draggable):
        set.__init__(self, *draggable)

    @property
    def dragging(self):
        for sprite in self:
            if sprite.dragging:
                yield sprite

    def ev_mouse_down(self, ev, **kwa):
        self.__click_sprite = ClickPointSprite(ev.pos.x, ev.pos.y)
        for sprite in self:
            if pygame.sprite.collide_circle(self.__click_sprite, sprite):
                sprite.drag(self.__click_sprite)

    def ev_mouse_up(self, ev, **kwa):
        for sprite in self.dragging:
            sprite.un_drag()

    def ev_mouse_motion(self, ev, engine=None):
        if engine.mouse_button_state[0] is True:
            self.__click_sprite.rect.center = (x, y)

    # # Deprecated
    # def check(self, x, y):
    #     self.__click_sprite = ClickPointSprite(x, y)
    #     for sprite in self:
    #         if pygame.sprite.collide_circle(self.__click_sprite, sprite):
    #             sprite.drag(self.__click_sprite)
    #
    # # Deprecated
    # def move(self, x, y):
    #     self.__click_sprite.rect.center = (x, y)
    #
    # # Deprecated
    # def un_drag(self):
    #     for sprite in self.dragging:
    #         sprite.un_drag()