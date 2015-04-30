import functools

import pygame

from ameiosis.framework import ClickPointSprite


class CircleSprite(pygame.sprite.Sprite):
    def __init__(self, size, pos):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self._size_mult = 10

        self.color_offset = 20
        self._color = (150, 150, 150)
        self.__coord = pos
        self.rect = pygame.Rect(pos[0]-self._get_radius(), pos[1]-self._get_radius(),
                                self._get_radius()*2, self._get_radius()*2)
        self.un_drag()

    def un_drag(self):
        self.dragging = False
        self.drag_sprite = ClickPointSprite(*self.__coord)

    def drag(self, drag_sprite):
        self.dragging = True
        self.drag_sprite = drag_sprite

    @property
    def color(self):
        if self.dragging:
            color_0 = self._color[0] + self.color_offset
            color_1 = self._color[1] + self.color_offset
            color_2 = self._color[2] + self.color_offset
            return (color_0 < 256 and color_0 or 255,
                    color_1 < 256 and color_1 or 255,
                    color_2 < 256 and color_2 or 255)
        else:
            return self._color

    @property
    def coord(self):
        return self.__coord

    def _get_radius(self):
        return self.size * self._size_mult

    @property
    def radius(self):
        return self._get_radius()

    def update(self):
        if self.dragging:
            self.__coord = self.drag_sprite.rect.center

    def draw(self, surface):
        self.rect = pygame.draw.circle(surface, self.color, self.coord,
                                       self.radius)

_id = 0
@functools.total_ordering
class Army(CircleSprite):
    def __init__(self, size, team, pos):
        global _id
        _id += 1
        super(Army, self).__init__(size, pos)
        self._id = _id
        self.__team = team
        if team == 0:
            self._color = (255, 150, 150)
        elif team == 1:
            self._color = (150, 255, 150)

        self.battalion = None
        self.battle_loss = 0

    def __lt__(self, other):
        return self._id < other._id

    def __eq__(self, other):
        return self._id == other._id

    @property
    def radius(self):
        init_rad = self.size * self._size_mult
        rad = int(init_rad * (self.battalion.units/self.battalion._starting_units))
        return rad > 0 and rad or 1

    def update(self):
        super(Army, self).update()
        if self.battalion:
            self.battle_loss = self.battalion._starting_units - self.battalion.units

            if self.battalion.units <= 0:
                self.kill()

    def __hash__(self):
        return hash(self._id)

    def __repr__(self):
        return """<Army sprite(id=%s). Team: %s>""" % (self._id, self.__team)