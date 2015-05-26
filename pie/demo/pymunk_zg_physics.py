import pygame

import pymunk
import pymunk.pygame_util

from pie.engine import Engine
from pie.entity.base import SpriteRect
from pie.entity.primitive import Surface, Point, Fill
from pie.math import flip_y_normals, vect_to_rad



class Object(SpriteRect):
    def __init__(self, space):
        # TODO: We need translations from view pixels to space coordinates.
        # 1:1 is fine for testing, but our "scaling" issue I think starts here.

        SpriteRect.__init__(self, (0,0), (100,100))
        self.rect.center = (512, 256)

        mass = .001
        inertia = pymunk.moment_for_box(mass, *self.rect.size)

        self.__body = pymunk.Body(mass, inertia)
        self.__body.position = pymunk.Vec2d(self.rect.center)
        self.__body.angular_velocity_limit = 100
        self.__body.velocity_limit = 100

        self.__offset = pymunk.Vec2d([0, 0])

        self.poly = pymunk.Poly.create_box(self.__body, size=self.rect.size)
        self.poly.color = pygame.color.THECOLORS['whitesmoke']

        space.add(self.__body)

    def fore(self):
        self.__body.apply_force(self.rotate_force_vector(pymunk.Vec2d(1, 0)), self.offset)

    def aft(self):
        self.__body.apply_force(self.rotate_force_vector(pymunk.Vec2d(-1, 0)), self.offset)

    def port(self):
        self.__body.apply_force(self.rotate_force_vector(pymunk.Vec2d(0, 1)), self.offset)

    def starboard(self):
        self.__body.apply_force(self.rotate_force_vector(pymunk.Vec2d(0,-1)), self.offset)

    def rotate_force_vector(self, vect):
        return vect.rotated(vect_to_rad(self.__body.rotation_vector))

    @property
    def body(self):
        return self.__body

    @property
    def offset(self):
        return self.__offset

    @property
    def offset_position(self):
        op = self.rect.center + self.offset
        return int(op[0]), int(op[1])

    def update(self):
        SpriteRect.update(self)
        self.rect.center = self.body.position
        self.__body.reset_forces()


class Zg(Engine):
    def __init__(self, *args, **kwa):
        Engine.__init__(self, *args, **kwa)

        # Set up the draw surface.
        self.__draw = Fill()
        self.add_render_plain(self.__draw)

        # Set up physics.
        self.__space = pymunk.Space()
        self.__obj = Object(self.__space)

        # Bind events.
        self.events.bind(pygame.KEYDOWN, self._ev_k_down)

    def _ev_k_down(self, ev):
        if ev.mod:
            pass
        else:
            if ev.key == pygame.K_LEFT:
                self.__obj.offset[0] -= 1
            elif ev.key == pygame.K_RIGHT:
                self.__obj.offset[0] += 1
            elif ev.key == pygame.K_UP:
                self.__obj.offset[1] -= 1
            elif ev.key == pygame.K_DOWN:
                self.__obj.offset[1] += 1
            elif ev.key == pygame.K_w:
                self.__obj.fore()
            elif ev.key == pygame.K_s:
                self.__obj.aft()
            elif ev.key == pygame.K_a:
                self.__obj.port()
            elif ev.key == pygame.K_d:
                self.__obj.starboard()

    def update(self):
        Engine.update(self)
        self.__space.step(1/self.fps)
        self.__obj.update()
        self.__draw.fill()
        pymunk.pygame_util.draw(self.__draw.surface, self.__obj.poly)
        poly_verts = self.__obj.poly.get_vertices()
        pygame.draw.circle(self.__draw.surface, (255,0,0),
                           flip_y_normals(self.__obj.offset_position,
                                          self.screen_height, ret_vec=False), 2, 2)
        pygame.draw.line(self.__draw.surface, (0,255,0),
                         flip_y_normals(poly_verts[-2],
                                        self.screen_height),
                         flip_y_normals(poly_verts[-1],
                                        self.screen_height))


# Keep this minimal.
if __name__ == "__main__":
    pygame.init()
    game = Zg(pygame.display.set_mode((1024, 512), 0, 32),
                       non_static_background=True)

    game.start()