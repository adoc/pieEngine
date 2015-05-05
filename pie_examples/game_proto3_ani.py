"""
Demonstrates asset loading and animation.
"""

import time
import random

import pygame
from pygame.locals import *

from pie.sprite import AnimatedSprite
from ameiosis.game import Ameosis as AmeosisBase


class Ameosis(AmeosisBase):
    def __init__(self, surface, clock, **kwa):
        super(Ameosis, self).__init__(surface, clock, **kwa)
        self.__spawn_size = 3
        self.__spawn_team = 0
        self._teams_spawn_ts = {}

        pygame.time.set_timer(self.event.set_next_user_event('ev_spawn_thing'), 10)
        self.event.bind_user('ev_spawn_thing', self.ev_spawn_thing)

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
    def stopped(self):
        return super(Ameosis, self).stopped or len(self._armies_sprites[0]) > 1000

    @property
    def spawn_team(self):
        try:
            return self.__spawn_team
        finally:
            self.__spawn_team += 1
            self.__spawn_team %= 2

    def ev_spawn_thing(self, ev, **kwa):
        pos = (random.random()*self.screen_width-20,
               random.random()*self.screen_height-20)

        spr = AnimatedSprite(self.assets.animations['bomber1'], pos,
                             self.assets.animations.get_largest_frame('bomber1').get_size())

        team = self.spawn_team
        self._armies_sprites[team].add(spr)
        self.drag_handler.add(spr)

    def update(self):
        super(Ameosis, self).update()
        self._debug_lines.append(("Size (up/down): %s" % (self.__spawn_size), 1, (240, 240, 240)))
        self._debug_lines.append(("Team (left/right): %s" % (self.__spawn_team), 1, (240, 240, 240)))
        self._debug_lines.append(("Simulate (space): %s" % (self._simulate_battle), 1, (240, 240, 240)))


if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((1024, 512),
                                     DOUBLEBUF | ASYNCBLIT | RESIZABLE)
    clock = pygame.time.Clock()
    game = Ameosis(screen, clock)

    game.assets.animations.add_from_zip('bomber1', "assets\\bomber1.zip",
                                        size=(64,64))

    while not game.stopped:
        t1 = time.time()
        game.buffer()
        game.update()
        game.draw()
        game.render()
        game.draw_debug(tick_time=time.time() - t1)