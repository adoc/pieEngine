import pygame
import pygame.math

from pie.util import OrderedDefaultDict
from pie.entity.primitive import Point
from pie.math import vect_diff


__all__ = ("EventHandler",
           "DragHandler")


class EventHandler:
    """EventHandler class providing Event bindings and user events.
    """
    def __init__(self):
        """Initializes the EventsMixin and sets up some default
        bindings.
        """
        self.__event_binds = OrderedDefaultDict(list)
        self.__user_events = OrderedDefaultDict(lambda: 0)
        self.__user_bind_index = 0

    def bind(self, event_const, func):
        """Bind a function a an events. (FIFO stack)
        :param pygame.*EVENT event_const: Event to bind the function to
        :param func: Function to be bound to the events.
        """
        self.__event_binds[event_const].append(func)

    def unbind(self, event_const, func):
        """
        * This is a slow operation and should be used sparingly
        :param pygame.*EVENT event_const: Event to unbind the function
            from.
        :param func: Function to be unbound from the events.
        """
        self.__event_binds[event_const].remove(func)

    def set_user(self, name):
        """Set a user events, but does not bind it.

        :param name:
        :return:
        """
        self.__user_bind_index += 1
        user_event = pygame.USEREVENT + self.__user_bind_index
        self.__user_events[name] = user_event
        return user_event

    def bind_user(self, name, func):
        """

        :param name:
        :param func:
        :return:
        """
        user_event = self.__user_events.get(name)
        if user_event:
            self.bind(user_event, func)
        else:
            self.bind(self.set_user(name), func)

        return user_event

    def unbind_user(self, name, func):
        """

        :param name:
        :param funct:
        :return:
        """

        self.unbind(self.__user_events[name], func)

    def update(self):
        """Check for events that have been bound and execute their
        callbacks with params (events, engine=<Engine object>). Clears
        the events queue after callback execution.
        """
        for event in pygame.event.get(list(self.__event_binds.keys())):
                for callback in self.__event_binds[event.type]:
                    callback(event)
        pygame.event.clear()


#TODO: Might need refactor.
class DragHandler(list):
    """List of draggable objects.
    """
    def __init__(self, event_handler, *draggable, drag_button=0):
        list.__init__(self, *draggable)
        self.__event_handler = event_handler
        self.__drag_button = drag_button
        # self.__collision_func = collision_func
        self.__dragging = None

        event_handler.bind(pygame.MOUSEBUTTONDOWN, self.__ev_mouse_down)
        event_handler.bind(pygame.MOUSEBUTTONUP, self.__ev_mouse_up)
        event_handler.bind(pygame.MOUSEMOTION, self.__ev_mouse_motion)

    def __ev_mouse_down(self, ev):
        # Creates a click sprite at the click point then checks it for
        # collisions against all the other sprites in this handler.
        if self.drag_button_state:
            self.__click_sprite = Point((ev.pos[0], ev.pos[1]))
            for sprite in self:
                if sprite.collide_func(self.__click_sprite, sprite):
                    self.__dragging = (sprite,
                                       vect_diff(sprite.rect.topleft,
                                            self.__click_sprite.rect.topleft))

    def __ev_mouse_up(self, ev):
        self.__dragging = None

    def __ev_mouse_motion(self, ev):
        if self.__dragging and self.drag_button_state:
            self.__click_sprite.rect.topleft = (ev.pos[0], ev.pos[1])

    @property
    def drag_button_state(self):
        return pygame.mouse.get_pressed()[self.__drag_button] == 1

    def update(self):
        if self.__dragging:
            sprite, offset = self.__dragging
            sprite.rect.topleft = self.__click_sprite.rect.topleft + offset