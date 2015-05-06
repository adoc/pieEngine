# TODO: Broken!

import time

import pygame
from pygame.locals import *

from lanchester.model.side import Battalion
from pie_examples.ameiosis.sprite import Army
from pie_examples.ameiosis.game import Ameiosis as AmeosisBase


class Ameosis(AmeosisBase):
    def __init__(self,*args, **kwa):
        super(Ameosis, self).__init__(*args, **kwa)
        self.__spawn_size = 1
        self.__spawn_team = 0

        self.events.bind(K_UP, self.__ev_inc_spawn_size)
        self.events.bind(K_DOWN, self.__ev_dec_spawn_size)
        self.events.bind(K_LEFT, self.__ev_dec_team)
        self.events.bind(K_RIGHT, self.__ev_inc_team)
        self.events.bind(K_SPACE, self.__ev_tog_simulate)

        self.events.bind(MOUSEBUTTONDOWN, self.__ev_mouse_down)

    def __ev_inc_spawn_size(self, ev):
        self.spawn_size += 1

    def __ev_dec_spawn_size(self, ev):
        self.spawn_size -= 1

    def __ev_inc_team(self, ev):
        self.spawn_team += 1

    def __ev_dec_team(self, ev):
        self.spawn_team -= 1

    def __ev_tog_simulate(self, ev):
        self._simulate_battle = not self._simulate_battle

    @property
    def spawn_size(self):
        return self.__spawn_size

    @spawn_size.setter
    def spawn_size(self, val):
        if val > 10:
            self.__spawn_size = 10
        elif val < 1:
            self.__spawn_size = 1
        else:
            self.__spawn_size = val

    @property
    def spawn_team(self):
        return self.__spawn_team

    @spawn_team.setter
    def spawn_team(self, val):
        if val > 1:
            self.__spawn_team = 1
        elif val < 0:
            self.__spawn_team = 0
        else:
            self.__spawn_team = val

    def __ev_mouse_down(self, ev):
        if ev.button == 3: # Right-Click
            army = Army(self.__spawn_size, self.__spawn_team, ev.pos)

            army.battalion = Battalion(self.__spawn_size * 1000, .01)

            self._armies_lanc_factions[self.__spawn_team].add_member(
                                                                army.battalion)
            self._armies_sprites[self.__spawn_team].add(army)
            self.__drag_handler.add(army)

    def update(self):
        super(Ameosis, self).update()
        self._debug_lines.append(("Size (up/down): %s" % (self.__spawn_size), 1, (240, 240, 240)))
        self._debug_lines.append(("Team (left/right): %s" % (self.__spawn_team), 1, (240, 240, 240)))
        self._debug_lines.append(("Simulate (space): %s" % (self._simulate_battle), 1, (240, 240, 240)))


if __name__ == "__main__":
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1024, 512))

    game = Ameosis(screen, clock)

    while not game.stopped:
        t1 = time.time()
        game.buffer()
        game.update()
        game.draw()
        game.render()

        # Will be refactored.
        game.draw_debug(tick_time=time.time() - t1)