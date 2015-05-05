import functools

import pygame

from pie.sprite import DragableSpriteMixin


class CircleSprite(pygame.sprite.Sprite, DragableSpriteMixin):
    def __init__(self, size, pos):
        DragableSpriteMixin.__init__(self, *pos)
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self._size_mult = 10

        self.color_offset = 20
        self._color = (150, 150, 150)
        self.rect = pygame.Rect(pos[0]-self._get_radius(),
                                pos[1]-self._get_radius(),
                                self._get_radius()*2, self._get_radius()*2)
        self.un_drag()

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

    def _get_radius(self):
        return self.size * self._size_mult

    @property
    def radius(self):
        return self._get_radius()

    def update(self):
        if self.dragging:
            self.rect.center = self.drag_sprite.rect.center

    def draw(self, surface):
        self.rect = pygame.draw.circle(surface, self.color, self.rect.center,
                                       self.radius)

# This is a little hackish and could be refactored, but a pragmatic
# solution to avoid further containers.
_army_id = 0
@functools.total_ordering
class Army(CircleSprite):
    def __init__(self, size, team, pos):
        global _army_id # Hack
        _army_id += 1

        super(Army, self).__init__(size, pos)
        self._id = _army_id
        self.__team = team
        if team == 0:
            self._color = (255, 150, 150)
        elif team == 1:
            self._color = (150, 255, 150)
        elif team == 2:
            self._color = (150, 150, 255)

        self.battalion = None

        self.vector = pygame.math.Vector2()
        self._interpolation = 1
        self.velocity = 0

    def __lt__(self, other):
        return self._id < other._id

    def __eq__(self, other):
        return self._id == other._id

    @property
    def radius(self):
        init_rad = self.size * self._size_mult
        rad = int(init_rad *
                    (self.battalion.units/self.battalion._starting_units))
        return rad > 0 and rad or 1

    # TODO: Adjust this to work with rect since ``coord`` and ``_coord`` were removed.
    # @property
    # def coord(self):
    #     x, y = self.vector.lerp(self._coord, self.interpolation)
    #     return (int(x), int(y))

    @property
    def interpolation(self):
        return self._interpolation

    @interpolation.setter
    def interpolation(self, val):
        if val <= 0:
            val = 0
        elif val >= 1:
            val = 1
        self._interpolation = val

    def update(self):
        super(Army, self).update()
        self.interpolation -= self.velocity
        if self.battalion and self.battalion.units <= 0:
            self.kill()

    def __hash__(self):
        return hash(self._id)

    def __repr__(self):
        return """<Army sprite(id=%s). Team: %s>""" % (self._id, self.__team)