import pygame

import pymunk
import pymunk.pygame_util

from pie.engine import Engine
from pie.entity.base import SpriteRect
from pie.entity.primitive import Surface


class Object(SpriteRect):
    def __init__(self, space):
        # TODO: We need translations from view pixels to space coordinates.
        # 1:1 is fine for testing, but our "scaling" issue I think starts here.

        SpriteRect.__init__(self, (0,0), (100,100))

        mass = 100
        inertia = pymunk.moment_for_box(mass, *self.rect.size)

        self.__body = pymunk.Body(mass, inertia)
        self.__body.position = pymunk.Vec2d(self.rect.topleft)
        self.__body.angular_velocity_limit = 100
        self.__body.velocity_limit = 100

        # Is nothing done with poly??
        self.poly = pymunk.Poly.create_box(self.__body, size=self.rect.size, offset=(512, 256))
        self.poly.color = pygame.color.THECOLORS['whitesmoke']

        space.add(self.__body)

    @property
    def body(self):
        return self.__body


class Zg(Engine):
    def __init__(self, *args, **kwa):
        Engine.__init__(self, *args, **kwa)
        self.__draw = Surface()
        self.add_render_plain(self.__draw)

        self.__space = pymunk.Space()
        self.__obj = Object(self.__space)

    def update(self):
        Engine.update(self)
        pymunk.pygame_util.draw(self.__draw.surface, self.__obj.poly)


# Keep this minimal.
if __name__ == "__main__":
    pygame.init()
    game = Zg(pygame.display.set_mode((1024, 512), 0, 32),
                       non_static_background=True)

    game.start()