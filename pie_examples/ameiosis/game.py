from functools import partial
from collections import defaultdict

import pygame
from pygame.locals import *

from pie.engine import Engine

from lanchester.model import LanchesterSquareAllies
from lanchester.model.side import Faction, Engagement


Engagement = partial(Engagement, alg=LanchesterSquareAllies())


class BattleHandler:
    def __init__(self, armies):
        self.__armies = armies
        self.__collisions = {}
        self.__engagments = set()

    def update(self):
        # Check collisions

        for team1 in self.__armies.values():
            for team2 in self.__armies.values():
                if team1 != team2:
                    self.__collisions = (
                        pygame.sprite.groupcollide(team1, team2, False, False,
                                                   pygame.sprite.collide_circle)
                    )

        if self.__collisions:
            engaged = list(self.__collisions.keys())
            for val in self.__collisions.values():
                engaged.extend(val)
            #print(engaged)
            engaged = set(engaged)
            engaged = sorted(engaged)

            self.__engagments.add(Engagement(*[army.battalion
                                                    for army in engaged]))

        remove = []
        for engagement in self.__engagments:
            if not engagement.finished:
                engagement.do_round()

            else:
                remove.append(engagement)

        if remove:
            print("Removing Engagements...")
        for engagement in remove:
            self.__engagments.remove(engagement)


class Ameiosis(Engine):
    def __init__(self, screen, clock, **kwa):
        super(Ameiosis, self).__init__(screen, clock, **kwa)
        self._armies_sprites = defaultdict(pygame.sprite.Group)
        self._armies_lanc_factions = defaultdict(self._make_faction)
        self.__faction_count = 0
        self._simulate_battle = False
        self.__battlehandler = BattleHandler(self._armies_sprites)

        self.events.bind(K_ESCAPE, self.stop)

    def _make_faction(self):
        self.__faction_count += 1
        return Faction(self.__faction_count)

    def update(self):
        super(Ameiosis, self).update()
        if self._simulate_battle:
            self.__battlehandler.update()

        self._debug_lines.append(("ESC to exit.", 1, (240,240,240)))

    def draw(self):
        super(Ameiosis, self).draw()
        for team in self._armies_sprites.values():
            for obj in team:
                obj.update()
                self.append_blit(obj.present)