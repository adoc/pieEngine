import pygame

from pie.util import OrderedDefaultDict
from pie.sprite import ClickPointSprite


class MouseState:
    """Tracks mouse state
    """
    def __init__(self, event_handler, button_down_state=True,
                 button_index_offset=-1):
        self.__button_down_state = button_down_state
        self.__button_index_offset = button_index_offset
        self.__button_state = [None] * 8
        self.__pos_state = (None,) * 2

        # Set up mouse events bindings.
        event_handler.bind(pygame.MOUSEBUTTONDOWN, self.__ev_mouse_down)
        event_handler.bind(pygame.MOUSEBUTTONUP, self.__ev_mouse_up)
        event_handler.bind(pygame.MOUSEMOTION, self.__ev_mouse_motion)

    @property
    def buttons(self):
        """Returns a list of mouse buttons that are down. By default,
        buttons are zero-indexed (i.e. button 1 is .buttons[0]), and
        True when down, False when up, and None when there's been no
        state update.

        :return: List of mouse button down states.
        """
        return self.__button_state

    @property
    def pos(self):
        """Returns the current mouse position.

        :return: Tuple (x, y) of current mouse position.
        """
        return self.__pos_state

    def __ev_mouse_down(self, ev):
        """Mouse down events has triggered.

        :param ev: Event object.
        """
        self.__button_state[ev.button - self.__button_index_offset] =\
            self.__button_down_state

    def __ev_mouse_up(self, ev):
        """Mouse up events has triggered.

        :param ev:
        """
        self.__button_state[ev.button - self.__button_index_offset] =\
            not self.__button_down_state

    def __ev_mouse_motion(self, ev):
        """Mouse motion even has triggered.

        :param ev:
        """
        self.__pos_state = ev.pos


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

    def handle(self):
        """Check for events that have been bound and execute their
        callbacks with params (events, engine=<Engine object>). Clears
        the events queue after callback execution.
        """
        for event in pygame.event.get(list(self.__event_binds.keys())):
                for callback in self.__event_binds[event.type]:
                    callback(event)
        pygame.event.clear()


class DragHandler(set):
    def __init__(self, event_handler, mouse_handler, *draggable):
        set.__init__(self, *draggable)
        self.__event_handler = event_handler
        self.__mouse_handler = mouse_handler

        event_handler.bind(pygame.MOUSEBUTTONDOWN, self.__ev_mouse_down)
        event_handler.bind(pygame.MOUSEBUTTONUP, self.__ev_mouse_up)
        event_handler.bind(pygame.MOUSEMOTION, self.__ev_mouse_motion)

    @property
    def dragging(self):
        for sprite in self:
            if sprite.dragging:
                yield sprite

    def __ev_mouse_down(self, ev):
        self.__click_sprite = ClickPointSprite(ev.pos[0], ev.pos[1])
        for sprite in self:
            if pygame.sprite.collide_circle(self.__click_sprite, sprite):
                sprite.drag(self.__click_sprite)

    def __ev_mouse_up(self, ev):
        for sprite in self.dragging:
            sprite.un_drag()

    def __ev_mouse_motion(self, ev, engine=None):
        if self.__mouse_handler.buttons[0] is True:
            self.__click_sprite.rect.center = (ev.pos[0], ev.pos[1])