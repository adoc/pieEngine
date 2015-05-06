# TODO: Broken!

import time

import pygame
from pygame.locals import *

from lanchester.model.side import Battalion
from pie_examples.ameiosis.sprite import Army
from pie.game import Ameosis as AmeosisBase


class Ameosis(AmeosisBase):
    def __init__(self, surface, clock, **kwa):
        super(Ameosis, self).__init__(surface, clock, **kwa)
        self.__spawn_size = 1
        self.__spawn_team = 0

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

    def ev_key_up(self, ev):
        super(Ameosis, self).ev_key_up(ev)
        if ev.key == K_UP:
            self.spawn_size += 1
        elif ev.key == K_DOWN:
            self.spawn_size -= 1
        elif ev.key == K_RIGHT:
            self.spawn_team += 1
        elif ev.key == K_LEFT:
            self.spawn_team -= 1
        elif ev.key == K_SPACE:
            self._simulate_battle = not self._simulate_battle

    def ev_mouse_down(self, ev):
        super(Ameosis, self).__ev_mouse_down(ev)
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