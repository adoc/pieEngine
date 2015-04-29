import pygame
from pygame.locals import *

from ameiosis.framework import ClickPointSprite, Game


class CircleSprite(pygame.sprite.Sprite):
    def __init__(self, size, pos):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self._size_mult = 10

        self.color_offset = 20
        self._color = (150, 150, 150)
        self.__coord = pos

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

    @property
    def radius(self):
        return self.size * self._size_mult

    def update(self):
        if self.dragging:
            self.__coord = self.drag_sprite.rect.center

    def draw(self, surface):
        self.rect = pygame.draw.circle(surface, self.color, self.coord,
                                       self.radius)


class Army(CircleSprite):
    def __init__(self, size, team, pos):
        CircleSprite.__init__(self, size, pos)
        self.__team = 0

        if team == 0:
            self._color = (255,150,150)
        elif team ==1:
            self._color = (150,255,150)


class Ameosis(Game):
    def __init__(self, surface, clock, *objs, **kwa):
        Game.__init__(self, surface, clock, **kwa)
        self.__objs = list(objs)
        self._drag_handler.update(objs)
        self.__spawn_size = 1
        self.__spawn_team = 0
        self.__simulate = False

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
        Game.ev_key_up(self, ev)
        if ev.key == K_UP:
            self.spawn_size += 1
        elif ev.key == K_DOWN:
            self.spawn_size -= 1
        elif ev.key == K_RIGHT:
            self.spawn_team += 1
        elif ev.key == K_LEFT:
            self.spawn_team -= 1
        elif ev.key == K_s:
            self.__simulate = not self.__simulate

    def ev_mouse_down(self, ev):
        Game.ev_mouse_down(self, ev)
        if ev.button == 3:
            army = Army(self.__spawn_size, self.__spawn_team, ev.pos)
            self.__objs.append(army)
            self._drag_handler.add(army)

    def update(self):
        self._debug_lines.append(("Size: %s" % (self.__spawn_size), 1, (240, 240, 240)))
        self._debug_lines.append(("Team: %s" % (self.__spawn_team), 1, (240, 240, 240)))
        self._debug_lines.append(("Simulate: %s" % (self.__simulate), 1, (240, 240, 240)))

    def draw(self):
        Game.draw(self)
        for obj in self.__objs:
            obj.update()
            obj.draw(self._surface)