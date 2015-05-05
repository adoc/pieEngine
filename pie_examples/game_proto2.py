import time

import pygame

from lanchester.model.side import Battalion
from pie.event import USER_EVENT_1
from ameiosis.sprite import Army
from pie.game import Ameosis as AmeosisBase


class Ameosis(AmeosisBase):
    def __init__(self, surface, clock, **kwa):
        super(Ameosis, self).__init__(surface, clock, **kwa)
        self.__spawn_size = 3
        self.__spawn_team = 0
        # self._margin_lines = 80
        self._teams_spawn_ts = {}
        pygame.time.set_timer(USER_EVENT_1, 5000)

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
        try:
            return self.__spawn_team
        finally:
            self.__spawn_team += 1
            self.__spawn_team %= 2

    def ev_key_up(self, ev):
        super(Ameosis, self).ev_key_up(ev)

    def ev_user_event_1(self, ev):
        super(Ameosis, self).ev_user_event_1(ev)
        ev.pos = (150, 150)
        team = self.spawn_team
        self._teams_spawn_ts[team] = time.time()
        army = Army(self.__spawn_size, team, ev.pos)
        army.battalion = Battalion(self.__spawn_size * 1000, .01)
        self._armies_lanc_factions[team].add_member(army.battalion)
        self._armies_sprites[team].add(army)
        self.__drag_handler.add(army)

    def update(self):
        super(Ameosis, self).update()
        self._debug_lines.append(("Size (up/down): %s" % (self.__spawn_size), 1, (240, 240, 240)))
        self._debug_lines.append(("Team (left/right): %s" % (self.__spawn_team), 1, (240, 240, 240)))
        self._debug_lines.append(("Simulate (space): %s" % (self._simulate_battle), 1, (240, 240, 240)))

    def draw(self):
        super(Ameosis, self).draw()
        # Draw margin lines.
        width, height = self.__screen.get_size()
        pygame.draw.circle(self.__screen, (120,120,120),
                            (width//2, height//2), height//4, 1)

        # pygame.draw.line(self.__screen, (120,120,120),
        #     (self._margin_lines, 0), (self._margin_lines, height))
        # pygame.draw.line(self.__screen, (120,120,120),
        #     (width-self._margin_lines, 0), (width-self._margin_lines, height))


if __name__ == "__main__":
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((700, 700))

    game = Ameosis(screen, clock)

    while not game.done:
        t1 = time.time()
        game.buffer()
        game.handle_events()
        game.update()
        game.draw()
        game.draw_debug(tick_time=time.time() - t1)