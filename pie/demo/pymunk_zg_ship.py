import math

import pygame

import pymunk
import pymunk.pygame_util

from pie.engine import Engine
from pie.entity.base import SpriteRect
from pie.entity.primitive import Surface, Point, Fill
from pie.math import flip_y_normals, vect_to_rad


class Ship(SpriteRect):
    def __init__(self, space, mass=0.1, position=(600, 256)):
        # TODO: We need translations from view pixels to space coordinates.
        # 1:1 is fine for testing, but our "scaling" issue I think starts here.

        SpriteRect.__init__(self, (0,0), (100, 30))
        self.rect.center = position

        inertia = pymunk.moment_for_box(mass, *self.rect.size)
        self.__body = pymunk.Body(mass, inertia)
        self.__body.position = pymunk.Vec2d(position)
        self.__body.angular_velocity_limit = 100
        self.__body.velocity_limit = 100
        self.__body.velocity_func = self.velocity_func

        self.__poly = pymunk.Poly.create_box(self.__body, size=self.rect.size)
        self.__poly.color = pygame.color.THECOLORS['whitesmoke']

        space.add(self.__body)

        # When body is at 0 degrees.
        self.__forward_vel_norm = pymunk.Vec2d(1, 0)
        self.__reverse_vel_norm = pymunk.Vec2d(-1, 0)
        self.__port_vel_norm = pymunk.Vec2d(1, 0)
        self.__starboard_vel_norm = pymunk.Vec2d(-1, 0)

        size_x, size_y = self.rect.size
        aft_side_off = 1
        aft_side_y = 1
        fore_side_off = 1
        fore_side_y = 1
        self.__aft_thrusters = (
            (pymunk.Vec2d(1, 0), pymunk.Vec2d(-size_x, 0)),
            (pymunk.Vec2d(1, -aft_side_y), pymunk.Vec2d(-size_x,
                                                      size_y * aft_side_off)),
            (pymunk.Vec2d(1, aft_side_y), pymunk.Vec2d(-size_x,
                                                     -size_y * aft_side_off)))

        self.__fore_thrusters = (
            (pymunk.Vec2d(-1, 0), pymunk.Vec2d(size_x, 0)),
            (pymunk.Vec2d(-1, -fore_side_y), pymunk.Vec2d(size_x,
                                                       size_y * fore_side_off)),
            (pymunk.Vec2d(-1, fore_side_y), pymunk.Vec2d(size_x,
                                                      -size_y * fore_side_off)))

    def __apply_force(self, force_vector, mag=1, offset=(0, 0)):
        self.__body.apply_force(self.body_rotated(force_vector * mag),
                                self.body_rotated(offset))

    def body_rotated(self, force_vector):
        return force_vector.rotated(self.__body.angle)

    @property
    def body(self):
        return self.__body

    @property
    def poly(self):
        return self.__poly

    def forward(self, mag=1):
        for t in self.__aft_thrusters:
            self.__apply_force(t[0], mag=mag, offset=t[1])

    def reverse(self, mag=1):
        for t in self.__fore_thrusters:
            self.__apply_force(t[0], mag=mag, offset=t[1])

    def rotate_starboard(self, mag=1):
        fv, fo = self.__fore_thrusters[1]
        av, ao = self.__aft_thrusters[2]
        self.__apply_force(fv, mag=mag, offset=fo)
        self.__apply_force(av, mag=mag, offset=ao)

    def rotate_port(self, mag=1):
        fv, fo = self.__fore_thrusters[2]
        av, ao = self.__aft_thrusters[1]
        self.__apply_force(fv, mag=mag, offset=fo)
        self.__apply_force(av, mag=mag, offset=ao)

    def stabilize_starboard(self, mag=1):
        fv, fo = self.__fore_thrusters[2]
        av, ao = self.__aft_thrusters[2]
        self.__apply_force(fv, mag=mag, offset=fo)
        self.__apply_force(av, mag=mag, offset=ao)

    def stabilize_port(self, mag=1):
        fv, fo = self.__fore_thrusters[1]
        av, ao = self.__aft_thrusters[1]
        self.__apply_force(fv, mag=mag, offset=fo)
        self.__apply_force(av, mag=mag, offset=ao)

    def dampen_local(self, dest_local=pymunk.Vec2d(0,0)):
        """Dampen any lateral motion and rotation when approaching the
        destination local vector.
        """
        pass

    def dampen_world(self, dest_world=pymunk.Vec2d(0, 0),
                     offset=pymunk.Vec2d(0, 0)):
        """

        :param dest_world:
        :return:
        """

        # fixme: all this sucks.... ughhhhhh


        dest_vect = dest_world - self.__body.position

        # Rotation dampening
        local_dest_angle = self.__body.rotation_vector.get_angle_between(-dest_vect)
        coef_dest_angle = local_dest_angle / math.pi

        dm = 2
        dmp = -dm * abs(coef_dest_angle) * self.__body.angular_velocity
        self.rotate_port(dmp)

        local_vel_angle = self.__body.velocity.get_angle_between(-dest_vect)
        coef_vel_angle = local_vel_angle / math.pi

        print(coef_vel_angle)

        dm = .1
        # dmp = -dm * abs(coef_vel_angle) * self.__body.velocity.rotated(local_vel_angle)
        dmp = -dm * abs(coef_vel_angle) * self.__body.velocity #.rotated(self.__body.angle)

        #self.stabilize_port(-dmp)
        #self.stabilize_starboard(dmp)


    def update(self):
        SpriteRect.update(self)
        self.rect.center = self.body.position # Update rect.
        self.__body.reset_forces() # Cancel force accumulation


class Zg(Engine):
    def __init__(self, *args, **kwa):
        Engine.__init__(self, *args, **kwa)

        # Set up the draw surface.
        self.__draw = Fill()
        self.add_render_plain(self.__draw)

        # Set up physics.
        self.__space = pymunk.Space()
        self.__obj = Ship(self.__space)

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.__obj.forward()
        if keys[pygame.K_s]:
            self.__obj.reverse()
        if keys[pygame.K_LEFT]:
            self.__obj.rotate_port()
        if keys[pygame.K_RIGHT]:
            self.__obj.rotate_starboard()
        if keys[pygame.K_a]:
            self.__obj.stabilize_port()
        if keys[pygame.K_d]:
            self.__obj.stabilize_starboard()

    def update(self):
        Engine.update(self)

        self.handle_keys()

        self.__space.step(1/self.fps) # Before update.
        self.__obj.update()
        #self.__obj.dampen_world(dest_world=pymunk.Vec2d(flip_y_normals(pygame.mouse.get_pos(), self.screen_height)))
        self.__draw.fill()  # Clear draw surface.

        # Draw the pymunk simulated poly.
        pymunk.pygame_util.draw(self.__draw.surface, self.__obj.poly)

        # Center of mass
        pygame.draw.circle(self.__draw.surface, (255, 0, 0),
                           flip_y_normals(self.__obj.body.position.int_tuple,
                                          self.screen_height, ret_vec=False), 2, 2)

        # Draw a green line at the front of the "ship"
        poly_verts = self.__obj.poly.get_vertices()
        pygame.draw.line(self.__draw.surface, (0, 255, 0),
                         flip_y_normals(poly_verts[-2],
                                        self.screen_height),
                         flip_y_normals(poly_verts[-1],
                                        self.screen_height))


# Keep this minimal.
if __name__ == "__main__":
    pygame.init()
    game = Zg(pygame.display.set_mode((1200, 512), 0, 32),
                       non_static_background=True)

    game.start()